# Sources

Every source cited in `spec/steps.yaml`. Format and rules: `CONVENTIONS.md` (Sources).

- One entry per `### <BASEKEY>` heading. Keys are `<FirstAuthorSurname or Org><Year>`, plus a letter if needed (`Smith2009a`), with no hyphens.
- Required lines: **Citation**, **Type**, **Group**. Optional: **Link**, **Access**, **Notes**.
- **Type** is one of `paper`, `teardown`, `textbook`, `review`, `roadmap`, `vendor`, `patent`, `news`.
- **Group** marks independence. Sources from the same authors, the same company, or derived from one another share a group. A source can list several groups, comma-separated (for example a paper with authors from two organizations). A param marked `verified` needs at least two sources that share no group.
- For an edited handbook, cite each chapter as its own entry, since chapters have different authors. Keys use the chapter's first author.
- Not acceptable as sources: Wikipedia, forums, blogs without primary references, or AI output. Use them only to find primary sources.
- Never paste source text here. Summarize in your own words.

### PG2023
- **Citation:** J. D. Plummer and P. B. Griffin, *Integrated Circuit Fabrication: Science and Technology*, prepublication draft, Sept. 2023 (Cambridge University Press).
- **Type:** textbook
- **Group:** pg
- **Access:** Full personal-use prepublication PDF (Stanford website version, Sept. 2023), kept locally in `references/` and never committed.
- **Notes:** Running header gives the title above; a Ch. 2 footnote says "…Fabrication Processes: …". Use the published title once confirmed. Chapters read and key facts:
  - Ch. 2, Modern CMOS (pp. 34–58): the flow backbone. Known issues: "Si₂Cl₂" is a typo for SiH₂Cl₂ (p. 38); Si–O vs. Si–N bond strength reversed (p. 38); the simulation domain is vertically compressed (SCOPE.md G1). Wafer p-type (100), ≈10¹⁵ cm⁻³, ≈$100 per 300 mm (p. 37). LPCVD nitride from SiH₄ or SiH₂Cl₂ + NH₃ (p. 38). STI etch: nitride, oxide, then Si with resist still on, then resist strip (p. 39). Liner oxidation example ≈5 nm at 800 °C, 30 min, O₂ (p. 39). Nitride stripped in phosphoric acid after HF exposes it (p. 40). Trench taper 85° in the simulation figure only (Fig. 2.4).
  - Ch. 6, Interfaces (pp. 243–257): pad oxides 10–50 nm under nitride, LOCOS context; thermal oxides also passivate STI trench sidewalls (p. 243, Fig. 6.1). Trench sidewalls aligned to the notch on (100) wafers are (110) and oxidize faster than the (100) bottom; linear-rate coefficient for (110) ≈1.2× (100) by Eq. 6.20 (garbled in text extraction; check p. 256); oxidation rounds bottom corners, and stress retards growth there (p. 257, Fig. 6.13).
  - Ch. 9, Etching and CMP (pp. 413–453): hot phosphoric acid etches Si₃N₄ 4.5 nm/min, thermal SiO₂ 0.18, Si 0.17, so nitride:oxide ≈25:1; 100:1 HF ≈1 nm/min on native oxide (p. 413, Table 9.1). Fluorine chemistry gives a tapered profile, wanted to reduce stress at STI corners (p. 436). CMP moved from interlevel oxides to STI (p. 453).
  - Ch. 4 (p. 122): CMP slurry abrasives include silica, alumina, and ceria.
  - Not in the book: STI gap-fill method, nitride thickness, production trench angle.

### Natarajan2008
- **Citation:** S. Natarajan et al., "A 32nm Logic Technology Featuring 2nd-Generation High-k + Metal-Gate Transistors, Enhanced Channel Strain and 0.171µm² SRAM Cell Size in a 291Mb Array," IEDM Tech. Dig., 2008, p. 941. DOI: TODO.
- **Type:** paper
- **Group:** intel
- **Access:** IEEE Xplore (Dartmouth Libraries); personal copy in `references/`, never committed.
- **Notes:** Intel 32 nm, the anchor flow (SCOPE.md §3). CPP 112.5 nm (drawn 116, shrunk 3%); Lg 30 nm; 193i on critical layers; 9 Å EOT, dual band-edge metal gates, RMG; eSiGe PMOS (Fig. 2). Table 1: isolation 140 nm pitch / 200 nm thickness; gate row 35 nm thickness (meaning not stated); M1–M3 112.5 nm pitch, 95 nm thick; 9 Cu layers, low-k CDO on the first 7. Silent on high-k first vs. last.

