# Sample Count and Temporal Stability — V4 validation

Date: 2026-10-30. Scene: `tools/blender_scene_proof.py`, 1080×1920, default shadow settings unless stated.

This document exists because the previous claim — *"8, 32 and 64 samples are visually identical"* — was based on mean luminance alone. Mean luminance is blind to noise, edge stipple and shadow grain. That claim is **withdrawn**.

---

## 1. Method

- Three renders of the identical scene at 8, 32 and 64 TAA samples, default shadow settings, 100 % resolution. Shadow settings were held constant so the sample count is the only variable.
- Five regions cropped and compared pairwise using ffmpeg's `psnr` and `ssim` filters. No new dependency; ffmpeg 8.1.1 was already installed.
- 64 samples is treated as the reference, not as ground truth.

| Region | Crop (w:h:x:y) | What it tests |
|---|---|---|
| card | 460:240:250:680 | Flat material, gradient, thin geometry detail |
| bevel | 460:260:60:1140 | Curved surface under soft shadow |
| rings | 340:260:380:880 | Emissive geometry, high contrast |
| floor | 380:380:620:1420 | Glossy reflection in shadow |
| bg | 320:320:40:120 | Smooth gradient, banding sensitivity |

Render times (default shadows): 8 spp **7.13 s**, 32 spp **15.67 s**, 64 spp **25.15 s**.

---

## 2. Results

SSIM ≥ 0.98 = converged. 0.95–0.98 = acceptable. < 0.95 = visible defect.

| Region | 8 vs 64 PSNR | 8 vs 64 SSIM | 32 vs 64 PSNR | 32 vs 64 SSIM | Verdict at 8 | Verdict at 32 |
|---|---:|---:|---:|---:|---|---|
| card | 54.10 | 0.9989 | 62.68 | 0.9997 | converged | converged |
| rings | 52.18 | 0.9983 | 58.88 | 0.9994 | converged | converged |
| background | 59.68 | 0.9988 | 63.55 | 0.9995 | converged | converged |
| bevel | 42.37 | 0.9689 | 50.60 | 0.9941 | acceptable | converged |
| **floor** | **29.32** | **0.7876** | 37.31 | **0.9292** | **fails** | **fails** |
| full frame | 37.80 | 0.9565 | 45.90 | 0.9878 | acceptable | converged |

### What the contact sheet shows

`tools/blender-test/contact_sheet.png` — left column 8 samples, right column 64 samples, rows in the order above.

- **Card, rings, background:** indistinguishable. The 8-sample renders are correct.
- **Bevel:** visible salt-and-pepper grain in the shadowed curve at 8 samples. Gone by 64.
- **Floor:** heavy stipple across the shadowed reflection at 8 samples; still visible at 32 by this metric. This is the single worst region in the frame.

### Shadow sampling is a different knob and helps only partly

8 samples with `shadow_ray_count=4`, `shadow_step_count=12`:

| Region | 8 spp default | 8 spp + shadow quality | Change |
|---|---:|---:|---|
| bevel | SSIM 0.9689 | **0.9844** | improves into range |
| floor | SSIM 0.7876 | 0.8447 | improves, still fails |

Cost: 7.13 s → 11.02 s (1.55×).

**The bevel noise is shadow sampling. The floor noise is glossy specular sampling and shadow settings do not fix it.**

### Conclusion on sample count

**Withdrawn:** "8 samples is visually identical to 64."

**Replaces it:** 8 samples is visually identical *for the card, the rings and the background*. It is not sufficient for soft-shadowed curved geometry, and it is materially wrong for a glossy reflective floor. A scene containing a glossy floor needs 64 samples to clear SSIM 0.98, which is 100 min per 10 seconds locally.

This converts a rendering question into an art-direction question: **a matte floor at 8 samples costs 28 min per 10 s; a glossy floor at 64 samples costs 100 min.** The choice belongs in the creative spec, not in the render settings.

---

## 3. Temporal stability

Three consecutive frames rendered from a **static** scene at 8 samples, same settings.

| Pair | PSNR | SSIM |
|---|---|---|
| frame 1 vs 2 | infinite (identical) | **1.000000** |
| frame 2 vs 3 | infinite (identical) | **1.000000** |
| frame 1 vs 3 | infinite (identical) | **1.000000** |

