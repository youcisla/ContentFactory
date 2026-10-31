# Lens probe — depth of field and motion blur, 2026-10-31

Purpose: prove that the two cheapest camera-language levers render headless on this host, measure their cost, and find a usable aperture at tabletop subject distance before any V5 asset work is authorised.

Environment: Blender 5.2.3 LTS, `BLENDER_EEVEE`, Intel OpenGL 4.6. Scene `tools/blender_scene_v4.py`, still frame 150, 1080×1920, 32 TAA samples. The probe is opt-in (`CF_LENS_PROBE=1`); with it unset, the baseline render path is unchanged.

## Results

| Run | Settings | Render | Delta |
|---|---|---:|---:|
| Baseline | no DOF, no blur, look `None` | **14.83 s** | — |
| A | DOF f/2.8, 180° blur (0.5), AgX Medium High Contrast | **21.46 s** | **+45 %** |
| B | DOF f/5.6, 180° blur | **21.91 s** | +48 % |
| C | DOF f/5.6, no blur | **17.42 s** | +17 % |
| D | DOF f/16, no blur | **13.01 s** | −12 % (within run-to-run noise) |

Outputs: `tools/blender-test/v4base_f150.png`, `v5probe_f150.png`, `v5probe_f150_f56.png`, `v5probe_f150_f56_nomblur.png`, `v5probe_f150_f16_nomblur.png`.

## What the stills show

- **f/2.8 or f/5.6 with a 65 mm lens at ~0.35 m destroys legibility.** The whole frame — card, chip, screen and keypad — is soft. The terminal screen, which is the film's payoff, cannot be read.
- **f/16 restores baseline sharpness.** Depth of field at this distance is a few centimetres wide at best; there is no aperture in the middle that separates card from terminal while keeping both readable.
- **Motion blur dominates the cost.** DOF alone adds ~17 %; adding the 180° shutter takes it to ~45–48 %.
- The contrast look is applied in every probe run and does not change geometry or legibility.

## Finding

The common advice "shoot wide open for cinematic separation" does not transfer to a macro tabletop product shot. At this scale the subject-to-background distance is smaller than the depth of field itself, so a wide aperture blurs the whole set instead of separating a subject from a background.

Rules that follow, and are now in `docs/creative/PREMIUM_TREATMENT_V5.md` C2:

1. Aperture is chosen from a depth-of-field budget at the measured subject distance, not a fixed f-number.
2. Wide apertures are only used when the background is at least ~0.5 m behind the subject — which means the camera and set must be placed so the backdrop is distant, not a wall 10 cm behind the terminal.
3. For the S3 rack focus to work, the card and screen planes must each fall inside their own focus zone at the chosen aperture; otherwise the "focus pull" reads as a blur pull.

## What this does not prove

- Any claim about V5 visual quality. This is a five-still camera-mechanics test on V4 geometry, not the benchmark.
- Sequence behaviour. Motion blur across a moving sequence, focus pulls over time, and flicker were not measured here; the exposure and sequence gates were not run.
- GPU or driver stability over a long render.

## Addendum — CC0 HDRI world, same frame

| Run | Settings | Render |
|---|---|---:|
| E | `CF_ASSET_HDRI=assets/hdri/brown_photostudio_02_2k.hdr`, strength 0.3 | **26.81 s** |

The HDR parses and renders headless. Cost is +81 % over the 14.83 s procedural baseline and +25 % over the f/2.8 DOF + blur run. Visually the difference at this strength is subtle: the image gains softer, more varied highlights, but primitive geometry still reads as primitive. Environment is not a substitute for geometry or set dressing.