### Packan2009
- **Citation:** P. Packan et al., "High Performance 32nm Logic Technology Featuring 2nd Generation High-k + Metal Gate Transistors," IEDM Tech. Dig., 2009, pp. TODO. DOI: TODO.
- **Type:** paper
- **Group:** intel
- **Access:** Freely available copy (record the URL here); personal copy in `references/`.
- **Notes:** Same technology as Natarajan2008 (shared authors), so same group. Adds raised NMOS S/D (Fig. 5) and PMOS SiGe moved closer to the channel; RMG lets stressors act before poly removal. Fig. 2 repeats the layer table (M9 pitch 19.4 µm). Fig. 4's 32/36 nm Lg devices illustrate a tradeoff, not the nominal Lg. Silent on high-k first vs. last.

### James2014
- **Citation:** D. James, "TSMC 20nm Arrives – The First Shoe Drops," Chipworks Real Chips blog, Solid State Technology, July 21, 2014.
- **Type:** teardown
- **Group:** chipworks
- **Link:** https://sst.semiconductor-digest.com/chipworks_real_chips_blog/2014/07/21/tsmc-20nm-arrives-the-first-shoe-drops/
- **Notes:** Physical analysis of production parts. Intel: high-k first at 45 nm, high-k last at 32 nm; raised NMOS S/D with stacking faults for tensile stress. TSMC: high-k first at 28 nm (28HPM image). Chipworks is now part of TechInsights; treat both as one group.

