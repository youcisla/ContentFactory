# V5 still benchmark — asset terminal vs primitive baseline

Date: 2026-10-31. Two stills at matched output settings, inspected as images.

## Setup

| Setting | Baseline (V4) | Candidate (V5 art A) |
|---|---|---|
| Scene | `tools/blender_scene_v4.py`, frame 6 (`product_still`) | `tools/shot_render.py -- shots/artA_premium_realistic.json` |
| Terminal | procedural primitives | CC0 asset `receipt-pos-terminal-cc0`, linked collection |
| Resolution / samples | 1080×1920 / 32 spp | 1080×1920 / 32 spp |
| Engine / view | Eevee, AgX Medium High Contrast | same |
| Environment | CC0 `brown_photostudio_02` HDRI at 0.3 | same HDRI at 0.25 |
| Lens | V4 fixed product camera | 85 mm, f/4, focused at the marker |
| Render seconds | **27.58** | **15.89** |
| Cache | none | content-addressed, hit = 0.90 s |

Both are 9:16 single frames of the same subject with the same educational purpose: show a card being read by a payment terminal.

## Measured (cf_qa.measure)

| Frame | mean | p95 | p99 | dark fraction | frame gate |
|---|---:|---:|---:|---:|---|
| Baseline V4 | 0.2645 | 0.5734 | 0.6477 | 0.0000 | **FAIL** — p99 below 0.7, no highlights |
| V5 art A | 0.2198 | 0.6084 | 0.8065 | 0.0000 | **PASS** |
| V5 art B (stylised) | 0.1940 | 0.6064 | 0.6938 | 0.2162 | FAIL — low-key by design; gate is tuned for product shots |
| t01 macro | 0.2628 | 0.7521 | 0.8182 | 0.0000 | PASS |
| t02 interaction | 0.2371 | 0.5457 | 0.7683 | 0.0000 | PASS |
| t03 reveal | 0.2401 | 0.6353 | 0.7403 | 0.0000 | PASS |

Metrics are recorded as facts, not as the verdict. The verdict below comes from looking at the images.

## Visual evidence

- `render/comparison/baseline_artA_artB.png` — three panels, 540 px each: baseline, art A, art B.
- `render/comparison/mobile_360x640.png` — art A at phone scale.
- `render/comparison/crop_screen_baseline.png`, `crop_screen_artA.png` — display detail crops.
- `render/stills/artA_premium_realistic.png`, `artB_premium_stylized.png`, `t01…t03`.

## Assessment

| Dimension | Baseline | Asset-driven | Note |
|---|---|---|---|
| Silhouette | Cartoon wedge; card floats separately | Real terminal profile: tilted head, keypad recess, card slot | The asset carries the silhouette; no modelling time spent |
| Material realism | One grey plastic; metals read as paint | Four distinct finishes: matte polymer, powdercoat, coated glass, satin enamel | The only adaptation applied — the GLB shipped flat 0.8 grey |
| Lighting | Flat ambient, no highlight control | Key/fill/rim with measured powers; specular on the bezel; contact shadow under the body | Baseline still fails the exposure gate |
| Composition | Card dominates and hides the screen | 85 mm product framing, screen legible, foreground falloff | DOF now works because the subject has depth |
| Visual depth | None — everything at one distance | Counter, subject, 3 m backdrop, focus falloff | |
| Object recognisability | Ambiguous device | Reads immediately as a card payment terminal | |
| Educational usefulness | Screen shows a blank bar and a tick | Screen states amount and status; slot is visible in the interaction shot | |
| Render cost | 27.58 s/frame | 15.89 s/frame; 0.90 s cached | Faster because V4's animation/gates run more per-frame work |

**Verdict: the asset-driven still is visibly better and the improvement is attributable to the asset, not to grading.** The strongest single evidence is the display crop: the baseline screen is a flat bar; the candidate has a bezelled dark-glass panel with legible amount text. The weakest part of the candidate remains the missing human hand and set dressing — the shot is a clean product photograph, not a film frame.

## Art direction A/B

Two directions were rendered from the same asset and the same learning beat:

- **A — premium realistic** (`shots/artA_premium_realistic.json`): dark studio, HDRI 0.25, warm key, 85 mm f/4, shallow focus.
- **B — premium stylised** (`shots/artB_premium_stylized.json`): teal key/fill, hard 22 W rim, 50 mm f/8, graphic silhouette.

**A is selected for production.** B is visually stronger as a still but fails the product exposure gate by design, trades realism for style, and would need its own gate before sequences. It is retained as a variant, not as the default.

## Honest limits

- One still per direction, no sequence, no motion, no audio.
- No human or hand in frame; the card is a locally modelled stand-in, not an asset.
- The creative acceptance decision (is this good enough to publish?) remains the user's; nothing here grants it.
