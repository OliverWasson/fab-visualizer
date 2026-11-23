"""Validate spec/steps.yaml and spec/sources.md against CONVENTIONS.md rules.

Every rule here is written down in CONVENTIONS.md, SCOPE.md, or STYLE.md.
If you change a rule there, change it here too (and log it in DECISIONS.md).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from pipeline.materials import REPO_ROOT

STEPS_PATH = REPO_ROOT / "spec" / "steps.yaml"
SOURCES_PATH = REPO_ROOT / "spec" / "sources.md"
MODELS_DIR = REPO_ROOT / "web" / "public" / "models"

MODULES = (
    "wafer",
    "sti",
    "well",
    "gate",
    "ldd",
    "spacer",
    "sige",
    "sd",
    "silicide",
    "rmg",
    "contact",
    "beol",
    "finfet",
)
KINDS = ("geometry", "implant", "thermal", "clean")
TOOLS = (
    "furnace",
    "rtp",
    "litho",
    "etch",
    "wet",
    "implant",
    "cvd",
    "epi",
    "pvd",
    "ald",
    "cmp",
    "ecd",
)
TRANSITIONS = (
    "deposit_conformal",
    "deposit_directional",
    "oxidize",
    "etch_anisotropic",
    "etch_isotropic",
    "cmp",
    "epi",
    "implant",
    "thermal",
    "litho_expose",
    "litho_develop",
    "strip",
)
CAMERA_PRESETS = ("overview", "pmos_x", "nmos_x", "gate_y", "gate_edge")
CUTS = ("pmos_x", "nmos_x", "gate_y", "free", "off")
CONFIDENCE = ("verified", "single-source", "uncertain")

REQUIRED = (
    "id",
    "module",
    "title",
    "kind",
    "tool",
    "summary",
    "explanation",
    "details",
)
OPTIONAL = (
    "mask",
    "transition",
    "camera",
    "cut",
    "callouts",
    "params",
    "fab_reality",
    "model",
    "doping_state",
)
KIND_PARAMS = {
    "implant": ("species", "energy", "dose", "tilt", "twist"),
    "thermal": ("temperature", "time", "ambient"),
}

ID_RE = re.compile(r"^([a-z]+)-(\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9]*)(?:-[A-Za-z0-9.]+)*$")
SOURCE_HEADING_RE = re.compile(r"^###\s+([A-Za-z][A-Za-z0-9]*)\s*$", re.M)
E_NOTATION_RE = re.compile(r"\b\d+(?:\.\d+)?e[+-]?\d+\b")
NO_UNIT_SPACE_RE = re.compile(r"\d(?:nm|µm|um|keV|eV|°C|cm|s|min)\b")
TAG_RE = re.compile(r"<[^>]+>")


def words(text: str) -> int:
    return len(TAG_RE.sub("", text).split())


class _Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


SOURCE_TYPES = (
    "paper",
    "teardown",
    "textbook",
    "review",
    "roadmap",
    "vendor",
    "patent",
    "news",
)
SOURCE_FIELDS = ("Citation", "Type", "Group")
FIELD_RE = re.compile(r"^\s*-\s*\*\*([A-Za-z]+):\*\*\s*(.*?)\s*$")


def load_sources(
    path: Path = SOURCES_PATH,
) -> tuple[dict[str, dict[str, str]] | None, _Report]:
    """Parse sources.md into {base_key: {field: value}} and report format problems."""
    r = _Report()
    if not path.exists():
        return None, r
    entries: dict[str, dict[str, str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            m = SOURCE_HEADING_RE.match(line)
            if not m:
                r.err("spec/sources.md", f"heading {line!r} is not a valid base key")
                current = None
                continue
            current = m.group(1)
            if current in entries:
                r.err(current, "duplicate source key")
            entries[current] = {}
        elif current and (f := FIELD_RE.match(line)):
            entries[current][f.group(1)] = f.group(2)
    for key, fields in entries.items():
        for need in SOURCE_FIELDS:
            if not fields.get(need):
                r.err(key, f"missing **{need}:** line")
        if fields.get("Type") and fields["Type"] not in SOURCE_TYPES:
            r.err(key, f"type {fields['Type']!r} not in {SOURCE_TYPES}")
    return entries, r


def _check_text(r: _Report, where: str, field: str, text: Any) -> None:
    if not isinstance(text, str) or not text.strip():
        r.err(where, f"{field} is empty")
        return
    if text.strip() in ("...", "…"):
        r.warn(where, f"{field} not written yet")
        return
    if E_NOTATION_RE.search(text):
        r.warn(where, f"{field} uses e-notation; write 1×10<sup>13</sup> (STYLE.md §5)")
    if NO_UNIT_SPACE_RE.search(TAG_RE.sub("", text)):
        r.warn(
            where, f"{field} has a number glued to its unit; add a space (STYLE.md §5)"
        )


def _resolve_sources(
    r: _Report, where: str, source: Any, sources: dict[str, dict[str, str]] | None
) -> list[str]:
    """Check one source key or a list of them; return the groups that resolved."""
    keys = source if isinstance(source, list) else [source]
    if not keys:
        r.err(where, "source list is empty")
    groups: list[str] = []
    for key in keys:
        m = SOURCE_RE.match(key) if isinstance(key, str) else None
        if not m:
            r.err(where, f"source {key!r} is not a valid key like PG2023-ch2-p41")
        elif sources is None:
            r.err(where, "spec/sources.md is missing, so sources can't be resolved")
        elif m.group(1) not in sources:
            r.err(
                where,
                f"source base key {m.group(1)!r} has no '### {m.group(1)}' in sources.md",
            )
        else:
            groups.append(sources[m.group(1)].get("Group", m.group(1)))
    return groups


def _check_camera(r: _Report, where: str, cam: Any) -> None:
    if isinstance(cam, str):
        if cam not in CAMERA_PRESETS:
            r.err(where, f"camera preset {cam!r} not in {CAMERA_PRESETS}")
        return
    ok = (
        isinstance(cam, dict)
        and isinstance(cam.get("target"), list)
        and len(cam["target"]) == 3
        and all(isinstance(v, (int, float)) for v in cam["target"])
        and isinstance(cam.get("distance"), (int, float))
        and cam["distance"] > 0
    )
    if not ok:
        r.err(where, "camera must be a preset or {target: [x, y, z], distance: nm > 0}")


def _check_step(
    r: _Report,
    s: dict[str, Any],
    ids_so_far: list[str],
    sources: dict[str, dict[str, str]] | None,
) -> None:
    where = str(s.get("id", f"step #{len(ids_so_far) + 1}"))
    for k in REQUIRED:
        if k not in s:
            r.err(where, f"missing required field {k!r}")
    for k in s:
        if k not in REQUIRED and k not in OPTIONAL:
            r.warn(where, f"unknown field {k!r} (typo?)")

    kind = s.get("kind")
    if kind not in KINDS:
        r.err(where, f"kind {kind!r} not in {KINDS}")
    if s.get("tool") not in TOOLS:
        r.err(where, f"tool {s.get('tool')!r} not in {TOOLS}")
    if "cut" in s and s["cut"] not in CUTS:
        r.err(where, f"cut {s['cut']!r} not in {CUTS}")
    if "camera" in s:
        _check_camera(r, where, s["camera"])

    t = (
        (s.get("transition") or {}).get("type")
        if isinstance(s.get("transition"), dict)
        else None
    )
    if t is None and kind in ("geometry", "implant", "thermal"):
        r.err(where, "transition.type is required for this kind")
    elif t is not None:
        if t not in TRANSITIONS:
            r.err(where, f"transition.type {t!r} not in STYLE.md §7")
        elif kind in ("implant", "thermal") and t != kind:
            r.err(where, f"{kind} steps must use transition {kind!r}")
        elif kind == "geometry" and t in ("implant", "thermal"):
            r.err(where, f"geometry steps can't use transition {t!r}")
        if t and t.startswith("litho") and not s.get("mask"):
            r.warn(where, "litho step has no mask id")

    summary = s.get("summary", "")
    _check_text(r, where, "summary", summary)
    if isinstance(summary, str) and words(summary) > 20:
        r.err(where, f"summary is {words(summary)} words (max 20)")
    expl = s.get("explanation", "")
    _check_text(r, where, "explanation", expl)
    if isinstance(expl, str):
        n = words(expl)
        if n > 100:
            r.err(where, f"explanation is {n} words (max ~80, hard limit 100)")
        elif n > 80:
            r.warn(where, f"explanation is {n} words (target ≤ 80)")
    _check_text(r, where, "details", s.get("details", ""))

    callouts = s.get("callouts") or []
    if len(callouts) > 3:
        r.err(where, f"{len(callouts)} callouts (max 3)")
    for c in callouts:
        if not isinstance(c, dict) or not c.get("anchor") or not c.get("text"):
            r.err(where, "each callout needs anchor and text")
        elif words(c["text"]) > 6:
            r.warn(where, f"callout {c['text']!r} is over 6 words")

    names: set[str] = set()
    for i, p in enumerate(s.get("params") or []):
        pw = f"{where} params[{i}]"
        if not isinstance(p, dict):
            r.err(pw, "must be a mapping")
            continue
        for k in ("name", "value", "source", "confidence"):
            if p.get(k) in (None, "") or p.get(k) == []:
                r.err(pw, f"missing {k!r}")
        if "unit" not in p:
            r.err(pw, "missing 'unit' (use null if dimensionless)")
        if p.get("confidence") and p["confidence"] not in CONFIDENCE:
            r.err(pw, f"confidence {p['confidence']!r} not in {CONFIDENCE}")
        if p.get("source"):
            groups = _resolve_sources(r, pw, p["source"], sources)
            if p.get("confidence") == "verified" and len(set(groups)) < 2:
                r.err(
                    pw, "verified needs 2+ sources from different groups in sources.md"
                )
        names.add(str(p.get("name")))
    for need in KIND_PARAMS.get(kind, ()):
        if need not in names:
            r.err(where, f"{kind} step missing param {need!r}")

    fr = s.get("fab_reality")
    if fr is not None:
        if not isinstance(fr, dict) or not fr.get("note"):
            r.err(where, "fab_reality needs a note")
        elif not fr.get("source"):
            r.err(where, "fab_reality needs its own source")
        else:
            _resolve_sources(r, f"{where} fab_reality", fr["source"], sources)

    for ref in ("model", "doping_state"):
        if s.get(ref) is not None and s[ref] not in ids_so_far:
            r.err(where, f"{ref} {s[ref]!r} must name an earlier step")

    if kind == "geometry" and isinstance(s.get("id"), str):
        if not (MODELS_DIR / f"{s['id']}.glb").exists():
            r.warn(where, "no .glb yet in web/public/models/")


def check_steps(path: Path = STEPS_PATH) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for spec/steps.yaml and spec/sources.md."""
    sources, r = load_sources()
    if sources is None:
        r.warn("spec/sources.md", "not written yet")
    if not path.exists():
        r.warn("spec/steps.yaml", "not written yet")
        return r.errors, r.warnings
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        r.err("spec/steps.yaml", "top level must be a list of steps")
        return r.errors, r.warnings

    ids: list[str] = []
    last_module, last_nn = -1, 0
    for s in data:
        if not isinstance(s, dict):
            r.err("spec/steps.yaml", "every step must be a mapping")
            continue
        sid = s.get("id")
        m = ID_RE.match(sid) if isinstance(sid, str) else None
        if not m:
            r.err(str(sid), "id must look like <module>-<NN>-<short-name>")
        else:
            mod, nn = m.group(1), int(m.group(2))
            if mod != s.get("module"):
                r.err(
                    sid, f"id prefix {mod!r} doesn't match module {s.get('module')!r}"
                )
            if mod not in MODULES:
                r.err(sid, f"module {mod!r} not in {MODULES}")
            else:
                mi = MODULES.index(mod)
                if mi < last_module:
                    r.err(sid, "module appears out of process order")
                elif mi == last_module and nn <= last_nn:
                    r.err(sid, f"NN {nn:02d} must increase within module {mod!r}")
                last_module, last_nn = mi, nn
            if sid in ids:
                r.err(sid, "duplicate id")
        _check_step(r, s, ids, sources)
        if isinstance(sid, str):
            ids.append(sid)
    return r.errors, r.warnings