### Xiao2012
- **Citation:** H. Xiao, *Introduction to Semiconductor Manufacturing Technology*, 2nd ed. SPIE Press, 2012.
- **Type:** textbook
- **Group:** xiao
- **Access:** Knovel (Dartmouth Libraries). Chapter PDFs in `references/`, never committed.
- **Notes:** Generic flows; most values are typical, not tied to a node. Chapters read and key facts:
  - Ch. 4, Wafer Manufacturing (pp. 97–120): ⟨100⟩ for MOSFETs (p. 97). CZ is the only method for >200 mm; quartz crucible at 1415 °C; O and C impurities (pp. 103–104). Notch on ≥200 mm wafers (p. 105). 300 mm wafer is 775 µm thick (Table 4.2, p. 106). Edge rounding, lapping, etch, CMP finishing; backside gettering and backside oxide/nitride (pp. 107–108). Epi needed for high-performance CMOS and applied by the wafer maker, not the fab (p. 109). Selective epi for SiGe PMOS S/D (p. 116). Fig. 4.32 (p. 120) shows a generic 22 nm flow with SiC NMOS S/D, which does not match Intel 32 nm (see James2014).
  - Ch. 5, Thermal Processes (pp. 125–175): vertical furnaces standard; control, tube, gas, exhaust, and loading subsystems, plus vacuum for LPCVD; flat zone ±0.5 °C at 1000 °C; wafer tower raised and lowered slowly (pp. 126–128). Native oxide 10–20 Å (p. 130). Pad oxide ≈150 Å (range 100–200 Å) buffers LPCVD nitride stress of up to 10¹⁰ dyn/cm² (p. 132; Table 5.2, p. 136). STI barrier (liner) oxide 100–200 Å, blocks contamination from the CVD fill (p. 132; Fig. 5.9; Table 5.2). Screen oxide 100–200 Å; sacrificial <1000 Å; gate ≈15 Å by the mid-2000s (pp. 132–136). Thin oxides grown dry at ≈1000 °C with HCl (pp. 140, 149). Linear vs. diffusion-limited growth (p. 139). LPCVD nitride: SiH₂Cl₂ + NH₃ at 700–800 °C (p. 165), SiH₄ + NH₃ at ≈900 °C (p. 166); LPCVD preferred for STI nitride (p. 165); run sequence and NH₄Cl byproduct (p. 166). Spike anneal well under 1 s; laser/flash in ms (p. 174).
  - Ch. 6, Photolithography (pp. 179–235): sequence clean, prebake + HMDS, spin coat, soft bake, align/expose, PEB, develop, hard bake, inspection, in an integrated track + scanner (Fig. 6.7, p. 185). Prebake hot plate 150–200 °C, 1–2 min (p. 187); HMDS vapor prime (p. 188); spin ≈500 rpm dispense, up to 7000 rpm, generic resist 3,000–30,000 Å (p. 189); optical EBR (p. 192); soft bake on hot plate then chill plate, 10–20% shrink (p. 193); PEB 110–130 °C, ≈1 min, acid amplification (p. 202); TMAH spin develop (p. 203); hard bake 100–130 °C, 1–2 min (p. 205). Overlay tolerance 10–20% of CD; 1 °C shifts a 300 mm wafer ≈0.75 µm (pp. 180, 194). 4:1 reticles, step-and-scan (pp. 196–197); 193i scanner $30–40M (p. 197). Light sources g, i, KrF 248, ArF 193, F₂ dropped after immersion, EUV 13.5 nm (p. 201). Standing waves countered by BARC and PEB (pp. 201–202). Overlay, CD-SEM, scatterometry, and defect inspection before etch; rework only before etch/implant (pp. 206–210). Track anatomy and stacked modules (pp. 211–212). R = k₁λ/NA, DOF = k₂λ/(2NA²); planarization needed for DOF (pp. 213–215). AttPSM (MoSi, 6–20% T), AAPSM, OPC, off-axis/dipole illumination, SMO (pp. 217–221). Immersion: water n = 1.44 at 193 nm, R = k₁λ/(n·NA), DOF ≥1.46×, widely used 45–22 nm (pp. 221–222). Double patterning since 45 nm, widely at 32/22 nm (LFLE, LELE, SADP); gate CD ±10%, overlay ≈20% of CD (pp. 222–225). EUV uses mirrors and Mo/Si multilayer masks (p. 226).
  - Ch. 9, Etch (pp. 315–367): STI trench is plasma-etched; post-CMP nitride strip is a blanket etch (p. 317). Hot H₃PO₄ nitride strip: 180 °C, 91.5% → ≈100 Å/min, >10:1 to thermal oxide, >33:1 to Si; 200 °C, 94.5% → ≈200 Å/min, ≈5:1 and ≈20:1; HF unusable because it removes pad and STI oxide first; strip follows USG polish and anneal (p. 328). 10:1 HF strips native oxide before oxidation; 6:1 BOE and 100:1 DHF are standard (p. 326). Strips are pure chemical etches; oxide/nitride etch use the damaging mechanism, Si etch the blocking mechanism (pp. 331–336, Table 9.3). STI hard-mask etch: CF₄/CHF₃/C₂F₆/C₃F₈ or SF₆ with heavy ion bombardment and Ar; endpoint on CN, N, or O lines (pp. 342–343, 349). Si trench etch: oxide or oxide + nitride hard mask instead of resist to avoid contamination (pp. 334, 352); HBr main etchant, O₂ sidewall passivation, SiF₄/NF₃ for profile; F-based breakthrough then HBr/O₂ main etch; endpoint by time; post-etch wet clean (pp. 352–353). ICP for Si/poly/metal, CCP for dielectric in 300 mm fabs (p. 363); MERIE, E-chuck with backside He, wafer <150 °C (pp. 337–339); optical endpoint for main etch → overetch (p. 322). Gate etch: Cl₂ main, HBr secondary, trilayer hard mask + BARC, HBr/O₂ overetch; ≈12 Å gate oxide at 45 nm (pp. 355–357). Σ-cavity SiGe S/D by anisotropic wet Si etch, KOH example (p. 317, Fig. 9.16; production chemistry to verify). Ni strip in 1:1 SPM (p. 329); RMG dummy poly removed by wet etch (Fig. 9.5). Fin formation by trench, fill, CMP, STI recess (Fig. 9.42).
  - Ch. 10, CVD and Dielectric Thin Films (pp. 369–407): grown film consumes Si, deposited does not; gate oxide always grown (p. 369). APCVD O₃-TEOS widely used for STI and ILD0 (p. 374). LPCVD 0.1–1 torr, usually >650 °C, furnace-like with three zones and a vertical boat (Fig. 10.7, pp. 375–377); LPCVD nitride is the STI CMP hard stop (p. 376). Nitride uses silane, not TEOS (p. 387). HDP-CVD: simultaneous deposition and sputtering at a few mTorr (pp. 381–382). STI fill is USG by PE-TEOS, O₃-TEOS, HDP-CVD, or spin-on depending on geometry; void-free, dense, low shrinkage (p. 391, Fig. 10.28). Fill shrinkage during the high-temperature anneal can stress trench corners (p. 407). n(SiO₂) = 1.46, n(Si₃N₄) = 2.01 (p. 398); κ 3.9 vs. 7.0 (Table 10.3). ILD0 at ≤180 nm: PSG or USG with CMP, nitride barrier <100 Å (pp. 392–395).
  - Ch. 12, CMP (pp. 514–544): STI and ILD0 are the two dielectric CMP steps (pp. 514–516). STI CMP stops on nitride; oxide:nitride selectivity 3–100 (p. 529). Ceria slurry (≈5% CeO₂) gives better selectivity and less dishing than silica (p. 525, Fig. 12.26); silica slurry at pH 10–12 with KOH (p. 523). Dishing in wide STI regions (pp. 530–531). Removal rate several thousand Å/min; Preston equation (p. 528). Optical (spectroreflectometry) and motor-current endpoint (pp. 528, 538–539). PVA brush post-CMP clean (p. 540). Platen and pad, carrier with membrane, retaining ring, and pneumatic downforce, diamond pad conditioner, slurry dispenser (pp. 519–521). Gate-last needs poly-open CMP and metal CMP; dummy-gate removal increases channel strain (p. 544).
  - Ch. 13, Process Integration (pp. 549–562): ⟨100⟩ wafers, typical substrate doping 1×10¹⁵ cm⁻³, p-type more common for historical reasons (p. 550); advanced CMOS uses p-type wafers with p-epi (p. 551). Advanced STI flow (Fig. 13.7, p. 556): resist stripped after nitride/pad-oxide etch, Si etched with the nitride hard mask, liner oxide, HDP-CVD USG, CMP, anneal, wet strip of nitride and pad oxide. Pad oxide relieves nitride stress; nitride stripped in hot H₃PO₄ (pp. 552, 557). HDP oxide needs no anneal; O₃-TEOS needs >1000 °C in O₂ (pp. 555–556). No channel-stop implant at ≤1.8 V (p. 555). STI used as a stressor (p. 557).
  - Open conflicts: STI fill anneal is shown in Figs. 13.7 and 10.28 and on pp. 328 and 407, but p. 556 says HDP oxide needs none. Liner oxide 100–200 Å here vs. ≈5 nm in PG2023. P diffuses slower than B (p. 559) vs. nearly equal in PG2023.

