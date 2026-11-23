# Conventions

Rules every file and every chat follows. If something here changes, log it in DECISIONS.md.

## Units and coordinates
- **Length unit:** nanometers (nm) everywhere: pipeline, spec, and web scene. No mixed units.
- **Pipeline axes (z-up):**
  - `x` = along the channel (source → drain direction, the cross-section direction of Plummer & Griffin Ch. 2 figures)
  - `y` = along the gate width (into the page in the textbook cross-sections)
  - `z` = vertical, +z up out of the wafer
  - `z = 0` is the **original silicon surface** before any processing.
- **Export:** glTF is y-up, so the pipeline rotates once at export (-90° about x). Nothing else rotates geometry.
- **Origin:** the model is centered in x and y on the inverter cell.

## Geometry files
- One `.glb` per process step **state** (what the wafer looks like after that step).
- Path: `web/public/models/<step-id>.glb`
- Step IDs: `<module>-<NN>-<short-name>`, lowercase, hyphenated, two-digit numbering per module.
  - Examples: `sti-01-pad-oxide`, `sti-02-nitride`, `well-03-boron-implant`
  - Modules: `sti`, `well`, `vt`, `gate`, `ldd`, `spacer`, `sd`, `strain`, `silicide`, `rmg`, `beol`
- glTF node names = material names (see palette), so the web app can toggle/highlight by material.
- Generated `.glb` files are committed (small, and the deploy needs them).

## Material palette
One color per material, used identically in every step. Defined in `pipeline/materials.py` and mirrored in `web/src/materials.ts`.

| Node name | Material | Notes |
|---|---|---|
| `silicon` | crystalline Si | substrate, epi Si |
| `oxide` | SiO₂ (thermal + deposited) | may split later into `oxide_thermal` / `oxide_cvd` |
| `nitride` | Si₃N₄ | hard masks, spacers, liners |
| `photoresist` | resist | |
| `polysilicon` | poly-Si | dummy gate |
| `sige` | SiGe:B | PMOS S/D |
| `silicide` | metal silicide | |
| `highk` | HfO₂ | |
| `metal_tin` | TiN | |
| `metal_tan` | TaN | |
| `metal_al` | Al / Al-based WF + fill | |
| `tungsten` | W | contact plugs |
| `copper` | Cu | interconnect |
| `lowk` | low-k ILD | |

Doping is **not** geometry: it is a color field (shader/texture) computed from the spec, and always labeled illustrative.

## Scale and exaggeration
- Geometry is generated at true scale.
- Any vertical exaggeration happens in the web app only, as a user toggle, and is always labeled on screen.

## Spec and sources
- `spec/steps.yaml` is the single source of truth for step order, parameters, and explanations.
- Every parameter has a source key, e.g. `source: PG2023-ch2-p41-fig2.7`.
- Full citations live in `spec/sources.md`.
- Plummer & Griffin text and figures are **never copied**. Facts and parameters are paraphrased and cited; all geometry and images are our own.
- Where the textbook differs from real fab practice, the step gets a `fab_reality` note with its own source.

## Code style
- Python: 3.12, type hints, small single-purpose modules, `black` formatting.
- TypeScript/React: functional components, Prettier defaults, one component per file.
- Keep files under ~300 lines so they're easy to paste into a chat.

## Workflow
- Branch per feature (`feat/sti-geometry`), merge to `main` when it works.
- Commit after every working step. Message says what changed and why.
- `main` auto-deploys to GitHub Pages.
