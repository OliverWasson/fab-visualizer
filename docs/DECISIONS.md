# Decisions log

Newest at the bottom. Each entry: date, decision, why. Don't relitigate a logged decision without adding a new entry that supersedes it.

## 2026-11-23: Device and flow
- **Model a 28 nm-class planar, gate-last high-k/metal-gate CMOS inverter.**
  Based on Plummer & Griffin (2023 prepublication), Ch. 2. Planar keeps every step visible and geometrically simple. A FinFET/GAA epilogue comes at the end.
- **The textbook flow is the backbone, corrected where it departs from real fab practice.** Known corrections, each shown as a "fab reality" note:
  - Intel 45 nm was high-k *first*, metal gate last. Our high-k-last flow matches 32/28 nm.
  - NMOS strain in production was mainly tensile nitride stress liners (Intel 90 nm), not SiC:P epitaxy.
  - Ti salicide at 350–450 °C is NiSi territory. TiSi₂ (C49 → C54) needs ~600–800 °C, and 28 nm used NiPt silicide.
  - STI gap fill at this node was HDP-CVD / SACVD (O₃-TEOS) / flowable CVD, not simple LPCVD SiH₄ + O₂.
  - Si–O is a stronger bond than Si–N (the textbook p. 38 says the reverse).
  - "Si₂Cl₂" on p. 38 is a typo for SiH₂Cl₂.
  - Intel 22 nm was tri-gate (three-sided), not double-gate.

## 2026-11-23: Architecture
- **Geometry is generated offline by a scripted Python pipeline**
  (manifold3d + trimesh + shapely) from our own mask polygons and spec parameters. It exports one `.glb` per step. The browser only loads and animates. Why: reproducible, parameter-driven, consistent across steps.
- **Web stack:** Vite + React + TypeScript + react-three-fiber + drei.
- **Hosting:** GitHub Pages via GitHub Actions, auto-deploying on push to `main`.
- **Tools are generic schematic cutaways** (~10 tool classes, reused across steps), not replicas of specific vendors' products.

## 2026-11-23: Content and IP
- Plummer & Griffin is cited as a reference only. No copied text or traced figures. All geometry and visuals are original.
- Each step is cross-checked against at least one other source.
- Consider asking the authors for permission or feedback before launch.

## Open questions
- Vertical exaggeration factor and UI for it.
- Doping visualization: shader vs. baked texture.
- Whether oxide splits into thermal vs. deposited materials visually.