### Pan1998
- **Citation:** J. T. Pan, D. Ouma, P. Li, D. Boning, F. Redeker, J. Chung, and J. Whitby, "Planarization and Integration of Shallow Trench Isolation," VLSI Multilevel Interconnection Conference (VMIC), Santa Clara, CA, June 1998.
- **Type:** paper
- **Group:** amat, boning
- **Link:** https://boning.mit.edu/wp-content/uploads/2022/11/Planarization-and-Integration-of-Shallow-Trench-Isolation.pdf
- **Notes:** Applied Materials + MIT; sub-0.25 µm era, so its numbers are historical, not 32 nm. Typical STI sequence (p. 1): pad oxide, LPCVD nitride, trench litho, trench etch, resist strip/clean, liner oxidation, CVD fill, CMP, post-CMP clean with light BHF dip, nitride strip, pad oxide strip, sacrificial oxide grow/strip, gate oxide. Nitride is the CMP stop, typically 170 nm then; its thickness is the budget for later lowering of the STI oxide surface, which should end at or slightly above the active Si to avoid gate wrap-around at the corner (p. 1, Table I itemizes recess, pattern effects, three wet etches, nitride loss, nonuniformity). Only HDP-CVD and O₃-TEOS (AP/SACVD) fill voids-free; SACVD is conformal, HDP gives a characteristic 45° faceted profile and self-planarizes over fine pitch (p. 3, Fig. 2). Standard slurry ≈4:1 oxide:nitride; high-selectivity slurries reported to 200:1 on blanket films, degrading at low active density (pp. 3–6).

### Cleavelin2007
- **Citation:** C. R. Cleavelin, L. Colombo, H. Niimi, S. Pas, and E. M. Vogel, "Oxidation and Gate Dielectrics," ch. 9 in Y. Nishi and R. Doering, eds., *Handbook of Semiconductor Manufacturing Technology*, 2nd ed. CRC Press, 2007 (confirm the copyright year on the title page).
- **Type:** textbook
- **Group:** cleavelin
- **Access:** Record the access route here (check Dartmouth Libraries for a CRCnetBASE / Taylor & Francis copy). Personal copy in `references/`, never committed.
- **Notes:** Cl (HCl and alternatives) is recommended for STI trench oxidation to neutralize metallic contamination (p. 9-5).

