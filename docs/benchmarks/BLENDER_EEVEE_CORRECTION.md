# Blender Eevee — Correction to CF-020

Date: 2026-10-30. Supersedes the **interpretation** in `BLENDER_EEVEE_RESULT.md`, not its measurements. That file is an immutable evidence record and is unchanged.

Trigger: the review stated that "one 1080×1920 frame took approximately 42.64 seconds and was nearly black. That is not a valid basis for a universal rendering-performance conclusion." This document tests that claim.

---

## 1. Why the frame was nearly black

Five defects, all in the scene, none in the hardware. Read from `tools/blender_evee_test.py`; no render was needed to identify them.

| # | Defect | Evidence |
|---|---|---|
| 1 | **Albedo near-black.** Card base colour `(0.035, 0.045, 0.06)` and floor `(0.02, 0.024, 0.032)` are linear values — 2–6 % reflectance. An 18 % grey card is the neutral reference. | `blender_evee_test.py:40-41` |
| 2 | **No ambient.** World background `(0.01, 0.012, 0.018)` at strength 1.0 contributes almost no fill. | `:72-73` |
| 3 | **Lights not aimed.** Key and fill use hand-written Euler angles instead of tracking the subject. An area light emits along −Z, so the values decide the aim; nothing verifies they point at the card. | `:58-68` |
| 4 | **AgX, never compensated.** Blender 5.x defaults to the AgX view transform. The script never sets `view_settings`, so sub-5 % albedo under a 1 % world is compressed into near-black. | absent from `:76-96` |
| 5 | **Framing overflow.** 50 mm at 2.44 m shows 0.99 m of width in a 9:16 frame; the card is 1.6 m wide. It was cropped. | `:48-50` + projection |

Defects 1–4 compound multiplicatively. Any one alone would darken the frame; together they produce a void.

**Not a cause:** GPU failure, driver fallback, or Eevee misconfiguration.

---

## 2. The GPU backend question is now closed

The original report recorded: *"If Blender is falling back to a software OpenGL renderer, a driver or session fix could change the number. Unverified."*

That is now measured. `gpu.platform` is uninitialised **before** the first render but valid **after** it, which is why the original probe failed.

| Query | Value |
|---|---|
| `renderer_get()` | `Intel(R) Graphics` |
| `vendor_get()` | `Intel` |
| `version_get()` | `4.6.0 - Build 32.0.101.8860` |
| `backend_type_get()` | `OPENGL` |

**Hardware OpenGL 4.6 on the Intel iGPU. No software fallback.** The 42.64 s was real GPU time, and no driver fix will change it. Risk of a large hidden speedup is now removed.

---

## 3. Corrected performance curve

Scene: `tools/blender_scene_proof.py` — 14 materials, emissive screen, emissive NFC rings, reflective floor, three area lights. Substantially more expensive than the CF-020 scene. Resolution 1080×1920 at 100 %.

### Sample count (default shadow settings)

| TAA samples | Render | Mean luminance | p99 | 240 frames |
|---:|---:|---:|---:|---:|
| 8 | **6.67 s** | 0.4533 | 0.999 | 26.7 min |
| 32 | **15.67 s** | 0.4534 | 0.999 | 62.7 min |
| 64 | **29.14 s** | 0.4534 | 0.999 | 116.6 min |

**The mean luminance is identical to four decimal places across 8, 32 and 64 samples.**

> **Correction, same day.** That sentence originally concluded "the extra 56 samples buy no observable image quality." **That conclusion is withdrawn.** Mean luminance is blind to noise. Region-level SSIM shows 8 samples failing badly on a glossy floor (0.788) while converging on the card, rings and background (≥ 0.998). Full evidence and the corrected per-region verdicts: [`SAMPLE_AND_TEMPORAL_QA.md`](SAMPLE_AND_TEMPORAL_QA.md). The *timings* above remain valid; only the quality conclusion changed.

Linear fit: `t ≈ 2.25 + 0.401 × samples` seconds.

