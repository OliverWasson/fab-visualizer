# Style

How the site looks, moves, and reads. Approved 2026-11-23. Any change goes through `DECISIONS.md` first. Hex values live in `spec/materials.yaml`, the single source that both the pipeline and the web app read.

## 1. Principles

1. **Schematic, not photoreal.** At 30 nm nothing has a visible "look," so rendering never pretends otherwise.
2. **Hue carries physical meaning, and only physical meaning.** Every hue on screen belongs to one of three families: material identity, dopant type, or process energy. The UI chrome is monochrome.
3. **The cell is the memorable part.** The 3D model and its transitions are where the boldness goes. Everything around them stays quiet.
4. **Honest about scale and modeling.** True scale is the default. Any exaggeration or illustrative model is labeled on screen whenever it's active.
5. **Never hue alone.** Every material can be identified by hover or tap, outlines, and labels as well as color.

## 2. Rendering

- **Materials:** `MeshStandardMaterial`. Dielectrics and silicon use roughness ~0.8 and metalness 0. Metals (`silicide`, `metal_*`, `tungsten`, `copper`) use metalness ~0.25 and roughness ~0.5, so they read as metal without visible reflections.
- **Lighting:** a hemisphere fill plus one key directional light. Soft contact shadows at most; no hard shadows.
- **Environment:** built from local drei `Lightformer`s only. No `Environment` presets, because those fetch HDRIs from a CDN.
- **Ambient occlusion:** N8AO (`@react-three/postprocessing`), with the radius tuned in nm during the STI slice.
- **Edges:** drei `<Edges>` on material boundaries, colored as the material darkened ~45%, so films thinner than a pixel still show a boundary.
- **Section caps:** stencil-capped, filled with the material color darkened ~15%, no hatching. The doping overlay is drawn on caps.
- **Ghost mode:** a toggle that renders chosen layers (resist, ILD, oxides) at 25% opacity with `depthWrite: false`. Everything is opaque by default.
- **Tool cutaways:**
  - hardware in neutral grays: shell `#C9CDD2`, cut faces `#B3B8BE`, fixtures `#8E959D`
  - the wafer in the material palette
  - only process elements (plasma, beam, gas, slurry, light) carry accent colors
- **Real tool photos:** shown only on request ("See the real one"), as an overlay on the tool inset with credit and license under it. Never recolored or edited beyond cropping.

## 3. Color

### 3.1 Materials

| Node | Hex | Material |
|---|---|---|
| `silicon` | `#B9B7AE` | Crystalline Si |
| `oxide_grown` | `#CFE0DA` | Grown SiO₂: pad, liner, gate, reoxidation, interfacial |
| `oxide_deposited` | `#ECE7DA` | Deposited SiO₂: STI fill, ILD0 |
| `nitride` | `#9AAE6B` | Si₃N₄: hard masks, spacers, CESL |
| `etchstop` | `#66784A` | SiCN Cu cap / etch stop |
| `photoresist` | `#F0CF62` | Resist (+ BARC) |
| `polysilicon` | `#8C8299` | Poly-Si dummy gate |
| `sige` | `#CDB384` | SiGe:B |
| `silicide` | `#4E4A55` | NiPt silicide |
| `highk` | `#1FA99A` | HfO₂ |
| `metal_tin` | `#B08A2A` | TiN |
| `metal_tan` | `#8A6E52` | TaN / Ta |
| `metal_al` | `#B4BDC9` | Al work-function metal + fill |
| `tungsten` | `#737D8A` | W plugs |
| `copper` | `#C4682F` | Cu |
| `lowk` | `#DCD3E8` | Low-k ILD |

Material colors are identical in light and dark themes. Materials that physically touch must differ clearly in lightness or hue. Re-check this whenever a material is added. **One tuning pass is allowed during the STI slice**, after which the palette is frozen. Log the pass in `DECISIONS.md`.

### 3.2 Doping (tints `silicon` and `sige` only)

