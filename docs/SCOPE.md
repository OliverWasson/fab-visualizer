# Scope

What this site models, explains, and leaves out. Approved 2026-11-23. Any change goes through `DECISIONS.md` first.

## 1. Purpose

An interactive 3D site that shows how a 28 nm-class planar CMOS inverter is made, one process step at a time, alongside the tool that performs each step.

Accuracy is the top priority:
- Every process parameter is sourced.
- Uncertainty is flagged in the data, not just in prose.
- Places where the textbook flow differs from real fab practice are called out explicitly.

## 2. Audience and text depth

**Primary reader:** someone with intro-level science or engineering background. They know roughly what a transistor is but not how one is manufactured.

**Secondary readers:** EE students, process engineers, and reviewers (hiring managers, the textbook authors) who open the details to check rigor.

Every step carries three text tiers:

| Field | Reader | Length | Content |
|---|---|---|---|
| `summary` | anyone | one line, ≤ 20 words | What happens, in plain words |
| `explanation` | primary reader | 2–4 sentences, ≤ ~80 words | What happens and why it happens at this point in the order |
| `details` | engineer | open-ended, collapsible | Parameters table, equations, `fab_reality`, metrology notes |

Writing rules:
- All wording is original. Plummer & Griffin is paraphrased and cited, never copied.
- Explain ordering. The main thing Ch. 2 teaches is *why this step comes here*.
- A term is defined in the tier where it first appears.

## 3. Reference flow

The model follows a **generic gate-last 28 nm foundry archetype**: HKMG with high-k last and metal gate last.

- Where Intel 32 nm differed, that difference goes in a `fab_reality` note.
- Gate-first 28 nm flows (the IBM alliance: GlobalFoundries and Samsung) are out of scope and get one mention.
- Any claim about what a specific company did needs a second source.

## 4. What the model contains

**Layout:** a real standard-cell inverter, not the textbook's side-by-side teaching layout (Plummer & Griffin Fig. 2.3).
- One active gate line runs in `y`. It crosses the PMOS active area (top, in the N-well) and the NMOS active area (bottom, in the P-well), passing over the STI between them.
- The N-well/P-well boundary lies under that STI.
- Dummy poly lines sit at both cell edges, per restrictive design rules (verify, §12).
- The gate contact lands on the gate where it crosses the STI.
- M1 carries a VDD rail along the top edge, a GND rail along the bottom edge, the S/D contacts, and the output strap joining the two drains.
- V1 and M2 bring the In and Out pins up one level, so a dual-damascene module appears exactly once.

**Extent:**
- The plan footprint is set by cell height and contacted poly pitch (roughly 0.8–1 µm × 0.4 µm; real values to be sourced).
- Vertical geometry is true scale (correction G1).
- The substrate is truncated below the well junction plus a margin. The bottom face gets a break marker and a note that the wafer continues to about 775 µm thick.

**BEOL:** W contacts, M1, then V1 + M2. A final stylized zoom-out says that roughly 8–12 more levels follow, without modeling them. Whether M1 is single or dual damascene still needs verifying (§12).

Coordinates, units, and naming follow `CONVENTIONS.md`.

## 5. Module order

This is an outline only. Parameters, sources, and exact step lists belong in `spec/steps.yaml`. Lithography appears as two steps per mask (§8), except for the full tour at the STI mask.

| Module | Main steps |
|---|---|
| `wafer` | Starting substrate: p-type (100), ~10¹⁵ cm⁻³ |
| `sti` | Pad oxide · LPCVD nitride · **full litho tour** · nitride/oxide/Si etch · resist strip · liner oxidation · gap fill (HDP/SACVD class) · CMP · HF deglaze · nitride strip |
| `well` | Screen oxide · N-well mask: deep well, punch-through, and Vt implants (P) · strip · P-well mask: same set (B) · strip · short anneal |
| `gate` | Screen oxide strip · dummy gate oxide · poly · nitride hard mask · gate mask (poly-cut mask?, §12) · gate etch · strip · reoxidation |
| `ldd` | Offset spacer deposition and etch · PMOS halo + extension implants · NMOS halo + extension implants · anneal (method to verify) |
| `spacer` | Main spacer deposition · anisotropic spacer etch |
| `sige` | Nitride hard mask · PMOS open · Σ recess · in-situ B-doped SiGe epi · hard mask strip |
| `sd` | NMOS deep S/D mask · implant · strip · activation anneal (spike/millisecond) |
| `silicide` | Pre-clean · NiPt deposition · first anneal · selective strip · second anneal (anneal count to verify) |
| `rmg` | Tensile CESL · ILD0 · CMP to poly-open · dummy poly removal · dummy oxide removal · interfacial oxide · HfO₂ · TiN cap · TaN etch stop · PMOS work-function TiN · NMOS open and TiN etch · Al work function + fill · CMP |
| `contact` | ILD · contact mask · etch · Ti/TiN liner · W CVD · CMP |
| `beol` | M1: cap/etch stop, low-k, trench, barrier/seed, ECD, anneal, CMP · V1 + M2: dual damascene · passivation as a note only |
| `finfet` | Epilogue (§10) |

