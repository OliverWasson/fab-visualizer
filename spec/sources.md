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
