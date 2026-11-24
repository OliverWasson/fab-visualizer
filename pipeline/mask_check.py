"""Validate masks/inverter.yaml: cell geometry, connectivity, and the rules in DECISIONS.md.

Every rule here is a hard geometric fact the 3D model depends on. Scaled FreePDK45
spacings are not enforced, because the two scale directions make them approximate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.materials import REPO_ROOT
from pipeline.spec_check import CONFIDENCE, _Report, _resolve_sources, load_sources

MASKS_PATH = REPO_ROOT / "masks" / "inverter.yaml"
Rect = tuple[float, float, float, float]
EPS = 0.05  # nm tolerance for rounding to 0.1 nm

# contact net -> metal1 net it must land on
CONTACT_TO_M1 = {
    "src_n": "vss",
    "drn_n": "out",
    "src_p": "vdd",
    "drn_p": "out",
    "gate": "in",
}


def _rect(v: Any) -> Rect:
    x0, y0, x1, y1 = (float(t) for t in v)
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def inside(a: Rect, b: Rect) -> bool:
    return (
        a[0] >= b[0] - EPS
        and a[1] >= b[1] - EPS
        and a[2] <= b[2] + EPS
        and a[3] <= b[3] + EPS
    )


def overlap(a: Rect, b: Rect) -> bool:
    return (
        a[0] < b[2] - EPS
        and b[0] < a[2] - EPS
        and a[1] < b[3] - EPS
        and b[1] < a[3] - EPS
    )


def inside_any(a: Rect, rects: list[Rect]) -> bool:
    """Rect lies inside the union of axis-aligned rects (checked on a 0.5 nm sample grid)."""
    if any(inside(a, r) for r in rects):
        return True
    step = 0.5
    x = a[0] + step / 2
    while x < a[2]:
        y = a[1] + step / 2
        while y < a[3]:
            if not any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for r in rects):
                return False
            y += step
        x += step
    return True


def _nets(layer: Any) -> dict[str, list[Rect]]:
    return {k: [_rect(r) for r in v] for k, v in (layer or {}).items()}


def check_masks(path: Path = MASKS_PATH) -> tuple[list[str], list[str]]:
    r = _Report()
    if not path.exists():
        r.warn("masks/inverter.yaml", "not written yet")
        return r.errors, r.warnings
    m = yaml.safe_load(path.read_text(encoding="utf-8"))
    where = "masks/inverter.yaml"
    params = {p["name"]: p for p in m.get("params", [])}
    sources, _ = load_sources()
    for name, p in params.items():
        if p.get("confidence") not in CONFIDENCE:
            r.err(
                where,
                f"param {name}: confidence {p.get('confidence')!r} not in {CONFIDENCE}",
            )
        _resolve_sources(r, f"{where} param {name}", p.get("source"), sources)

    def val(name: str) -> float:
        if name not in params:
            r.err(where, f"missing param {name!r}")
            return float("nan")
        return float(params[name]["value"])

    cpp, lg, m1p, tracks = val("cpp"), val("lg"), val("m1_pitch"), val("tracks")
    cell = m["cell"]
    if abs(cell["width"] - 2 * cpp) > EPS:
        r.err(where, f"cell width {cell['width']} != 2 x cpp ({2 * cpp})")
    if abs(cell["height"] - tracks * m1p) > EPS:
        r.err(
            where, f"cell height {cell['height']} != tracks x m1_pitch ({tracks * m1p})"
        )

    L = m["layers"]
    ext = (
        m["model_extent"]["x"][0],
        m["model_extent"]["y"][0],
        m["model_extent"]["x"][1],
        m["model_extent"]["y"][1],
    )
    active, poly = _nets(L.get("active")), _nets(L.get("poly"))
    m1, m2, v1 = _nets(L.get("metal1")), _nets(L.get("metal2")), _nets(L.get("via1"))
    nwell, pwell = _rect(L["nwell"][0]), _rect(L["pwell"][0])
    contacts = [(c["net"], _rect(c["rect"])) for c in L.get("contact", [])]

    for lname, groups in (
        ("active", active),
        ("poly", poly),
        ("metal1", m1),
        ("metal2", m2),
        ("via1", v1),
    ):
        for net, rects in groups.items():
            for rc in rects:
                if not inside(rc, ext):
                    r.err(where, f"{lname}.{net} {rc} lies outside model_extent")

    gate = poly.get("gate", [])
    if not gate or abs((gate[0][2] - gate[0][0]) - lg) > EPS:
        r.err(where, "first poly.gate rect must be the gate line, lg wide")
    for side, sign in (("dummy_left", -1), ("dummy_right", 1)):
        d = poly.get(side, [])
        if not d:
            r.err(where, f"missing poly.{side}")
            continue
        cx = (d[0][0] + d[0][2]) / 2
        if abs(cx - sign * cpp) > EPS or abs((d[0][2] - d[0][0]) - lg) > EPS:
            r.err(where, f"poly.{side} must be lg wide, centred at {sign * cpp}")
        for a in active.values():
            if overlap(d[0], a[0]):
                r.err(where, f"poly.{side} overlaps active; dummies must sit over STI")

    n_act, p_act = active["nmos"][0], active["pmos"][0]
    if not (n_act[3] < nwell[1] + EPS and nwell[1] < p_act[1] + EPS):
        r.err(
            where, "well boundary must lie in the STI gap between NMOS and PMOS active"
        )
    if not inside(n_act, pwell) or not inside(p_act, nwell):
        r.err(where, "NMOS active must be in pwell and PMOS active in nwell")

    for net, rc in contacts:
        cw = f"contact {net} {rc}"
        if net not in CONTACT_TO_M1:
            r.err(where, f"{cw}: unknown net")
            continue
        if net == "gate":
            if not inside_any(rc, gate):
                r.err(where, f"{cw}: must lie inside gate poly")
            if any(overlap(rc, a[0]) for a in active.values()):
                r.err(where, f"{cw}: gate contact must land over STI, not active")
        else:
            act = n_act if net.endswith("_n") else p_act
            if not inside(rc, act):
                r.err(where, f"{cw}: must lie inside its active area")
            if any(overlap(rc, g) for g in gate):
                r.err(where, f"{cw}: overlaps the gate")
        if not inside_any(rc, m1.get(CONTACT_TO_M1[net], [])):
            r.err(where, f"{cw}: not covered by metal1 net {CONTACT_TO_M1[net]!r}")

    for net, rects in v1.items():
        for rc in rects:
            if not inside_any(rc, m1.get(net, [])) or not inside_any(
                rc, m2.get(net, [])
            ):
                r.err(
                    where,
                    f"via1 {net} {rc}: must lie inside metal1 and metal2 of net {net!r}",
                )

    for lname, groups in (("metal1", m1), ("metal2", m2)):
        nets = list(groups)
        for i, a in enumerate(nets):
            for b in nets[i + 1 :]:
                if any(overlap(x, y) for x in groups[a] for y in groups[b]):
                    r.err(where, f"{lname}: nets {a!r} and {b!r} short")
    return r.errors, r.warnings