**Result: Eevee's TAA is deterministic here. Static frames are bit-identical. There is no Monte-Carlo flicker component.**

This is a materially good result. It means:
- Any difference between consecutive frames in an animation is **motion**, not sampling noise.
- A per-frame quality regression would be attributable to a scene change, not to randomness.
- Frame-level caching and resumable rendering are sound, because re-rendering frame N produces the same bytes.

**Caveat, stated honestly:** the test used a static scene. Grain that is frozen rather than flickering still looks like grain — determinism removes the strobe, not the noise. The floor defect from §2 is present on every frame identically.

---

## 4. Visual QA specification

Objective criteria a frame must satisfy before review. Each is computable from the render.

| ID | Criterion | Measure | Pass |
|---|---|---|---|
| QA-1 | Not black | mean luminance | in a scene-specific window, default [0.04, 0.40] |
| QA-2 | Has highlights | 99th-percentile luminance | ≥ 0.70 |
| QA-3 | Has shadow detail | 1st-percentile luminance | ≥ 0.002 |
| QA-4 | Subject framed | hero object bounding box inside the 9:16 safe area (top 12 %, bottom 20 % reserved) | 100 % inside |
| QA-5 | Object visibility | each named object ≥ 2,000 px above local background contrast | all pass |
| QA-6 | No interpenetration | manual check against the storyboard's physical model | signed off |
| QA-7 | Sampling converged | SSIM vs a 64-sample reference ≥ 0.98 **per region** | every region |
| QA-8 | Temporal continuity | static frames SSIM = 1.000; moving frames SSIM within the motion bound | met |
| QA-9 | Educational clarity | every claim in the script maps to a named visual element | human gate G3 |
| QA-10 | Safe text | no text below 42 px at 1080 width | automated |

QA-1..3 are implemented in `blender_scene_proof.py`. QA-7 is implemented by the method in §1. QA-4..6, 9, 10 are specified but **not implemented** — claiming otherwise would be false.

**QA-7 is the criterion that would have caught the withdrawn claim.** It compares regions, not the whole frame, because the whole-frame SSIM of 0.9565 averaged a converged card against a failing floor and landed in "acceptable".

---

## 5. Smallest useful local animation benchmark

The smallest test that exercises motion, determinism and encoding without being a heavy benchmark.

| Parameter | Value | Why |
|---|---|---|
| Frames | 24 (1 s @ 24 fps) | long enough to show motion and a transition |
| Resolution | 540×960 | half resolution; preview grade |
| Samples | 8 | the cheapest setting that is correct for everything except a glossy floor |
| Estimated render | **~108 s** | from `t ≈ 2.8 + 3.32 µs × px` at 8 samples |
| Encode | FFmpeg libx264 | already installed |
| Total | **under 3 minutes** | boundable in one foreground command |

This is the recommended CF-028. It answers: does the scene animate correctly, does the encoder produce a valid MP4, and is frame order stable.

---

## 6. Local Eevee viability — reassessed

| Use | Verdict | Basis |
|---|---|---|
| Hero still, 64 samples | **Viable** — 25 s | measured, gate PASS |
| Low-res preview, 108×192, 8 spp | **Viable** — 2.9 s | measured |
| 1 s preview clip, 540×960, 8 spp | **Viable** — ~2 min | estimated from the pixel model |
| 10 s production clip | **Not viable** — 28 to 310 min | measured range |
| Unattended overnight render | **Viable but marginal** — deterministic and resumable, but a 10 s shot is 0.5–5 h | temporal test + timings |
| Hero motion shot | **Not viable** | as above |

**Unchanged verdict for motion. New verdict for stills and previews: local is the correct tool.**

The practical split: author and light locally, proof every look locally as a still, preview motion at half resolution, render the final sequence remotely.

---

## 7. Reproducibility

Everything needed is in the repository and now tracked by git:

| File | Role |
|---|---|
| `tools/blender_scene_proof.py` | Scene, gate, frame-cost mode, GPU probe, shadow and animation switches |
| `tools/blender-test/sm8.png`, `sm32.png`, `sm64.png` | Sample-count evidence |
| `tools/blender-test/sh8.png` | 8 samples + shadow quality |
| `tools/blender-test/tmp_f0001..3.png` | Static-frame determinism evidence |
| `tools/blender-test/c_*.png` | Region crops |
| `tools/blender-test/contact_sheet.png` | Visual comparison |

