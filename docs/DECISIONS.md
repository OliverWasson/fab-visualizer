# Decisions log

Newest entries go at the bottom. Each entry has a date, the decision, and why. Don't relitigate a logged decision without adding a new entry that supersedes it.

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

## 2026-11-23: Scope (see SCOPE.md)
- **Layered audience.** The primary reader has intro science/engineering background. Each step has `summary`, `explanation`, and `details` tiers. Why: one site that teaches by default and holds up to an engineer's scrutiny.
- **A real standard-cell inverter, not the textbook's side-by-side layout.** One gate line crosses PMOS over NMOS, with dummy poly at the cell edges. Why: it's accurate, and the y-cut gives the 3D view something the book can't show.
- **BEOL goes through V1 + M2.** Why: one dual-damascene module teaches the repeating unit of the interconnect stack.
- **Granularity.** Every unit operation is a step, but only `geometry` steps emit a `.glb`. This *supersedes* "one `.glb` per step" in the Architecture entry. Why: avoids dozens of duplicate meshes, and lets thermal steps show doping change while the geometry stays still.
- **Reference flow is a generic gate-last 28 nm foundry archetype,** with Intel 32 nm differences as notes. Gate-first flows are out of scope.
- **Geometry corrections G1–G6 adopted** (SCOPE.md §7): true vertical scale; NMOS strain via tensile CESL instead of SiC:P; Σ-recess SiGe:B after the spacer with no PMOS deep implant; NiPt silicide before ILD0 with the gate hard mask kept; an offset spacer; retrograde wells with Vt implants under the well masks. G2–G4 are medium confidence and need verification.
- **Module list changed:** `vt` merged into `well` (G6); `strain` renamed `sige`, since NMOS strain is now the CESL in `rmg`; `wafer`, `contact`, and `finfet` added.
- **12 tool classes,** built in the Python pipeline and exported to `web/public/tools/`. This *supersedes* "~10 tool classes." Why: that's the number of distinct hardware types the corrected flow actually uses.
- **Lithography:** a full walkthrough at the STI mask, then two steps per mask. Resist and BARC are one layer; the gate hard mask is modeled.
- **Non-goals, FinFET epilogue (~5 states + static GAA), and an STI vertical slice first** (SCOPE.md §9–11).

## 2026-11-23: Style (see STYLE.md)
- **Technical-illustration rendering,** not photoreal. Why: nothing at this scale has a visible appearance, and matte, outlined solids keep every layer readable.
- **Hue is reserved for physics.** Material, dopant type, and process energy each get their own color family. The UI is monochrome.
- **Palette hex values set** (STYLE.md §3), with one tuning pass allowed during the STI slice.
- **Oxide split into `oxide_grown` and `oxide_deposited`.** Resolves the open question. The names describe origin rather than tool, because the sub-nm chemical interfacial oxide is grown but not thermal.
- **Added `etchstop` (SiCN)** for the BEOL Cu cap / etch-stop layers.
- **Vertical exaggeration:** default 1×, toggle 1× / 2× / 4×, thin films handled by camera framing. Resolves the open question.
- **Doping:** a baked 3D net-doping texture from the pipeline, sampled in the silicon and SiGe materials. Resolves the open question. Why: the physics stays offline in Python, the same split as the geometry.
- **Typed transitions with pipeline-generated delta meshes.** Node names gain `__added` / `__removed` suffixes and `anchor__` empties.
- **Camera flies to each step's framing,** with a Keep-my-view toggle. Each step sets a default section cut, plus presets and a free plane. Hash routing, since GitHub Pages has no SPA fallback.
- **Light scene background is the cool neutral `#E9ECEF`**, not the warm cream used in the swatch preview. Why: warm cream is a common tell of generated sites, and a cool tone fits the cleanroom subject.
- **Fonts: Oxanium (display), Atkinson Hyperlegible Next (body), Kode Mono (data), all self-hosted.** Why: a futuristic voice limited to short strings, with readable body and data text that keeps confusable characters (O/0, l/1) distinct.

## 2026-11-23: Repo infrastructure
- **The palette has one source: `spec/materials.yaml`.** `pipeline/materials.py` loads it, and `pipeline/gen_materials_ts.py` generates `web/src/generated/materials.ts`, which is committed so the web build needs no Python. This *supersedes* "mirrored in `materials.py` and `materials.ts`." Why: hand-mirrored colors drift.
- **The generator enforces STYLE.md §3.1.** CIE76 ΔE ≥ 15 for every pair listed in `adjacent_pairs`. A per-pair override requires a written reason (the two oxides use 9). Contrast against the scene background warns below 10; currently both oxides warn against the light background, to revisit in the STI tuning pass.
- **Every documented rule is checked automatically.** `python -m pipeline.check` validates the palette, the generated TS, and `spec/steps.yaml` (IDs and order, allowed values, text-tier word limits, notation, params with sources and confidence, required implant/thermal params, `fab_reality` sources). CI runs it with `black --check` and ESLint, and deploys from `main` only when all pass. Written in plain Python rather than pydantic, so it adds no dependency and could be tested end to end. Why: accuracy rules a person has to remember will eventually be missed.
- **A missing `.glb` for a geometry step is a warning until M1 is done,** then becomes an error.

## Open questions
- None at the architecture level. Open facts that still need sources are listed in SCOPE.md §12.
