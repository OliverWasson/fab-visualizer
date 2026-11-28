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
- **Licenses: MIT for code, CC BY 4.0 for content** (docs, spec text, masks, generated models and doping data). Why: anyone, including courses, can reuse the material with credit, which is the point of an educational project. Third-party components keep their own licenses, recorded in `ATTRIBUTIONS.md`.
- **Reference PDFs are gitignored.** The Plummer & Griffin prepublication is for personal use only, so it must never be committed. Checked on 2026-11-23: no PDF has ever been in the repo's history.
- **"Verified" is countable.** Each source in `sources.md` has a Group (same authors, same company, or derived works share one). A `verified` param needs sources from 2+ different groups, and the checker fails it otherwise. Why: "two independent sources" was an honor-system claim.
- **Source types are ranked** (header of `sources.md`): papers and teardowns for what a node actually did, textbooks for physics and ordering, roadmaps only as labeled targets, patents never alone. Wikipedia, forums, and AI output are never sources.

## 2026-11-23: Reference flow anchored to Intel 32 nm
- **The model follows Intel 32 nm:** gate-last, high-k last, eSiGe PMOS, raised NMOS S/D. This *supersedes* "generic gate-last 28 nm foundry archetype" in the Scope entry. Why: the generic archetype matched no real flow. TSMC 28 nm was high-k first, and 28HPL had no eSiGe (James2014). Intel 32 nm is well documented (Natarajan2008, Packan2009, James2014) and is the flow the textbook describes.
- **G1 value:** STI ≈ 200 nm (Natarajan2008 Table 1), replacing the unsourced "250–350 nm."
- **G2 revised:** NMOS gets a raised S/D epi step; its strain (stacking faults, RMG) is a text note. The tensile CESL step is removed. *Supersedes* G2 in the Scope entry.
- **G4 reopened:** silicide timing follows Intel 32 nm once sourced; `uncertain` until then.

## 2026-11-23: STI module choices
- **Starting wafer is bare p-type (100), ~10¹⁵ cm⁻³.** Advanced CMOS usually starts on a p-epi wafer (Xiao2012 p. 551); that becomes a `fab_reality` note. Why: the epi layer is Si on Si and would look identical; no Intel-specific source yet.
- **STI resist is stripped after the nitride/pad-oxide etch, before the Si trench etch,** which uses the nitride as a hard mask (Xiao2012 Fig. 13.7). PG2023's order (etch all three, then strip) goes in `details` as an alternative. Marked `uncertain` until a third source settles it.
- **A fill densification anneal follows STI CMP,** as a `thermal` step flagged `uncertain`. Why: Xiao's STI flows include it (Figs. 13.7, 10.28; p. 407), but Xiao p. 556 says HDP oxide needs none.
- **A source can belong to several groups.** Independence means sharing no group. Edited handbooks are cited per chapter. Why: Pan1998 shares a company with one Doering & Nishi chapter and an author with another, and a single group per source couldn't express that.

## 2026-11-24: STI module, after sourcing
This *supersedes* "STI module choices" (2026-11-23) where they differ.
- **Resist stays on through the nitride, pad-oxide, and Si etch, then is stripped** (PG2023, Quirk2001; Wolf2002 reports in-situ hard-mask-open etching as the scaling trend). Xiao2012's hard-mask order goes in `details`.
- **A post-CMP STI anneal replaces the fill-densification anneal.** HDP needs no densification (Xia2007, Xiao2012 p. 556) but a post-CMP anneal is still used (Tilke2007, Xiao2012 Fig. 13.7). Temperature and time unsourced.
- **Liner oxidation runs in the `rtp` tool** (Timans2007, Wolf2002), ≈15 nm (Xiao2012, Quirk2001). Wolf's 0.25 µm-era 40–50 nm would not fit 32 nm trenches.
- **An HF pad-oxide undercut step is added before the liner,** for top-corner rounding (Wolf2002).
- **Values:** pad oxide ≈15 nm (verified), nitride ≈100 nm (`uncertain`; 100–200 nm at 0.25 µm per Wolf2002 and Pan1998), trench sidewall ≈87° (verified, Wolf2002 + Tilke2007), STI depth ≈200 nm (Natarajan2008), HDP fill with 45° facets (Pan1998, Wolf2002).
- **G3's Σ recess shape is verified** (James2010 TEM, Packan2009).
- **New source type `pdk`** for generic open design kits (FreePDK45, Nangate). They supply representative layout proportions where Intel publishes nothing, scaled to Intel 32 nm pitches, and can never verify a company-specific fact.