Blender itself is gitignored (387 MB, reproducible from the official archive with a verified SHA-256). The scene script reads only environment variables and writes only into `tools/blender-test/`.

**Not committed:** `tools/blender-test/*.png` remains ignored. A hash manifest would let a fresh clone verify the claims; that is not yet written.

---

## 8. CF-028 result — first motion

Approved and executed 2026-10-30. 24 frames, 540×960, 8 TAA samples, raised shadow sampling, camera orbit at 1.5°/frame (34.5° total), encoded with FFmpeg libx264.

### Output

| Property | Value |
|---|---|
| File | `tools/blender-test/cf028.mp4` |
| Codec / size | h264, 136,429 bytes |
| Dimensions | 540 × 960 |
| Frames | 24 |
| Duration | 1.000 s @ 24 fps |

### Measured cost

| Metric | Value |
|---|---|
| Total wall clock | **74.6 s** |
| First frame | 4.07 s |
| Median frame | **2.42 s** |
| Setup | 1.65 s |
| **10 s at 540×960** | **582 s ≈ 9.7 min** |
| Estimate in §5 | ~108 s; **actual 74.6 s — estimate was 31 % conservative** |

**At half resolution a 10-second clip is ~9.7 minutes and fits the ≤15 min V4 budget.** It is preview grade, not production grade, but it is the first configuration measured to fit.

### Temporal stability — pass

| Metric | Value |
|---|---|
| Adjacent-frame SSIM, all 23 pairs | **0.9589 – 0.9718** |
| Mean | 0.9684 |
| Outliers | none; values rise monotonically then plateau |
| Dropped or duplicated frames | none |

Monotonic progression with a 0.013 spread across 23 pairs means every frame differs from its neighbour by a similar, small amount. **No flicker, no stutter, no frame-order defect.**

### Defect F1 — exposure drift, 32 %

Per-frame luma (YAVG, 16–235 scale) falls monotonically:

```
f01 69.61  f06 63.41  f12 55.80  f18 50.34  f24 47.35
```

Frame 24 is **32 % darker than frame 1**. The camera orbits out of the key light, so the visible surfaces receive progressively less. This is not flicker — it is a one-directional fade.

**Consequence:** the gate failed on frame 24 (`p99 = 0.6676 < 0.70`). The gate was right: the frame genuinely lost its highlights. A 1-second shot that dims by a third reads as an accidental fade.

**Root cause is scene construction, not renderer.** The lights are fixed in world space and the camera moves. Standard product-shot practice is a turntable where the lights rotate with the camera. The scene has no such rig.

### Defect F2 — the gold chip renders black

In frame 24 the chip is a black rectangle. Material is `metallic = 1.0`, and a pure metal has no diffuse component — it can only show what it reflects. At this camera angle nothing bright is in its reflection cone, so it returns near-zero.

Two fixes, both cheap: give the scene a low-intensity environment texture so metals have something to reflect, or reduce metallic to ~0.85 and raise roughness so some diffuse survives.

### What this changes

| Item | Before CF-028 | After |
|---|---|---|
| First motion produced | none | 1.0 s, 24 frames, encoded |
| Half-res 10 s clip | estimated viable | **measured 9.7 min, fits budget** |
| Temporal flicker | untested under motion | **tested — none** |
| Gate on sequences | assumed per-frame | **fails correctly on exposure drift; needs sequence semantics** |
| Metals | assumed correct | **fail in vacuum — no environment to reflect** |
| Lighting rig | static three-point | **must become camera-relative for any orbit** |

---

## 9. CF-030 / CF-031 — lighting candidates compared

Both candidates rendered from the identical camera path, resolution, sample count, colour management and output settings, driven by one script and one `place_orbit()` function. `CF_RIG=A|B` is the only difference.

| | Rig A — camera-relative | Rig B — fixed + gradient world |
|---|---|---|
| Lights | Three area lights parented to an empty rotated 1.5°/frame with the camera | Three area lights world-fixed |
| Environment | Near-black constant world, strength 0.20 | Procedural vertical gradient, strength 1.00 |
| `metallic` changed | **no** | **no** |

### Stills at 32 samples, three orbit positions

