# Scope

What this site models, explains, and leaves out. Approved 2026-11-23. Any change goes through `DECISIONS.md` first.

## 1. Purpose

An interactive 3D site that shows how a 28 nm-class planar CMOS inverter is made, one process step at a time, alongside the tool that performs each step.

Accuracy is the top priority:
- Every process parameter is sourced.
- Uncertainty is flagged in the data, not just in prose.
- Places where the textbook flow differs from real fab practice are called out explicitly.

## 2. Audience, voice, and story mode

**Primary reader:** a curious non-specialist, a teenager or adult with no science or engineering background. Engagement comes first: every step should leave them with something exciting and true.

**Secondary readers:** students, process engineers, and reviewers (hiring managers, the textbook authors) who open the details to check rigor.

Every step carries three text tiers:

| Field | Reader | Length | Content |
|---|---|---|---|
| `summary` | everyone | one line, ≤ 20 words | A hook: what happens, said so it's interesting |
| `explanation` | everyone | 3–5 short sentences, ≤ ~80 words | What you're seeing, why it happens now, and one wow (scale, stakes, or what's temporary) |
| `details` | engineer | open-ended, collapsed by default | Technical terms, parameters, citations, `fab_reality`, metrology, the arithmetic behind any comparison |
| `physics` | student | optional, inside details ("Go deeper") | The governing model where a step has one: name, equation, a short explanation, and its source; constants are sourced params |

Each module also gets a one-line goal and a short intro in `spec/modules.yaml`, so the reader always knows what's being built and why.

Writing rules:
- Accuracy is not traded for excitement. Every analogy must be true, and every claim in the public tiers traces to a source (via `details`).
- The public tiers need no background. Technical vocabulary and acronyms live in `details`; STYLE.md §12 has the voice guide.
- All wording is original. Plummer & Griffin is paraphrased and cited, never copied.
- Explain ordering. The main thing Ch. 2 teaches is *why this step comes here*.

**Story mode.** About 70 steps is too many for a casual visit, so the site opens in story mode: roughly 20–25 steps marked `story: true`, chosen for being visual or pivotal. Skipped steps still happen: moving between story steps plays them as a quick labeled montage, so nothing is hidden. A toggle shows every step for completists. Navigation details are in STYLE.md §8.

## 3. Reference flow

The model is **anchored to Intel's 32 nm flow**: gate-last HKMG with high-k last, eSiGe PMOS, and raised NMOS source/drains. The site still describes itself as "28 nm-class."

- Intel 32 nm is the best-documented flow of this generation (IEDM papers plus independent teardowns), and it is the flow Plummer & Griffin Ch. 2 describes.
- Foundry 28 nm differences go in `fab_reality` notes. For example, TSMC 28 nm put the high-k down first, and its 28HPL variant had no eSiGe.
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
- The cell is 225 × 1125 nm (2 CPP × 10 M1 tracks) and the model is 3 CPP wide (337.5 nm), so both dummy gates sit fully inside. Shapes live in `masks/inverter.yaml`, checked by `pipeline/mask_check.py`.
- Vertical geometry is true scale (correction G1).
- The substrate is truncated below the well junction plus a margin. The bottom face gets a break marker and a note that the wafer continues to about 775 µm thick.

**BEOL:** W contacts, M1, then V1 + M2. A final stylized zoom-out says that roughly 8–12 more levels follow, without modeling them. Whether M1 is single or dual damascene still needs verifying (§12).

Coordinates, units, and naming follow `CONVENTIONS.md`.

## 5. Module order

This is an outline only. Parameters, sources, and exact step lists belong in `spec/steps.yaml`. Lithography appears as two steps per mask (§8), except for the full tour at the STI mask.