Signed log net doping, 5-stop ramps from 10¹⁶ to ≥ 10²⁰ cm⁻³. Below 10¹⁶ the silicon stays untinted, and junctions show as the pale band where the sign flips.

| Type | 10¹⁶ | 10¹⁷ | 10¹⁸ | 10¹⁹ | ≥ 10²⁰ |
|---|---|---|---|---|---|
| N | `#D6E2F2` | `#A9C3E6` | `#6F9AD2` | `#3A6FB8` | `#1E4F96` |
| P | `#F4D9D6` | `#E8ADA8` | `#D7766E` | `#C0473F` | `#9A2A24` |

While the overlay is on, a legend and the badge "Doping: illustrative model" are always visible. No material may use a saturated blue or red.

### 3.3 Process-energy accents

These are emissive, animated, additive-blended, and never used on solid geometry.

| Accent | Hex | Used for |
|---|---|---|
| `plasma` | `#9B6BFF` | Etch and PECVD glow |
| `ion_beam` | `#33C3F0` | Implant streaks |
| `uv_exposure` | `#5B4BE0` | 193 nm exposure |
| `heat` | `#FF6B3D` | Thermal-step rim glow |
| `gas_flow` | `#E8E8E8` | Gas and slurry streaks (60% opacity) |

### 3.4 Scene and UI (monochrome)

| Token | Light | Dark |
|---|---|---|
| `scene-bg` | `#E9ECEF` | `#1B1D21` |
| `panel-bg` | `#F7F8F9` | `#141619` |
| `ink` | `#1B1D21` | `#ECEEF1` |
| `ink-2` (secondary) | `#4A4F57` | `#B4BAC2` |
| `ink-3` (muted, ≥ 4.5:1) | `#6B717A` | `#8A9099` |
| `border` | `#D3D7DC` | `#2E3238` |
| `border-strong` | `#A9AFB7` | `#4A5059` |

- Active and selected states use weight, underline, a fill contrast swap, or `border-strong`. Never a hue.
- Focus ring: 2 px `ink` with a 2 px offset.
- The theme follows `prefers-color-scheme`, with a manual toggle that's remembered per browser.

## 4. Typography

| Role | Typeface | Use |
|---|---|---|
| Display | **Oxanium** | Module names, step titles, step counter, 3D callouts, buttons, tool-tour labels. Short strings only (≤ ~6 words), never paragraphs |
| Body | **Atkinson Hyperlegible Next** | Summary, explanation, details prose, table text, tooltips |
| Data | **Kode Mono** | Parameter values, source keys, node names, the confidence column. Only inside tables and code, never as decorative small labels |

- **Scale:** 16 px base, ratio 1.25: 12.8 / 16 / 20 / 25 / 31.25 px.
  - step title: 25 px Oxanium 600
  - module line: 16 px Oxanium 500
  - body: 16/1.55 Atkinson 400
  - details: 14/1.5
  - table values: 13–14 px Kode Mono
- **Line length:** ≤ 70 characters (the ~380 px panel gives about 50–55).
- **Case:** sentence case everywhere. No all-caps labels, no tracked-out eyebrows above headings.
- **Step header:** module name on its own line ("Shallow trench isolation"), title below it ("Nitride deposition"), and "Step 3 of 11" as a separate element. No strings glued together with middle dots.
- **Loading:** self-hosted, no font CDN. Intended packages are `@fontsource-variable/oxanium`, `@fontsource-variable/kode-mono`, and Atkinson Hyperlegible Next. **Verify in M1** that each package exists and covers the glyphs we need. Otherwise self-host the OFL files under `web/public/fonts/` with `@font-face`.
- **Fallback stacks:** `Oxanium, "Segoe UI", system-ui, sans-serif`; `"Atkinson Hyperlegible Next", system-ui, sans-serif`; `"Kode Mono", ui-monospace, monospace`.

## 5. Notation