### Timans2007
- **Citation:** P. J. Timans, "Rapid Thermal Processing," ch. 11 in Y. Nishi and R. Doering, eds., *Handbook of Semiconductor Manufacturing Technology*, 2nd ed. CRC Press, 2007 (confirm the copyright year on the title page).
- **Type:** textbook
- **Group:** timans
- **Access:** Record the access route here (check Dartmouth Libraries for a CRCnetBASE / Taylor & Francis copy). Personal copy in `references/`, never committed.
- **Notes:** Table 11.1a (p. 11-2) lists pad oxide and STI liner oxide as RTP applications at 65–22 nm; the same table's 32 nm "FD-SOI" leading-technology row is a roadmap projection, not what shipped, so don't cite it. RTO gives more uniform trench liners with less crystal-orientation dependence and better corners; liner thickness varies at corners from stress and orientation (p. 11-76). Steam RTO improves STI corner rounding (p. 11-84).

### Xia2007
- **Citation:** L.-Q. Xia and M. Chang, "Chemical Vapor Deposition," ch. 13 in Y. Nishi and R. Doering, eds., *Handbook of Semiconductor Manufacturing Technology*, 2nd ed. CRC Press, 2007 (confirm the copyright year on the title page).
- **Type:** textbook
- **Group:** amat
- **Access:** Record the access route here (check Dartmouth Libraries for a CRCnetBASE / Taylor & Francis copy). Personal copy in `references/`, never committed.
- **Notes:** Authors at Applied Materials, so same group as Pan1998. HDP-CVD: SiH₄ + O₂ deposition with simultaneous Ar sputtering; HDP oxide qualified for STI without any post-deposition anneal; triangular top profile is its signature (p. 13-24, Fig. 13.10). Other CVD oxides normally need a post-deposition anneal in STI for etch resistance (p. 13-28). Pad oxide buffers Si/nitride thermal-mismatch stress; LPCVD nitride etches 10–15 Å/min vs. 900 Å/min for steam oxide in 6:1 BHF (p. 13-31).

### Shinn2007
- **Citation:** G. B. Shinn, V. Korthuis, G. Grover, S. Fang, and D. S. Boning, "Chemical–Mechanical Polishing," ch. 17 in Y. Nishi and R. Doering, eds., *Handbook of Semiconductor Manufacturing Technology*, 2nd ed. CRC Press, 2007 (confirm the copyright year on the title page).
- **Type:** textbook
- **Group:** boning
- **Access:** Record the access route here (check Dartmouth Libraries for a CRCnetBASE / Taylor & Francis copy). Personal copy in `references/`, never committed.
- **Notes:** Shares an author (Boning) with Pan1998. STI (p. 17-43): fill oxide deposited to slightly above the original Si level, then CMP stops on nitride, nitride removed in hot H₃PO₄; pattern-density effects; under-polish leaves nitride (device failure), over-polish dishes wide trenches; low-selectivity silica slurry erodes nitride in sparse regions; aids include reverse etch-back, dummy active fill, nitride cap layers; ceria under evaluation for selectivity but scratches more; blanket-wafer selectivity overstates patterned results.

### Ventzek2007
- **Citation:** P. L. G. Ventzek, S. Rauf, and T. Sparks, "Plasma Etch," ch. 21 in Y. Nishi and R. Doering, eds., *Handbook of Semiconductor Manufacturing Technology*, 2nd ed. CRC Press, 2007 (confirm the copyright year on the title page).
- **Type:** textbook
- **Group:** ventzek
- **Access:** Record the access route here (check Dartmouth Libraries for a CRCnetBASE / Taylor & Francis copy). Personal copy in `references/`, never committed.
- **Notes:** STI etch has two critical steps, nitride hard-mask patterning and Si etch (p. 21-18). Nitride etch as vertical as possible, e.g. CF₄/CHF₃ (p. 21-20). Si trench should have slightly sloped sidewalls (avoids seams in the CVD fill), rounded top corners (sharp corners raise leakage), and an oxidized bottom; the nitride must not be etched into the Si; uniform Si:nitride selectivity preserves CMP margin (p. 21-20). Example chemistry Cl₂–HBr–He–O₂ with SiOₓ sidewall deposition; more He–O₂ gives more taper (p. 21-20, citing Yeon & You, J. Vac. Sci. Technol. A 16, 1502, 1998). Taper vs. spacing: ≈66–80° over ≈0.1–10 µm spacing, open trenches more tapered, narrow ones more vertical (Fig. 21.11, p. 21-23, same source). No STI film thicknesses in Chs. 9, 11, 13, 17, or 21.