| Module | Main steps |
|---|---|
| `wafer` | Starting substrate: bare p-type (100), ~10¹⁵ cm⁻³ (epi wafers as a `fab_reality` note) |
| `sti` | Pad oxide (≈15 nm) · LPCVD nitride (≈100 nm, uncertain) · **full litho tour** · nitride/pad-oxide/Si etch with resist on (≈87° sidewalls) · resist strip · HF pad-oxide undercut · liner oxidation (RTP, ≈15 nm, rounds the top corner) · HDP gap fill · CMP stopping on nitride · post-CMP STI anneal · HF deglaze · nitride strip |
| `well` | Pad oxide strip · sacrificial (screen) oxide (≈20 nm) · N-well mask: deep well, punch-through, and Vt implants (P) · strip · P-well mask: same set (B) · strip · short anneal |
| `gate` | Screen oxide strip · dummy gate oxide · poly · nitride hard mask · gate mask (poly-cut mask?, §12) · gate etch · strip · reoxidation |
| `ldd` | Offset spacer deposition and etch · PMOS halo + extension implants · NMOS halo + extension implants · anneal (method to verify) |
| `spacer` | Main spacer deposition · anisotropic spacer etch |
| `sige` | Nitride hard mask · PMOS open · Σ recess · in-situ B-doped SiGe epi · hard mask strip |
| `sd` | NMOS raised S/D epi (material and order to verify) · NMOS deep S/D mask · implant · strip · activation anneal (spike/millisecond) |
| `silicide` | Pre-clean · NiPt deposition · first anneal · selective strip · second anneal (anneal count to verify) |
| `rmg` | ILD0 · CMP to poly-open · dummy poly removal · dummy oxide removal · interfacial oxide · HfO₂ · TiN cap · TaN etch stop · PMOS work-function TiN · NMOS open and TiN etch · Al work function + fill · CMP |
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
| G1 | Vertically compressed simulation domain: STI ~40 nm, 3–10 keV well implants | Real-scale depths: STI ≈ 200 nm (Intel 32 nm isolation thickness), retrograde wells below the STI | High that the textbook is compressed; STI depth single-source (IBM-alliance flows were deeper, ≈300 nm, Tilke2006) |
| G2 | NMOS strain from SiC:P epi | Raised NMOS S/D epi; strain from stacking faults and the RMG flow as text notes (not geometry). No stress liner unless a source shows one | Raised S/D verified; strain mechanism single-source |
| G3 | PMOS deep S/D implant, then recess + SiGe | Σ recess + in-situ B-doped SiGe right after the main spacer, before the NMOS deep S/D; no PMOS deep implant | Medium-high on order; Σ shape verified (James2010 TEM, Packan2009) |
| G4 | TiSi₂ at 350–450 °C with a TiN strip | NiPt-class silicide; poly protected by the gate nitride hard mask. Timing (before ILD0 vs. in contact trenches) follows Intel 32 nm once sourced | Uncertain, verify |
| G5 | One 10 nm spacer; extensions implanted against the bare gate | Thin offset spacer before halo/extension implants, then the main spacer | High |
| G6 | Well drive-in at 1000 °C for 10 min; separate well and Vt masks | One mask per well carrying deep-well, punch-through, and Vt implants, then a short anneal | High |

### 7.2 Text-only

- Intel 45 nm was high-k first, metal gate last; Intel moved to high-k last at 32 nm. TSMC 28 nm stayed high-k first.
- Embedded Si:C for NMOS reached production only at IBM 22 nm (2012), so the textbook's SiC:P NMOS step doesn't fit this generation.
- STI gap fill was HDP-CVD, SACVD (O₃-TEOS), or flowable CVD, not LPCVD SiH₄ + O₂. This changes the tool class but not the modeled shape. We model HDP; at 45 nm and below, high-aspect-ratio trenches moved to O₃/TEOS HARP fill (Tilke2006/2007).
- 45 nm-class STI liners were often oxide plus a thin nitride, or oxynitride, rather than pure oxide (Tilke2006).
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
- **Real photos:** each tool class gets one real photo behind a "See the real one" tap, with a person or object for scale. Every photo needs a license (Creative Commons, or written permission from the vendor or fab), recorded in `ATTRIBUTIONS.md`. A tool with no licensable photo ships without one.
- **Do the step:** on story steps, the viewer performs the action instead of pressing Next (hold to etch, drag the polishing pad, slide the wafer into the furnace). It drives the same scrubbable transition; nothing about the result changes. Parameter tweaking stays a non-goal (§9).

### 8.3 Lithography

- **Full walkthrough once, at the STI mask:** coat, soft bake, exposure (reticle, immersion, printing below the wavelength), post-exposure bake, develop.
- **Every later mask is two geometry steps:** "resist patterned" (`details` names the mask and its purpose) and "resist strip."
- Resist and BARC are modeled together as one `photoresist` layer; BARC is mentioned in the tour text. The gate nitride hard mask *is* modeled, because G4 needs it.

## 9. Non-goals (v1)