| Orbit | A mean | A p99 | A gate | B mean | B p99 | B gate |
|---:|---:|---:|---|---:|---:|---|
| 0 | 0.2468 | 0.7107 | PASS | 0.2768 | 0.7135 | PASS |
| 12 | 0.2402 | 0.7135 | PASS | 0.2145 | 0.6732 | FAIL |
| 24 | 0.2398 | 0.7135 | PASS | 0.1825 | 0.6724 | FAIL |
| **deviation from orbit 0** | **2.8 %** | | | **34.1 %** | | |

### 24-frame sequences at 540×960, 8 samples

| Metric | Rig A | Rig B | Target |
|---|---:|---:|---|
| `seq_max_deviation` | **3.55 %** | **33.50 %** | ≤ 5 % |
| `seq_drift` (first → last) | −3.13 % | −33.50 % | — |
| `seq_flicker_index` | **0.00043** | 0.00093 | ≤ 0.01 |
| luma first → last | 0.2470 → 0.2393 | 0.2770 → 0.1842 | — |
| last-frame gate | PASS | FAIL (p99 0.6724) | — |
| Per-frame render | 2.10 s | 2.09 s | no cost increase |
| 240 frames | 8.4 min | 8.4 min | — |

### Verdict

**Rig A passes. Rig B fails.**

- **Exposure:** A holds within 3.55 %, inside the ±5 % target. B loses a third of its light, matching the CF-028 defect it was meant to fix.
- **Flicker:** both are clean (0.00043 / 0.00093). Neither drifts because of temporal noise — B's problem is directional, not stochastic.
- **Chip:** legible and metallic at all six stills and across both sequences. **CF-031 is solved by both rigs, without touching `metallic`.**
- **Cost:** 2.10 s vs 2.09 s per frame. No penalty either way, so cost does not decide it.

### Why B failed

