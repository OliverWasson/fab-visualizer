# Status

Handoff for the next chat. Read this first, then `SCOPE.md`, `DECISIONS.md`, `CONVENTIONS.md`, and `STYLE.md`. Last updated 2026-11-24.

## Where things stand

- **Live site:** https://oliverwasson.github.io/fab-visualizer/ (M0 smoke test). Repo: github.com/OliverWasson/fab-visualizer.
- **Milestone:** M1, the STI vertical slice (SCOPE.md §11). **Sourcing and cell layout are done.** Nothing in `spec/steps.yaml` yet.
- **Branch:** recent work is on `feat/intel32-anchor`. Merge it to `main` once CI is green (`git checkout main && git merge --ff-only feat/intel32-anchor && git push`).

### Done
- Scope and style docs; reference flow anchored to **Intel 32 nm** (gate-last, high-k last, eSiGe PMOS, raised NMOS S/D).
- Palette single source (`spec/materials.yaml` → generated `web/src/generated/materials.ts`) with ΔE contrast checks.
- `python -m pipeline.check` validates palette, generated TS, `spec/steps.yaml`, `spec/sources.md`, and `masks/inverter.yaml`. CI runs it plus `black --check`, ESLint, and the web build; deploys only from `main` when all pass.
- Licenses (MIT code, CC BY 4.0 content), `ATTRIBUTIONS.md`, `.gitignore` guard for PDFs and `references/`.
- `spec/sources.md`: 19 sources with groups (independence), including the `pdk` type.
- STI module fully sourced and decided (DECISIONS.md "STI module, after sourcing").
- Cell layout: `masks/inverter.yaml` (Nangate INV_X1 scaled to Intel pitches), checked by `pipeline/mask_check.py`.

### Next, in order
1. Merge `feat/intel32-anchor` to `main`.
2. Write `spec/steps.yaml` entries for `wafer` and `sti`, with all three text tiers and sourced params (values below). The checker validates as you go.
3. Pipeline geometry for each geometry step, with `__added` / `__removed` delta meshes (CONVENTIONS.md).
4. Tool panels: `furnace`, `rtp`, `litho` (full tour), `etch`, `wet`, `cvd`, `cmp`.
5. Transitions, camera presets, section cuts; palette tuning pass; self-host fonts (verify the `@fontsource` packages).
6. Deferred infrastructure: performance budget + WebGL2 fallback message; root README (replace the Vite template in `web/README.md`).

## Values for the `wafer` and `sti` steps

Source keys resolve to `spec/sources.md`. "verified" = 2+ sources sharing no group.

