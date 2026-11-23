# Sources

Every source cited in `spec/steps.yaml`. Format and rules: `CONVENTIONS.md` (Sources).

- One entry per `### <BASEKEY>` heading. Keys are `<FirstAuthorSurname or Org><Year>`, plus a letter if needed (`Smith2009a`), with no hyphens.
- Required lines: **Citation**, **Type**, **Group**. Optional: **Link**, **Access**, **Notes**.
- **Type** is one of `paper`, `teardown`, `textbook`, `review`, `roadmap`, `vendor`, `patent`, `news`.
- **Group** marks independence. Sources from the same authors, the same company, or derived from one another share a group. A param marked `verified` needs sources from at least two different groups.
- Not acceptable as sources: Wikipedia, forums, blogs without primary references, or AI output. Use them only to find primary sources.
- Never paste source text here. Summarize in your own words.

### PG2023
- **Citation:** J. D. Plummer and P. B. Griffin, *Integrated Circuit Fabrication: Science and Technology*, prepublication draft, Sept. 2023 (Cambridge University Press).
- **Type:** textbook
- **Group:** pg
- **Access:** Personal-use prepublication PDF, kept locally in `references/` and never committed.
- **Notes:** Ch. 2 is the flow backbone. Known issues: "Si₂Cl₂" typo for SiH₂Cl₂ (p. 38); Si–O vs. Si–N bond strength reversed (p. 38); the simulation domain is vertically compressed (see SCOPE.md G1). The running header and a footnote give slightly different titles; use the published title once confirmed.

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
