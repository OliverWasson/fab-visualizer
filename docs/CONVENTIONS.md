# Conventions

Rules that every file and every chat follows. If something here changes, log it in `DECISIONS.md`. Scope lives in `SCOPE.md`; look and feel in `STYLE.md`.

## Units and coordinates
- **Length unit:** nanometers (nm) everywhere: pipeline, spec, and web scene. No mixed units.
- **Pipeline axes (z-up):**
  - `x`: along the channel (source → drain). In the standard-cell layout this is the direction of the PMOS and NMOS x-cuts.
  - `y`: along the gate width. The single active gate line runs in `y` from the PMOS active area (top) across STI to the NMOS active area (bottom).
  - `z`: vertical, with +z up out of the wafer.
  - `z = 0` is the **original silicon surface** before any processing.
- **Export:** glTF is y-up, so the pipeline rotates once at export (−90° about x). Nothing else rotates geometry.
- **Origin:** the model is centered in x and y on the inverter cell.

## Steps and step IDs
- Every unit operation is a step in `spec/steps.yaml` (see `SCOPE.md` §6).
- Step IDs: `<module>-<NN>-<short-name>`. Lowercase, hyphenated, numbered with two digits per module.
  - Examples: `sti-02-nitride`, `well-03-boron-implant`
- Modules, in process order: `wafer`, `sti`, `well`, `gate`, `ldd`, `spacer`, `sige`, `sd`, `silicide`, `rmg`, `contact`, `beol`, `finfet`
- Each step has a `kind`: `geometry`, `implant`, `thermal`, or `clean`.

## Geometry files
- One `.glb` per **geometry state**: what the wafer looks like after a `geometry` step. Non-geometry steps emit no `.glb` and reuse the latest one.
- Path: `web/public/models/<step-id>.glb`
- **Node names:**
  - `<material>`: the state's geometry, one merged mesh per material (names from the palette).
  - `<material>__added`: material added by this step, with the morph targets its transition needs.
  - `<material>__removed`: material removed by this step, shown only during the transition.
  - `anchor__<name>`: empty nodes that callouts attach to.
  - The web app toggles and highlights by base material name, ignoring the suffix.