| Step | Value | Sources | Confidence |
|---|---|---|---|
| Wafer | p-type (100), ~1×10¹⁵ cm⁻³ | PG2023-ch2-p37, Xiao2012-ch13-p550 | verified |
| | 300 mm, 775 µm thick, notch | Xiao2012-ch4-tab4.2, Quirk2001-ch4-p76; notch Xiao2012-ch4-p105, Quirk2001-ch4-p82 | verified |
| | Epi wafer is real practice (`fab_reality`) | Xiao2012-ch4-p109, Xiao2012-ch13-p551 | single-source |
| Pad oxide | ≈15 nm, dry O₂ (thin oxides ≈1000 °C with HCl) | Xiao2012-ch5-p132, Quirk2001-ch9-p208; conditions Xiao2012-ch5-p140 | thickness verified |
| LPCVD nitride | ≈100 nm | Wolf2002-ch9-p447, Pan1998-p1 (both 0.25 µm era) | uncertain |
| | SiH₂Cl₂ + NH₃, 700–800 °C, furnace | Xiao2012-ch5-p165, Quirk2001-ch11-p275, PG2023-ch2-p38 | verified |
| STI litho | 193 nm immersion; coat, soft bake, expose, PEB, develop, hard bake | Natarajan2008-p1, Xiao2012-ch6-p221; conditions Xiao2012-ch6-p187 to p205 | 193i verified |
| STI etch | resist on through nitride, pad oxide, Si; then strip | PG2023-ch2-p39, Quirk2001-ch9-p208 (Xiao2012-ch13-fig13.7 differs; note in `details`) | verified |
| | nitride/oxide: CF₄/CHF₃; Si: HBr/O₂ | Xiao2012-ch9-p342, Ventzek2007-ch21-p20; Xiao2012-ch9-p352, Wolf2002-ch9-p447 | verified |
| | depth ≈200 nm | Natarajan2008-tab1 (IBM alliance ≈300 nm, Tilke2006) | single-source |
| | sidewall ≈87°, rounded bottom corners | Wolf2002-ch9-p455, Tilke2007-p61 | verified |
| Resist strip | O₂ plasma or H₂SO₄/H₂O₂ | PG2023-ch2-p39 | single-source |
| Pad-oxide undercut | short HF dip, improves top-corner rounding | Wolf2002-ch9-p450 | single-source |
| Liner oxidation | ≈15 nm, RTP tool, rounds the top corner | Xiao2012-ch5-tab5.2, Quirk2001-ch9-p209; RTP Timans2007-ch11-p2, Wolf2002-ch9-p451 | verified |
| Gap fill | HDP-CVD, 45° facets at trench tops | Xiao2012-ch13-fig13.7, Pan1998-p3; facets Pan1998-p3, Wolf2002-ch9-p460 | verified |
| | overfill thickness | none for 32 nm | uncertain |
| CMP | stops on nitride; ceria slurry; dishing note | Xiao2012-ch12-p529, Quirk2001-ch9-p209; ceria Xiao2012-ch12-p525 | stop verified |
| Post-CMP anneal | RTA or furnace; temperature/time unsourced | Tilke2007-p60, Xiao2012-ch13-fig13.7 | verified (step) |
| HF deglaze | removes the oxynitride skin before the strip; 100:1 HF ≈1 nm/min | Wolf2002-ch9-p453, PG2023-ch2-p40; rate PG2023-ch9-p413 | verified |
| Nitride strip | hot H₃PO₄, selective to oxide and Si; 180 °C, 91.5%, ≈10 nm/min | PG2023-ch9-p413, Xiao2012-ch9-p328 | selectivity verified |

Final STI oxide stands slightly above the active Si (Pan1998-p1, Shinn2007-ch17-p43; both in the `boning` group, so single-source). The liner is modeled uniform until Intel's channel orientation is known (SCOPE.md §12).

## Cell layout (masks/inverter.yaml)

Cell 225 × 1125 nm (2 CPP × 10 M1 tracks); model 337.5 nm wide (3 CPP). Origin: gate centre (x), cell centre (y); PMOS on top (+y). Gate Lg 30 nm at x = 0, dummies at ±112.5 over STI. W_n ≈ 334 nm, W_p ≈ 506 nm, 141 nm STI between them, gate contact over that STI, well boundary at y ≈ −88 nm. M1: VSS/VDD rails, output strap, input pad; V1 + M2 bring In and Out up. Scaling: x × 112.5/190, y × 112.5/140 (DECISIONS.md "Cell layout").

## Working style (keep doing this)

- macOS, zsh, VS Code; Python env is a uv venv, so install with `uv pip install`, not `pip`.
- Give complete files, plus exact commands. Avoid `#` comments in pasted commands (zsh treats an apostrophe in one as an open quote).
- Downloads may get renamed (`file (1).md`), so move files with `mv -f "$(ls -t ~/Downloads/NAME*.ext | head -1)" dest`.
- Run `black pipeline` and `python -m pipeline.check` before every commit; don't commit on `FAIL`.
- One branch per feature; merge to `main` when CI is green.
- Sources: read a source completely before adding it; then give the full updated `spec/sources.md` to download. Paraphrase, never paste source text. AI output is never a source.
- Locators are hyphen-separated letters, digits, and dots (no underscores): `Xiao2012-ch5-tab5.2`.
- Reference PDFs and kit files live in `references/` (gitignored). Record a lawful access route in each source's **Access** line.
- After changing a doc, also update it in the claude.ai Project knowledge.

## Open items

SCOPE.md §12 has the full verify list. Most relevant soon: nitride thickness at 32 nm, Intel's contact scheme, Intel's channel orientation, dummy poly and poly-cut at Intel 32 nm, Intel-specific cell height and device widths, real-scale well and Vt implants (M2), and the P vs. B diffusivity conflict between Xiao2012 and PG2023 (M2).