## 6. Step granularity

- **Every unit operation is a step** in `steps.yaml`, so the narrative is complete.
- Each step has a `kind`: `geometry`, `implant`, `thermal`, or `clean`.
- **Only `geometry` steps emit a `.glb`.** Other kinds reuse the latest model. Implant and thermal steps update the doping texture; thermal steps also show a thermal-budget readout.
- **A clean is its own step only if** it removes material or the narrative depends on it (HF deglaze, the strip before gate oxidation, the pre-epi HF). Other cleans are mentioned in the explanation text of a neighboring step.
- **Metrology is never a step.** It appears in `details` where it matters, such as CMP endpoint or etch endpoint detection.

## 7. Fab-reality corrections

### 7.1 Geometry-changing (modeled the real way)

Each becomes a `fab_reality` note on the affected steps, citing its own source.

| # | Textbook | Modeled instead | Confidence |
|---|---|---|---|
| G1 | Vertically compressed simulation domain: STI ~40 nm, 3–10 keV well implants | Real-scale depths: STI on the order of 250–350 nm, retrograde wells below the STI | High that the textbook is compressed; values to source |
| G2 | NMOS strain from SiC:P epi | Tensile nitride CESL after silicide; stress memorization (SMT) as a text note | Medium, verify |
| G3 | PMOS deep S/D implant, then recess + SiGe | Σ recess + in-situ B-doped SiGe right after the main spacer, before the NMOS deep S/D; no PMOS deep implant | Medium-high on order; medium on Σ shape, verify |
| G4 | TiSi₂ at 350–450 °C with a TiN strip | NiPt silicide before ILD0; poly protected by the gate nitride hard mask; Intel-style trench silicide as a note | Medium-high, verify timing |
| G5 | One 10 nm spacer; extensions implanted against the bare gate | Thin offset spacer before halo/extension implants, then the main spacer | High |
| G6 | Well drive-in at 1000 °C for 10 min; separate well and Vt masks | One mask per well carrying deep-well, punch-through, and Vt implants, then a short anneal | High |

### 7.2 Text-only

- Intel 45 nm was high-k first, metal gate last. Our high-k-last flow matches 32/28 nm.
- STI gap fill was HDP-CVD, SACVD (O₃-TEOS), or flowable CVD, not LPCVD SiH₄ + O₂. This changes the tool class but not the modeled shape.
- Si–O is the stronger bond, not Si–N (the textbook, p. 38, says the reverse).
- "Si₂Cl₂" on p. 38 is a typo for SiH₂Cl₂.
- Intel 22 nm was tri-gate (three-sided), not double-gate. This goes in the epilogue.
- The textbook says FinFET is the current state of the art. That's outdated: gate-all-around nanosheets are in production. This also goes in the epilogue.
- The textbook's layout (Fig. 2.3) is a teaching layout. Real cells stack PMOS over NMOS on one gate line.

## 8. Tools and lithography

### 8.1 Tool classes

Generic schematic cutaways, not replicas of any vendor's product. Built in the Python pipeline from primitives and exported to `web/public/tools/<tool-id>.glb`.

