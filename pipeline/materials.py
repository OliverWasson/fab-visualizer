"""Load and validate the project palette from spec/materials.yaml.

This module holds no colors itself: spec/materials.yaml is the single source.
Rules enforced here come from STYLE.md §3.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "spec" / "materials.yaml"

_HEX = re.compile(r"^#[0-9A-F]{6}$")
SHADING_KINDS = ("semiconductor", "dielectric", "metal")


@dataclass(frozen=True)
class Material:
    id: str
    hex: str
    shading: str
    doping_tint: bool
    label: str
    name: str
    roughness: float
    metalness: float

    @property
    def srgb(self) -> tuple[float, float, float]:
        return hex_to_srgb(self.hex)

    @property
    def linear_rgba(self) -> tuple[float, float, float, float]:
        """Linear-light RGBA, as glTF baseColorFactor expects."""
        r, g, b = (_srgb_to_linear(c) for c in self.srgb)
        return (r, g, b, 1.0)


@dataclass(frozen=True)
class Palette:
    materials: dict[str, Material]
    doping: dict[str, Any]
    accents: dict[str, str]
    tool_hardware: dict[str, str]
    scene_bg: dict[str, str]
    raw: dict[str, Any]


class PaletteError(ValueError):
    """Raised when spec/materials.yaml breaks a palette rule."""


# ---------- color math ----------


def hex_to_srgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_lab(h: str) -> tuple[float, float, float]:
    """sRGB hex -> CIELAB (D65)."""
    r, g, b = (_srgb_to_linear(c) for c in hex_to_srgb(h))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(a: str, b: str) -> float:
    """CIE76 colour difference between two hex colours."""
    return math.dist(hex_to_lab(a), hex_to_lab(b))


# ---------- loading ----------


def _check_hex(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not _HEX.match(value):
        errors.append(f"{where}: {value!r} is not an uppercase #RRGGBB hex")


def load(path: Path = SPEC_PATH) -> Palette:
    """Load the palette, raising PaletteError listing every rule violation."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    shading = raw.get("shading", {})
    for kind in SHADING_KINDS:
        if kind not in shading:
            errors.append(f"shading: missing preset {kind!r}")

    materials: dict[str, Material] = {}
    for i, m in enumerate(raw.get("materials", [])):
        where = f"materials[{i}] ({m.get('id', '?')})"
        missing = {"id", "hex", "shading", "doping_tint", "label", "name"} - m.keys()
        if missing:
            errors.append(f"{where}: missing {sorted(missing)}")
            continue
        if not re.fullmatch(r"[a-z][a-z0-9_]*", m["id"]):
            errors.append(f"{where}: id must be lowercase snake_case")
        if m["id"] in materials:
            errors.append(f"{where}: duplicate id")
        _check_hex(m["hex"], where, errors)
        if m["shading"] not in SHADING_KINDS:
            errors.append(f"{where}: shading must be one of {SHADING_KINDS}")
            continue
        preset = shading.get(m["shading"], {})
        materials[m["id"]] = Material(
            id=m["id"],
            hex=m["hex"],
            shading=m["shading"],
            doping_tint=bool(m["doping_tint"]),
            label=m["label"],
            name=m["name"],
            roughness=float(preset.get("roughness", 0.8)),
            metalness=float(preset.get("metalness", 0.0)),
        )

    doping = raw.get("doping", {})
    for t in ("n", "p"):
        stops = doping.get(t, [])
        if len(stops) != 5:
            errors.append(f"doping.{t}: expected 5 stops, got {len(stops)}")
        for j, c in enumerate(stops):
            _check_hex(c, f"doping.{t}[{j}]", errors)

    for group in ("accents", "tool_hardware", "scene_bg"):
        for k, c in raw.get(group, {}).items():
            _check_hex(c, f"{group}.{k}", errors)

    if errors:
        raise PaletteError("\n".join(errors))

    return Palette(
        materials=materials,
        doping=doping,
        accents=dict(raw.get("accents", {})),
        tool_hardware=dict(raw.get("tool_hardware", {})),
        scene_bg=dict(raw.get("scene_bg", {})),
        raw=raw,
    )


# ---------- contrast rules (STYLE.md §3.1) ----------


def check_contrast(p: Palette) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for adjacent-pair and background contrast."""
    errors: list[str] = []
    warnings: list[str] = []
    rules = p.raw.get("contrast", {})
    floor = float(rules.get("min_delta_e", 15))
    bg_warn = float(rules.get("bg_warn_delta_e", 10))
    seen: set[frozenset[str]] = set()

    for entry in p.raw.get("adjacent_pairs", []):
        if isinstance(entry, dict):
            pair = entry.get("pair", [])
            limit = entry.get("min_delta_e")
            reason = entry.get("reason")
            if limit is not None and not reason:
                errors.append(
                    f"adjacent pair {pair}: min_delta_e override needs a reason"
                )
            limit = float(limit) if limit is not None else floor
        else:
            pair, limit = entry, floor
        if len(pair) != 2 or any(x not in p.materials for x in pair):
            errors.append(f"adjacent pair {pair}: must name two known materials")
            continue
        key = frozenset(pair)
        if key in seen:
            errors.append(f"adjacent pair {pair}: listed twice")
        seen.add(key)
        de = delta_e(p.materials[pair[0]].hex, p.materials[pair[1]].hex)
        if de < limit:
            errors.append(f"{pair[0]} / {pair[1]}: ΔE {de:.1f} < {limit:g}")

    for theme, bg in p.scene_bg.items():
        for m in p.materials.values():
            de = delta_e(m.hex, bg)
            if de < bg_warn:
                warnings.append(
                    f"{m.id} vs {theme} scene background: ΔE {de:.1f} < {bg_warn:g}"
                )

    return errors, warnings