- A thin space (U+2009) between number and unit: `10 nm`, `1000 °C`, `30 s`, `15 keV`.
- Doses: `1×10¹³ cm⁻²`. Concentrations: `1×10¹⁸ cm⁻³`. Never `1e13` in displayed text (the yaml may use it).
- Formulas, subscripts, and exponents are written as HTML `<sub>`/`<sup>` from yaml markup (`Si<sub>3</sub>N<sub>4</sub>`), so rendering never depends on a font's Unicode coverage.
- Approximate values: `≈ 5 nm`. Ranges: an en dash with no spaces, `900–1200 °C`.
- Equations use KaTeX, loaded only when a Details section that contains one opens.
- Use the same name for a thing everywhere: if a button says "Show tool," the panel is titled "Tool."

## 6. Scale

- True scale (1×) by default. A toggle offers 1× / 2× / 4×. When not at 1×, a persistent badge reads "Vertical ×N."
- Exaggeration scales the scene root in `z` about `z = 0`. The doping shader samples unscaled coordinates.
- Thin films are made visible by camera framing (§8), not by stretching.
- A live scale bar (nm) and an axis triad are always shown.
- The substrate's bottom face gets a zig-zag break edge and the note "wafer continues, ≈ 775 µm."

## 7. Motion

Each step's `transition.type` selects an animator. The pipeline supplies the delta meshes (see `CONVENTIONS.md`).

| Type | Animation | Duration |
|---|---|---|
| `deposit_conformal` | `__added` morph collapses to the surface, weight 1 → 0 | 2.0 s |
| `deposit_directional` | Rising clip plane reveals `__added` | 2.0 s |
| `oxidize` | Oxide grows outward while consumed Si recedes (morphs on both) | 2.0 s |
| `etch_anisotropic` | Descending clip plane through `__removed`, plasma glow | 2.0 s |
| `etch_isotropic` | `__removed` shrinks along normals | 2.0 s |
| `cmp` | Descending plane, gas_flow slurry streaks | 2.5 s |
| `epi` | Faceted `__added` morph out of the recess | 2.5 s |
| `implant` | Ion streaks at the step's tilt and twist, stopping visibly in resist; doping fades in | 2.5 s |
| `thermal` | Heat rim glow, doping crossfade, thermal-budget readout | 2.0 s |
| `litho_expose` / `litho_develop` / `strip` | UV through the reticle pattern, then resist clears | 1.5 s each |

- Easing: ease-in-out cubic for growth and morphs; linear for clip sweeps.
- The camera flies before the transition starts.
- Every transition can be scrubbed and paused.
- **Do the step (story steps):** the viewer's gesture drives the transition's progress: press-and-hold for timed processes (etch, deposition, oxidation, implant), drag for CMP and wafer loading. Releasing early pauses; finishing advances. Keyboard: hold Space. A plain Next button is always available as well, and reduced motion uses it alone.
- **Reduced motion:** a 300 ms crossfade, no particles, and the camera jumps instead of flying.
- UI motion is limited to responses to the user's own actions (panel open, step change). No decorative entrance animations. The two orchestrated moments are the intro and the finale.
- **Intro (powers of ten):** about 15 s, skippable at any point, ending on the wafer step. A scale label (e.g. "1 cm", "10 µm", "100 nm") stays on screen throughout. Reduced motion: a sequence of stills with a Next button.
- **Finale (switching):** an input toggle (0/1). The conducting transistor's channel glows in the dopant color of its carriers, and the output node and wires shift between VDD and ground, over about 0.6 s. A persistent "Illustrative" badge, the same rule as doping.

## 8. Camera, section, navigation

