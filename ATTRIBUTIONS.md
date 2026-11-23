# Attributions

Third-party components used by this project and their licenses. Licenses were
read from each package's installed metadata on 2026-11-23. Update this file
whenever a dependency is added, removed, or upgraded across a major version.

## Shipped in the website

These are bundled into the published site, so their notices travel with it.

| Package | License |
|---|---|
| three | MIT |
| react | MIT |
| react-dom | MIT |
| @react-three/fiber | MIT |
| @react-three/drei | MIT |

**Fonts (to be added in M1).** Oxanium, Atkinson Hyperlegible Next, and Kode Mono are all
distributed under the SIL Open Font License 1.1. When they are installed, add each
font's copyright line from its `OFL.txt` here, and ship the OFL text with the
font files, as the license requires.

**To do before launch (M7):** emit the full third-party license notices for the
bundled JavaScript with the build (for example with a Rollup license plugin), so
the deployed site carries them, not just this file.

## Used only to build the site

These run in the offline pipeline and are not distributed with the site.

| Package | License |
|---|---|
| manifold3d | Apache-2.0 |
| trimesh | MIT |
| shapely | BSD-3-Clause |
| numpy | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 |
| PyYAML | MIT |

Development tools (black, ESLint, TypeScript, Vite) are not distributed and are
not listed.

## References

Sources cited for process facts and parameters are listed in `spec/sources.md`.
Citing them does not imply endorsement by their authors.