### Quirk2001
- **Citation:** M. Quirk and J. Serda, *Semiconductor Manufacturing Technology*. Prentice Hall, 2001.
- **Type:** textbook
- **Group:** quirk
- **Access:** Record the access route here (check Dartmouth Libraries). Personal copy in `references/`, never committed. The copy read was a scan without a text layer (OCR'd) and ends near book p. 493, so the CMP chapter (STI oxide polish, p. 535) was not read.
- **Notes:** Sub-0.25 µm era CMOS inverter flow. Ch. 4: 300 mm wafers 775 ± 20 µm (table from Huff et al. 1997, p. 76); "775 ± 25 µm" in text; notch and laser scribe (p. 82). Ch. 9 STI (pp. 207–210): ≈150 Å furnace-grown barrier (pad) oxide; LPCVD nitride from DCS + NH₃ at ≈750 °C as mask and CMP stop; STI litho; nitride, oxide, and Si etched with resist on, resist stripped after each etch; slanted profile and rounded bottom improve fill and isolation; ≈150 Å furnace liner oxide; fill by LPCVD furnace or other CVD (dated); CMP with nitride as the harder polish stop; post-CMP scrub; nitride strip in hot H₃PO₄. Flow drawn on p-epi over p⁺ substrate (Figs. 9.8–9.12). Ch. 10: STI liner 150–200 Å, passivates Si and blocks fill contamination (p. 238). Ch. 11: LPCVD nitride from DCS + NH₃ at 700–800 °C; nitride k ≈ 6.9 (p. 275). No nitride thickness given.

### Wolf2002
- **Citation:** S. Wolf, *Silicon Processing for the VLSI Era*, Vol. 4: *Deep-Submicron Process Technology*. Lattice Press, 2002.
- **Type:** textbook
- **Group:** wolf
- **Access:** Record the access route here (check Dartmouth Libraries). Personal copy in `references/`, never committed. The copy read was a scan of two-page spreads (OCR'd); Ch. 9 read.
- **Notes:** Ch. 9, STI (pp. 433–472); the §9.4 baseline is 0.25 µm era, with scaling trends in §9.5.
  - Baseline flow (pp. 446–455): RCA clean; pad oxide 10–20 nm (≈10 nm in STI vs. 25–40 nm for LOCOS, since STI has no field oxidation); LPCVD nitride 100–200 nm as trench hard mask and CMP stop, also deposited on the wafer back; nitride/pad-oxide plasma etch in a dielectric etcher; Si trench etch in a second etcher (HBr/Cl₂/O₂ or HBr/NF₃/He/O₂), blind and timed, sidewalls 70–85° with rounded bottom corners; resist strip; short HF dip to undercut the pad oxide, which improves top-corner rounding; liner oxide 40–50 nm in dry O₂ (best rounding with RTO at 1050–1100 °C, Fig. 9-13), which also converts a thin nitride skin to oxynitride; CVD fill (LPCVD TEOS, AP/SA O₃-TEOS, or HDP), 800–900 nm over a 500 nm trench; densify ≈900 °C to cut wet-etch rate ≈20%; optional reverse-mask etchback; CMP stopping on nitride; short HF to remove the oxynitride skin, then hot H₃PO₄ nitride strip (also removes backside nitride); pad oxide strip in HF; ≈20 nm sacrificial oxide; well, channel-stop, Vt, and punch-through implants through it; sacrificial oxide strip, partly to avoid a Kooi-like gate-oxide thinning; gate oxide.
  - Trends (pp. 449, 455–456): in-situ hard-mask-open single-etcher STI etch (resist on) in production by 2000 and more feasible as profiles steepen; slopes up to 88° for scaled trenches (Lam SEM shows 87°, Fig. 9-11); a 50 nm top-corner radius removes the I–V double hump for slopes ≤80° (p. 451); trench depth expected to fall below 0.2 µm near the 0.1 µm node (p. 456).
  - HDP-CVD (p. 460): sputter rate peaks about 45° from normal, producing 45° facets at trench tops and bottom-up fill.
  - p. 469 example stack (196 nm nitride, 15 nm liner) is an MIT test wafer, so it is not independent of Pan1998.