## 2026-11-24: Cell layout
- **The cell is Nangate2010's INV_X1 scaled to Intel 32 nm pitches:** x by the CPP ratio (112.5/190), y by the M1-track ratio (112.5/140), with Lg 30 nm from Natarajan2008. Why: FreePDK45's poly direction is deliberately conservative (NCSU2011), so a single scale factor would distort the cell; both vertical ratios agree (≈0.80–0.82). Cell 225 × 1125 nm; W_n ≈ 334 nm, W_p ≈ 506 nm.
- **Dummy poly at both cell edges, over STI,** at ±1 CPP (Chipworks2011, TSMC 28 nm), so the model is 3 CPP wide. Nangate has none.
- **Square contacts, two per S/D, scaled from Nangate.** Intel's contact scheme is unsourced.
- **One deviation from Nangate:** the input M1 pad is widened left so the input via shares the M2 track.
- **Masks are checked automatically** (`pipeline/mask_check.py`): cell = 2 CPP × tracks × M1 pitch; gate and dummies lg wide at 0 and ±CPP; contacts inside their active or poly and on the right M1 net; gate contact over STI; vias inside matching M1 and M2; no M1 or M2 shorts; wells split in the STI gap; params sourced.

## 2026-11-24: Engagement first
- **The primary reader is now a curious non-specialist,** not someone with engineering background. The summary and explanation tiers are written for them, in the voice in STYLE.md §12; rigor stays in `details`, collapsed by default. This *supersedes* the audience in the 2026-11-23 Scope entry. Why: the site should leave everyone with something exciting and true, while still holding up to an engineer.
- **Story mode is the default:** about 20–25 `story: true` steps, with skipped steps played as a labeled montage and an "Every step" toggle. Why: about 70 steps is too many for a casual visit, but hiding steps would break the honesty principle.
- **Module goals and intros live in `spec/modules.yaml`.**
- **Transition type `intro`** for the first step, replacing a placeholder.
- **Scale comparisons are allowed in the public tiers** when computed from a sourced value, with the arithmetic and the everyday reference value stated in `details`.

## 2026-11-24: Intro, finale, and Go deeper
- **Powers-of-ten intro and an interactive switching finale** move into scope as milestone M7; the launch review becomes M8. The finale is illustrative, so the no-electrical-simulation non-goal stands. Why: they bookend the experience for a general audience.
- **Optional `physics` entries per step** ("Go deeper"): the governing model, its equation, a student-level explanation, and a source, with constants as sourced params. Why: it's what makes the site useful to engineering students, at low cost per step.

## 2026-11-24: Interaction, tool photos, and backlog
- **"Do the step" gestures on story steps** (hold to etch, drag to polish) drive the existing transitions. Why: doing beats watching, at almost no extra cost. **Parameter tweaking stays out:** accurate consequences would need process simulation, and anything simpler would be cartoon physics.
- **One real, licensed photo per tool class,** behind a "See the real one" tap. Why: the gap between schematic and reality (a box the size of a bus) is itself a wow moment. Each photo needs a license recorded in ATTRIBUTIONS.md.
- **Backlog until after the first user test** (SCOPE.md §13): curated "what goes wrong" cases, a days-in-the-fab indicator, share images. Why: build M1 and test it with non-technical people before adding more.

## 2026-11-24: STI lithography walkthrough and review fixes
- **The STI litho tour is five steps:** resist coat (`geometry`), soft bake (`thermal`), exposure (story step), post-exposure bake (`thermal`), and development (`geometry`). Later masks stay at two steps. This *supersedes* a single litho step for the tour. Why: it is the one place the site teaches lithography, and each operation changes something different.
- **New step kind `exposure`.** It emits no `.glb`, must use transition `litho_expose`, and needs `wavelength` and `dose` params; the checker enforces this, and geometry steps can no longer use `litho_expose`. Why: exposure changes the resist's chemistry, not its shape, so none of the four kinds fit.
- **No hard-bake step.** Both sources end the sequence with one (Xiao2012 p. 205, PG2023 Fig. 5.30); the development step describes it. Why: it keeps the walkthrough to the five operations in SCOPE.md §8.3.
- **Resist and BARC thickness go on the verify list** (SCOPE.md §12), since Xiao2012 Ch. 6 has no 193 nm value. The model uses 100 nm, the bottom of PG2023's generic 0.1–0.5 µm (p. 186), as `uncertain`. The soft-bake time and the hot-plate ambient of both bakes are `uncertain` too.
- **HBr vs. fluorine trench etch** is a text-only correction (SCOPE.md §7.2) and the trench etch's `fab_reality` note.
- **The textbook's ≈28–30 nm printed STI feature is not used.** Ch. 2's figures come from a compressed simulation domain (G1), so its dimensions aren't real-node values.
- **Rounded trench bottom corners are re-cited** to Wolf2002 p. 447 and Quirk2001 p. 208 (still verified); Tilke2007 p. 61 covers only the sidewall angle.

## Open questions
- None at the architecture level. Open facts that still need sources are listed in SCOPE.md §12.