- No electrical simulation (no TCAD, no computed I-V). The switching finale (§11, M7) is an illustrative animation, labeled as such.
- Doping is illustrative: computed from sourced implant and anneal parameters with simple models (Gaussian implants, √(Dt) broadening), not calibrated.
- One device flavor: core-Vt NMOS and PMOS only. A note explains that real chips also carry multiple Vt flavors and thick-oxide I/O devices.
- No crystal growth, wafer making, dicing, packaging, test, or yield/economics. Crystal growth and wafer making get one intro paragraph.
- No parameter tweaking or open-ended "what if" mode. (A few curated, sourced failure cases are in the backlog, §13.)
- No SRAM, passives, or fuses, and nothing above M2.

## 10. FinFET epilogue

- About 5 simplified geometry states from the same pipeline: fin patterning (spacer-based double patterning as text), STI recess revealing the fins, dummy gate wrap, merged diamond-shaped S/D epi, and RMG on three sides.
- A side-by-side comparison with the planar cell.
- One static gate-all-around nanosheet state as the closing view. UTB-SOI gets a text note.
- Production facts (who ships GAA at which node) are sourced when the epilogue is written, since they change.

## 11. Milestones

- **M0 (done).** Repo, smoke test (Python → `.glb` → R3F viewer), GitHub Pages deploy.
- **M1: STI vertical slice.** Done means all of the following:
  - every `wafer` + `sti` step is in `steps.yaml` with all three text tiers (public voice for summary and explanation), sourced params, confidence flags, and `story` flags; both modules are in `spec/modules.yaml`
  - pipeline geometry plus delta meshes for every geometry step
  - doping hook in place (an empty field is fine at this point)
  - tool panels for `furnace`, `rtp`, `litho` (full tour), `etch`, `wet`, `cvd`, and `cmp`
  - transitions, camera presets, and section cuts working
  - the palette tuning pass, logged in `DECISIONS.md`
  - fonts self-hosted
- **M2.** `well` + `gate`: first real doping textures.
- **M3.** `ldd` → `sd`.
- **M4.** `silicide` + `rmg`.
- **M5.** `contact` + `beol`.
- **M6.** `finfet` epilogue.
- **M7: intro and finale.**
  - *Powers-of-ten intro:* a skippable zoom of about 15 s from a phone to its chip, the die, rows of standard cells, and the one inverter. Scale facts it shows are sourced.
  - *Switching finale:* the finished inverter is interactive. Flipping the input shows which transistor conducts (its channel glows) and the output node following, labeled illustrative.
- **M8: launch review.** Second-source audit of every parameter, accessibility pass, and consider contacting Plummer & Griffin for permission or feedback.

## 12. Verify before writing the affected steps

Each item gets a source in `spec/sources.md`, or stays in the data with confidence `uncertain`.

- Dummy poly and a poly-cut mask at Intel 32 nm (both confirmed for TSMC 28 nm by Chipworks2011).
- Intel 32 nm channel orientation (⟨110⟩ vs. rotated ⟨100⟩). It decides whether trench sidewalls are (110) and grow a thicker liner; until sourced, the liner is modeled uniform.
- M1 single vs. dual damascene at 28 nm.
- Intel 32 nm NMOS raised S/D: material, doping, and where it sits in the order (G2).
- Intel 32 nm silicide and contact scheme: timing and number of anneals (G4).
- A second, independent source for Intel 32 nm high-k last (currently Chipworks only).
- Independent measurements of Intel 32 nm CPP, Lg, and STI depth (currently Intel only).
- Anneal method after the halo/extension implants.
- Intel 32 nm contact scheme (square contacts vs. trench contacts); the masks use scaled square contacts until sourced.
- An Intel-specific source for cell height and device widths (currently Nangate2010 scaled, `uncertain`). The nitride thickness is still `uncertain` for 32 nm.
- Real-scale well, punch-through, and Vt implant species, energies, and doses.
- Current GAA production facts for the epilogue.

## 13. Backlog (after the first user test)

Held until the STI slice has been tried by 3–5 people with no technical background (see STATUS.md). Their reactions decide what gets built.

- **What goes wrong:** 3–5 hand-built, sourced failure cases shown beside the correct result (for example no pad oxide, over-polished STI, a misaligned mask).
- **Days in the fab:** a running indicator of time and step count, once sourced.
- **Share images:** a preview image per step for links pasted into messages and social media.