### Shadow quality (same scene, 64 samples)

| Setting | Render | 240 frames |
|---|---:|---:|
| Default | 29.14 s | 1.94 h |
| `use_shadow_jitter`, `shadow_ray_count=4`, `shadow_step_count=12` | **77.41 s** | **5.16 h** |

Shadow sampling costs **2.7×** at identical resolution and sample count. This is the dominant quality knob, not TAA.

### Resolution (8 samples)

| Resolution | Megapixels | Render |
|---|---:|---:|
| 108 × 192 | 0.02 | 2.87 s |
| 1080 × 1920 | 2.07 | 6.67 s |
| 3888 × 6912 | 26.87 | 84.84 s |

Fit: `t ≈ 2.8 + 3.32 µs × pixels` at 8 samples. Fixed overhead ≈ 2.8 s.

---

## 4. What this changes

### The original extrapolation was approximately right

CF-020 extrapolated 240 × 42.64 s ≈ 170 min. A comparable-cost scene at 64 samples measures 29.1 s/frame → 117 min. Same order, same conclusion.

### But "11× over budget" was too harsh

| Configuration | 240 frames | vs V4 budget (≤15 min) |
|---|---:|---:|
| 8 samples, default shadows | 27 min | **1.8×** |
| 64 samples, default shadows | 117 min | 7.8× |
| 64 samples, high shadow quality | 310 min | 20.7× |

At the cheapest defensible setting, local misses the budget by **1.8×**, not 11×. The V4 budget was set before any measurement existed.

### The real constraint is shadow sampling, not samples

Anyone optimising this scene reaches for TAA first and buys nothing. The 2.7× is in `shadow_ray_count` / `shadow_step_count`.

### Verdict unchanged, reasoning replaced

Local Eevee animation is still **rejected** — every measured configuration exceeds the budget. But the reason is now "1.8–20× over, dominated by shadow sampling", not "11× over because the iGPU can't rasterise".

---

## 5. The scene now passes an objective exposure gate

`blender_scene_proof.py` measures the rendered frame after writing it:

| Metric | Value | Gate |
|---|---:|---|
| mean luminance | 0.2468 | must be in [0.040, 0.400] |
| p99 luminance | 0.7107 | must be ≥ 0.70 (real highlights present) |
| dark fraction (< 0.01) | 0.0447 | informational |
| Verdict | **PASS** | |

The gate caught two real regressions during development:
- After the rim light was reduced to remove a blown hotspot, `p99` fell to 0.6816 and the gate failed — the image had lost all specular highlights.
- Raising the shadow settings changed nothing about exposure, confirming the two knobs are independent.

**This is the acceptance test CF-020 lacked.** A frame is either inside the exposure window or the test is void. "Nearly black" is now a number the build fails on.

---

## 6. What is still unmeasured

- Cycles performance remains unmeasured (no supported CUDA/HIP device).
- Animation frames at 8 samples **with** high shadow quality: inferred at ~2.7× the 6.67 s figure (≈18 s, ≈72 min for 240 frames). Not directly measured.
- Whether any of this generalises to a second machine. One host only.
- Motion blur and depth of field costs are unmeasured; both would raise per-frame time.

---

## 7. Evidence files

| File | Content |
|---|---|
| `tools/blender_scene_proof.py` | Corrected scene, exposure gate, frame-cost mode, GPU probe |
| `tools/blender-test/proof_final.png` | Final 1080×1920 frame, 64 samples, gate PASS |
| `tools/blender-test/proof_final.txt` | Exact settings and measured metrics |
| `tools/blender-test/spp8.png`, `spp32.png`, `spp64.png` | Sample-count curve |
| `tools/blender-test/proof_v2.png` … `proof_v6.png` | Iteration record, including the failed compositions |
| `tools/blender-test/frame.png` | Unchanged CF-020 near-black original, preserved |

The iteration images are kept deliberately: the before/after shows what changed, and the failures are part of the evidence.