- **Controls:** drei `CameraControls`, with distance limits (~20 nm to ~5 µm) and a polar limit so the camera can't wander under the wafer.
- **Presets:** `overview`, `pmos_x`, `nmos_x`, `gate_y`, `gate_edge`, or an explicit target and distance in `steps.yaml`.
- **Fly policy:** on step change, a 1.2 s ease-in-out flight to the step's framing. A "Keep my view" toggle suppresses this; "Reset view" returns to the step's framing.
- **Section plane:** presets `pmos_x`, `nmos_x`, `gate_y`, a `free` draggable plane, and `off`. Each step picks its default cut.
- **Navigation:** a module-segmented timeline, ←/→ keys, and deep links via hash routing (`#/step/<step-id>`). GitHub Pages has no SPA fallback for path routes.
- **Story mode (default):** the timeline shows only `story: true` steps. Advancing from one story step to the next plays the skipped steps in between as a montage, about 0.6 s each, with their titles shown, so every material change stays visible. A toggle ("Every step") reveals the full list. Deep links to a non-story step switch the toggle on. Under reduced motion the montage becomes a single crossfade with the skipped titles listed.
- **Module intro:** entering a module shows its goal line and intro from `spec/modules.yaml`, in both modes.

## 9. Layout

```
Desktop (≥ 768 px)
┌───────────────────────────────────────────┬──────────────────┐
│ scale bar · triad        cut · toggles    │ Module name      │
│                                           │ Step title       │
│                 3D cell                   │ Step 3 of 11     │
│                                           │ summary          │
│ badges: Vertical ×N / Doping: illustrative│ explanation      │
│                                           │ ▸ Details        │
│                                           ├──────────────────┤
│                                           │ Tool inset       │
├───────────────────────────────────────────┴──────────────────┤
│ timeline segmented by module   ◀ ▶  ⏯  transition scrubber   │
└──────────────────────────────────────────────────────────────┘

Mobile (< 768 px)
┌──────────────────────┐
│ 3D cell (~55 vh)     │
├──────────────────────┤
│ sheet: Step | Details│
│        | Tool        │
├──────────────────────┤
│ module chip · dots   │
└──────────────────────┘
```

- The canvas takes ~65–70% of the width on desktop; the panel is ~380 px; text is left-aligned.
- The main scene and the tool inset share **one `<Canvas>`** through drei `<View>`, to save GPU memory and stay within iOS Safari's WebGL context limits.

## 10. Labels

- **Hover/tap:** a tooltip with the full name, for example "TiN (titanium nitride)." It works on every mesh and every section cap.
- **Callouts:** at most 3 per step, from `steps.yaml`. Each is anchored to an `anchor__<name>` node exported by the pipeline and drawn as a 1 px `ink-2` leader with Oxanium 13 px text. When callouts overlap, the lower-priority one hides.
- **Tool tours:** numbered callouts are allowed here, because the tour is a real sequence.

## 11. Accessibility

- WCAG AA contrast for all text.
- Full keyboard navigation with a visible focus ring.
- The canvas `aria-label` is the current step's `summary`.
- Doping and materials are never identified by hue alone (§1.5).
- `prefers-reduced-motion` is honored (§7).

## 12. Voice

How the public tiers (`summary`, `explanation`, module goals and intros) are written. The details tier keeps a precise technical register.

- **Write for a curious reader with no science background.** No acronyms or jargon; if a term is unavoidable, say what it is in the same breath ("silicon dioxide, the same compound as glass").
- **Lead with something interesting.** The summary is a hook, not a label.
- **Each explanation answers three questions:** What am I looking at? Why does it happen now? What's the wow? The wow is one of: scale, stakes ("if this cracks, the chip is dead"), or temporary versus permanent ("this layer is scaffolding").
- **Short sentences, active voice, present tense.** One idea per sentence.
- **Excitement comes from facts, not adjectives.** No hype words (amazing, incredible, revolutionary) and no exclamation marks.
- **Comparisons must be true.** A scale comparison computed from a sourced value is allowed when `details` states the arithmetic and the everyday reference value used (for example, a hair width of ≈90 µm).
- **Repeat the throughline:** most early layers are temporary scaffolding. Say so when one appears and when it's removed.
- **Developer notes never go in reader text.** Implementation notes belong in YAML comments.
- **"Go deeper" (`physics`) is written for an engineering student:** name the model, give the equation, say in two or three sentences what each term means physically and when the model holds, and cite it. Equations render with KaTeX.