- Generated `.glb` files are committed (they're small, and the deploy needs them).

## Tool files
- Path: `web/public/tools/<tool-id>.glb`
- Tool IDs: `furnace`, `rtp`, `litho`, `etch`, `wet`, `implant`, `cvd`, `epi`, `pvd`, `ald`, `cmp`, `ecd`
- Node names: `hw__<part>` for hardware, `wafer` for the wafer, and `fx__<accent>` for process effects (accent names from `STYLE.md` §3.3).

## Doping files
- Path: `web/public/doping/<step-id>.bin` plus `<step-id>.json`, keyed by the step that produced that doping state.
- Content: illustrative signed **net** doping on an `x × y × z` grid. `x` and `y` are uniform; `z` is non-uniform, fine near the surface and coarse deep. The `.json` lists the axis coordinates in nm, the grid shape, and the source step.
- Encoding (`uint8`): with `m = clamp((log10|N_D − N_A| − 15) / 6, 0, 1)`, store `byte = 128 + sign(N_D − N_A) · round(127·m)`. A value of 128 means below 10¹⁵ cm⁻³ (untinted).
- Doping is not geometry and is always labeled illustrative on screen.

## Material palette
One color per material, used identically in every step and in both themes. Defined once in `spec/materials.yaml`. `pipeline/materials.py` loads it, and `web/src/generated/materials.ts` is generated from it (never edit the generated file by hand). `STYLE.md` §3 documents the values and the rules.

| Node name | Material | Notes |
|---|---|---|
| `silicon` | crystalline Si | substrate |
| `oxide_grown` | SiO₂, grown | pad, liner, dummy gate, reoxidation, interfacial oxide |
| `oxide_deposited` | SiO₂, deposited | STI fill, ILD0 |
| `nitride` | Si₃N₄ | hard masks, spacers, CESL |
| `etchstop` | SiCN | BEOL Cu cap / etch stop |
| `photoresist` | resist + BARC | modeled as one layer |
| `polysilicon` | poly-Si | dummy gate |
| `sige` | SiGe:B | PMOS S/D |
| `silicide` | NiPt silicide | |
| `highk` | HfO₂ | |
| `metal_tin` | TiN | |
| `metal_tan` | TaN / Ta | |
| `metal_al` | Al / Al-based work function + fill | |
| `tungsten` | W | contact plugs |
| `copper` | Cu | interconnect |
| `lowk` | low-k ILD | |

## Scale and exaggeration
- Geometry is generated at true scale.
- Vertical exaggeration (1× / 2× / 4×) happens in the web app only, as a user toggle, and is always labeled on screen.
- The substrate is truncated below the well junction plus a margin, with a break marker.

## Spec schema (`spec/steps.yaml`)
`spec/steps.yaml` is the single source of truth for step order, parameters, and explanations. The example below uses `...` wherever a value still has to be written and sourced.

```yaml
- id: sti-02-nitride
  module: sti
  title: Nitride deposition
  kind: geometry            # geometry | implant | thermal | clean
  tool: furnace             # tool-id
  mask: null                # mask id on litho steps
  transition:
    type: deposit_conformal # see STYLE.md §7
  camera: overview          # preset or {target: [x,y,z], distance: nm}
  cut: nmos_x               # pmos_x | nmos_x | gate_y | free | off
  callouts:                 # max 3
    - anchor: pad_oxide
      text: Pad oxide
  summary: ...
  explanation: ...
  details: ...
  params:
    - name: precursors
      value: SiH<sub>2</sub>Cl<sub>2</sub> + NH<sub>3</sub>
      unit: null
      source: PG2023-ch2-p38      # one key, or a list of keys
      confidence: single-source   # verified | single-source | uncertain
  fab_reality:              # optional
    note: ...
    source: ...
```

- `model` and `doping_state` default to the latest available. Set them explicitly only to override.
- Implant steps include `species`, `energy`, `dose`, `tilt`, and `twist` params. Thermal steps include `temperature`, `time`, and `ambient`.
- `confidence`: `verified` means two or more independent sources agree, which the checker enforces as sources from at least two different **Group**s in `sources.md`; `single-source` means one; `uncertain` means flagged and not yet confirmed.

## Sources
- Every parameter has a source key, for example `source: PG2023-ch2-p41-fig2.7`.
- Full citations live in `spec/sources.md`, one per `### <BASEKEY>` heading (for example `### PG2023`). A source key is the base key plus an optional locator after the first hyphen, so `PG2023-ch2-p41-fig2.7` resolves to `PG2023`.
- Each `sources.md` entry has **Citation**, **Type**, and **Group** lines; the file's header lists the allowed types and what makes sources independent.
- AI output, including Claude's, is never a source. A value enters `steps.yaml` only when it traces to a document someone actually read.
- Reference PDFs are **never committed** (`*.pdf` and `references/` are gitignored). Keep local copies in `references/`.
- Plummer & Griffin text and figures are **never copied**. Facts and parameters are paraphrased and cited; all geometry and images are our own.
- Where the textbook differs from real fab practice, the step gets a `fab_reality` note with its own source.

## Code style
- Python: 3.12, type hints, small single-purpose modules, `black` formatting.
- TypeScript/React: functional components, Prettier defaults, one component per file.
- Keep files under ~300 lines so they're easy to paste into a chat.

## Workflow
- One branch per feature (`feat/sti-geometry`); merge to `main` when it works.
- Commit after every working step. The message says what changed and why.
- Run `python -m pipeline.check` and `black pipeline` before committing. CI runs both (plus ESLint and the web build) on every push and pull request.
- `main` auto-deploys to GitHub Pages, but only when every check passes.
- The rules `pipeline/spec_check.py` enforces are the ones written in these docs. Change a rule in both places, and log it in `DECISIONS.md`.