An environment adds a constant-ish term, not a proportional one. At orbit 0 it made the frame *brighter* (0.2770 vs A's 0.2470), which looked like progress, but the fixed key light still rotated away from the subject. Environment light compensated ~12 % and the key lost ~33 %.

The lesson is general: **ambient light cannot fix a directional problem.** It raises the floor; it does not stop the fall.

### Why A still drifts 3.55 %

The residual is *not* from the lights. Rotating a light about the Z axis through the origin leaves its distance to the target invariant (`x² + y²` unchanged, target at `x = y = 0`), so the key's contribution is exactly constant.

The residual comes from what does not rotate: the near-black world is fixed, and the floor's reflection is view-dependent. As the camera turns, a slightly different slice of floor and background enters the frame. Three and a half per cent is the cost of holding the world still.

### Artifacts

| File | Content |
|---|---|
| `rig_compare.png` | 6 panels — 2 rigs × 3 orbit positions |
| `chip_crops.png` | 6 chip crops at 2× — the CF-031 evidence |
| `motion_strip.png` | frames 1, 8, 16, 24 of both sequences side by side |
| `regions_compare.png` | card and terminal crops at orbit 24 |
| `cf030_A.mp4`, `cf030_B.mp4` | the two 1 s sequences |

### QA rule added

`SAMPLE_AND_TEMPORAL_QA.md` §4 QA-8 said "temporal continuity — SSIM within the motion bound". That was insufficient: SSIM measures difference, and a shot can change smoothly while still fading to black. Replaced by two independent measures computed in the scene script:

- **`seq_max_deviation`** — largest departure from frame 1, as a fraction of frame 1's luma. Catches drift in any direction.
- **`seq_flicker_index`** — mean absolute second difference of the luma series, normalised. A smooth ramp has near-zero curvature; flicker does not. This is what separates "the shot dimmed" from "the shot strobed".

Setting `CF_INTENTIONAL_DRIFT=1` reclassifies a drift failure as `INFO(intentional-drift)` rather than `FAIL`, so a scripted light move is distinguishable from an accidental one. Without the flag, drift beyond 5 % fails.

---

## 10. V4 cinematic scene and corrected QA system

`tools/blender_scene_v4.py` + `tools/cf_qa.py`. The Rig A baseline `blender_scene_proof.py` is untouched.

### 10.1 QA system changes

| Requirement | Implementation |
|---|---|
| `gate` no longer ambiguous | split into **`frame_gate`** (one frame, with `frame_gate_reason`) and **`seq_verdict`** (the sequence) |
| Region-specific temporal QA | `region_<name>_deviation`, `_flicker`, `_first`, `_last` for card, chip, terminal |
| Thresholds by shot type | `SHOT_THRESHOLDS` for `product_still`, `product_motion`, `diagram`; selected with `CF_SHOT` |
| Documented expected curve | `CF_EXPECTED_CURVE` → `seq_expected_curve_error`; without a curve, drift >5 % fails |
| Historical evidence preserved | `BLENDER_EEVEE_CORRECTION.md`, §2–§9, and every `.txt` report unchanged |

### 10.2 Scene changes

| Before (proof scene) | Now |
|---|---|
| Three floating torus rings | A four-sided antenna coil inset in the card, which energises |
| Constant 1.5°/frame orbit | Eased dolly-in, 55–70 mm |
| Flat gradient background | Emissive radial backdrop |
| Glossy floor dominating the lower third | Matte floor at roughness 0.55 |
| Card only | Card, chip, stripe, coil, terminal head, screen, NFC indicator, departing packet |

### 10.3 Measurements

| Item | Value |
|---|---|
| Stills, 1080×1920, 24–32 spp | 18.4 – 43.3 s each |
| Sequence, 24 frames, 540×960, 8 spp | median **2.73 s**/frame |
| 240 frames at that rate | **658 s ≈ 11.0 min** |
| `frame_gate` (final frame) | **PASS** — mean 0.2846, p99 0.9947 |
| `seq_max_deviation` | **10.95 %** |
| `seq_drift` | **+10.34 %** |
| `seq_flicker_index` | **0.00292** |

### 10.4 The QA did its job — and exposed a criterion that does not fit

`seq_verdict` = **FAIL**: whole-frame deviation 11 % > 5 %, and every region far worse (card 86 %, chip 80 %, terminal 102 %).

**Neither failure is an image defect.** Both are consequences of the shot type:

- **A dolly-in must brighten.** The camera moves from 0.53 m to 0.38 m, so the lit subject occupies more of the frame. A 10 % mean rise is the arithmetic of the move, not exposure drift. The ±5 % criterion was derived from CF-028's orbit, where framing was constant.
- **Fixed region rects are invalid under a dolly.** A rectangle sized around the card at frame 1 contains mostly background; by frame 24 it is full of card. The 86 % "deviation" measures the subject growing into the box, not a lighting change.

**This is the evidence item 1 was asking for.** "Make exposure thresholds configurable by shot type" needed a second shot type to exist before the thresholds could be set correctly. They still are not: a `dolly` shot type needs either an exposure measure invariant to subject scale, or region rects that track objects per frame.

Recorded as **CF-035**, open.

### 10.5 Visual defects found on inspection

| ID | Defect | Severity |
|---|---|---|
| V1 | **The packet passes through the card.** It starts at (0, 0.020, 0.050), inside the reader head, and its Bezier arc takes it straight through the card body around frame 12–14. | **High** |
| V2 | **The packet leaves frame at the end** — visible as a dot at the top-right corner of frame 24, then gone. The third beat is only half legible. | **High** |
| V3 | **Backdrop seam.** A hard horizontal edge crosses the upper third where the backdrop plane ends. | Medium |
| V4 | **The terminal reads as two stacked boxes**, not a card reader. The head needs a defined bezel and the screen needs to face camera. | Medium |
| V5 | The card is still untextured apart from chip, stripe and coil — no number block, no branding. | Medium |

**Creative verdict: not accepted.** The scene now has a story structure and the coil is accurate, but the payoff beat is physically broken (V1) and then invisible (V2). Fixing V1 and V2 is the entire difference between "a card hovering over a box" and "the request leaves".

### 10.6 Cost comparison against the Rig A baseline

| | Rig A baseline | V4 |
|---|---:|---:|
| Per frame, 540×960, 8 spp | 2.10 s | 2.73 s (+30 %) |
| Stills at 1080×1920 | 11.8–37.5 s | 18.4–43.3 s |

The 30 % is the backdrop emission and the additional objects. Against the target "no material increase without demonstrated visual benefit", the benefit is real — a graded background and a story — but the shot is not yet good enough to call it earned.

### 10.7 Artifacts

`v4_strip.png` (frames 1/8/16/24), `v4_cf033.mp4`, `v4d_beats.png`, and the per-run `.txt` reports. Earlier proof-scene evidence, including `contact_sheet.png` and `rig_compare.png`, is retained unchanged.