| `tool-id` | Class | Used for |
|---|---|---|
| `furnace` | Vertical batch furnace | Thermal oxidation, liner oxide, LPCVD nitride and poly |
| `rtp` | Rapid thermal / millisecond anneal | Well anneal, spike/flash S/D anneal, silicide anneals |
| `litho` | Coat/develop track + 193 nm immersion scanner | Every mask |
| `etch` | Plasma etch reactor | STI, gate, spacers, recess, contacts, damascene |
| `wet` | Wet bench / single-wafer wet | HF, SPM, hot H₃PO₄, Σ-recess wet etch |
| `implant` | Beamline ion implanter | Wells, Vt, halo, extensions, NMOS S/D |
| `cvd` | Single-wafer CVD (HDP, SACVD, PECVD, W-CVD variants) | STI fill, CESL, ILDs, W |
| `epi` | Lamp-heated RP-CVD epitaxy | SiGe:B |
| `pvd` | Magnetron sputter | NiPt, Ti/TiN, TaN/Ta, Cu seed |
| `ald` | Atomic layer deposition | HfO₂, TiN, TaN |
| `cmp` | Chemical-mechanical polisher | STI, ILD0, RMG, W, Cu |
| `ecd` | Electroplating | Cu fill |

### 8.2 Presentation

- An inset tool panel shows the step's tool as a cutaway, with the active region highlighted and a process animation.
- The first time each tool appears, the user gets a guided tour of 4–6 labeled components. Later uses skip the tour.
- A Tools index page lists all 12.

### 8.3 Lithography

- **Full walkthrough once, at the STI mask:** coat, soft bake, exposure (reticle, immersion, printing below the wavelength), post-exposure bake, develop.
- **Every later mask is two geometry steps:** "resist patterned" (`details` names the mask and its purpose) and "resist strip."
- Resist and BARC are modeled together as one `photoresist` layer; BARC is mentioned in the tour text. The gate nitride hard mask *is* modeled, because G4 needs it.

## 9. Non-goals (v1)

- No electrical simulation (no TCAD, no computed I-V). The final step explains switching qualitatively, with a transfer curve labeled illustrative.
- Doping is illustrative: computed from sourced implant and anneal parameters with simple models (Gaussian implants, √(Dt) broadening), not calibrated.
- One device flavor: core-Vt NMOS and PMOS only. A note explains that real chips also carry multiple Vt flavors and thick-oxide I/O devices.
- No crystal growth, wafer making, dicing, packaging, test, or yield/economics. Crystal growth and wafer making get one intro paragraph.
- No parameter tweaking or "what if" mode.
- No SRAM, passives, or fuses, and nothing above M2.

## 10. FinFET epilogue

- About 5 simplified geometry states from the same pipeline: fin patterning (spacer-based double patterning as text), STI recess revealing the fins, dummy gate wrap, merged diamond-shaped S/D epi, and RMG on three sides.
- A side-by-side comparison with the planar cell.
- One static gate-all-around nanosheet state as the closing view. UTB-SOI gets a text note.
- Production facts (who ships GAA at which node) are sourced when the epilogue is written, since they change.

## 11. Milestones

- **M0 (done).** Repo, smoke test (Python → `.glb` → R3F viewer), GitHub Pages deploy.
- **M1: STI vertical slice.** Done means all of the following:
  - every `wafer` + `sti` step is in `steps.yaml` with all three text tiers, sourced params, and confidence flags
  - pipeline geometry plus delta meshes for every geometry step
  - doping hook in place (an empty field is fine at this point)
  - tool panels for `furnace`, `litho` (full tour), `etch`, `wet`, `cvd`, and `cmp`
  - transitions, camera presets, and section cuts working
  - the palette tuning pass, logged in `DECISIONS.md`
  - fonts self-hosted
- **M2.** `well` + `gate`: first real doping textures.
- **M3.** `ldd` → `sd`.
- **M4.** `silicide` + `rmg`.
- **M5.** `contact` + `beol`.
- **M6.** `finfet` epilogue.
- **M7: launch review.** Second-source audit of every parameter, accessibility pass, and consider contacting Plummer & Griffin for permission or feedback.

## 12. Verify before writing the affected steps

Each item gets a source in `spec/sources.md`, or stays in the data with confidence `uncertain`.

- Dummy poly at cell edges as a 28 nm design rule.
- Poly-cut mask at 28 nm gate patterning.
- M1 single vs. dual damascene at 28 nm.
- Foundry 28 nm NMOS strain: CESL and SMT (G2).
- Σ-recess profile at 28 nm (G3).
- Silicide timing, pre-ILD0 vs. trench silicide, and the number of anneals (G4).
- High-k first vs. last at foundry 28 nm.
- Anneal method after the halo/extension implants.
- Real dimensions: Lg, CPP, cell height, STI depth, gate height, every film thickness.
- Real-scale well, punch-through, and Vt implant species, energies, and doses.
- Current GAA production facts for the epilogue.
