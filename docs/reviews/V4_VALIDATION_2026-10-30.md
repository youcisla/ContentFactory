# V4 Validation — scorecard and adversarial review

Date: 2026-10-30. Follows `REMEDIATION_REVIEW_2026-10-30.md`. This round added measured evidence and withdrew one claim.

---

## 1. Scorecard

| Dimension | Previous | Now | Evidence | What 5/5 still requires |
|---|---:|---:|---|---|
| Engineering process | 4 | **4.5** | Determinism test added (static frames SSIM 1.000000); region-level QA criterion QA-7 added; contact sheet artifact | CI running the gates; a build that fails on regression |
| Tool discovery | 4 | **4** | Unchanged — no new tools were needed; ffmpeg's own PSNR/SSIM avoided a dependency | Hands-on trial of a remote option |
| Hardware understanding | 4 | **4.5** | Per-region sample convergence, shadow-vs-TAA separation, temporal determinism, GPU backend named | Motion-blur and DOF costs; sustained/thermal behaviour; Cycles |
| Architecture validation | 3.5 | **3.5** | ADR-0001/0002 amended with measured data, statuses preserved as `proposed` | Two architectures compared on the same storyboard with measurements |
| Documentation consistency | 3.5 | **4** | Wrong claim withdrawn with an inline correction and pointer; ADR amendments preserve original text; BACKLOG gains CF-028/029 | The 10 unaudited files; machine-checked cross-links |
| Visual quality | 3 | **3** | `proof_final.png` passes QA-1..3; now known to be *noisy in two regions* at low samples | Rings still read as hoops; no contact shadow; no motion; no creative approval |
| Production readiness | 1.5 | **1.5** | One scene script and one gate | Any episode rendered end-to-end |

**Visual quality does not improve despite a full measurement round.** The measurements found a defect, they did not fix one. That is the honest reading.

---

## 2. Adversarial findings, scored on observable evidence

| ID | Finding | Evidence | Severity | Status |
|---|---|---|---|---|
| A1 | **A wrong claim was written into a document as "measured, not a preference".** "The extra 56 samples buy no observable image quality" was based on mean luminance alone. | Floor SSIM 0.7876 at 8 samples; visible stipple in `contact_sheet.png` row 4 | **High** | **Fixed** — withdrawn inline in `BLENDER_EEVEE_CORRECTION.md` with a pointer to the correcting document |
| A2 | **Whole-frame metrics hid a failing region.** Full-frame SSIM 0.9565 read as "acceptable" while one region sat at 0.788. | Per-region table, §2 of the QA document | **High** | **Fixed** — QA-7 requires per-region convergence |
| A3 | **The floor defect has no fix.** Raising shadow sampling moved it from 0.788 to 0.845 — still failing. The cause is glossy specular sampling. | 8spp+shadow comparison | **High** | **Open** — options are matte floor (art change) or 64 samples (4× cost) |
| A4 | **Temporal test used a static scene.** It proves determinism, not the absence of flicker under motion. | Method, §3 | Medium | **Open** — needs a moving sequence |
| A5 | **Evidence images are gitignored.** The claims are reproducible from the script, but the artifacts themselves are not verifiable from a clone. | `tools/.gitignore` | Medium | **Open** — needs a hash manifest |
| A6 | **QA-4, QA-5, QA-6, QA-9, QA-10 are specified, not implemented.** Five of ten criteria are prose. | §4 note | Medium | **Open** — CF-029 |
| A7 | **The 24-frame benchmark cost is estimated, not measured.** The estimate uses the same extrapolation this project criticises elsewhere. | §5 | Medium | **Open** — CF-028 measures it |
| A8 | **`CF_SHADOW_QUALITY` and `CF_ANIMATE` were added mid-review.** The scene script now has three boolean env switches; undocumented combinations could produce incomparable renders. | `blender_scene_proof.py` | Low | Accepted — every comparison in this round recorded its switches |

### Cinematic findings — carried forward, all still open

| ID | Finding | Status |
|---|---|---|
| C1 | NFC rings read as three independent hoops, not an electromagnetic field | **Open** |
| C2 | No contact shadow between card and terminal | **Open** |
| C3 | Card has no branding, number block or contactless glyph | **Open** — chip and stripe added, both still visible |
| C4 | Composition bottom-heavy; top third empty | **Open** |
| C5 | No depth of field | **Open** |
| C7 | The frame teaches nothing — no numeral, no causal arrow, no motion | **Open** |
| **C8** | **The worst-quality region is the floor, which occupies the bottom third of frame.** The defect is in the most prominent area, not a corner. | **New — Open** |

### Product findings — carried forward

| ID | Finding | Status |
|---|---|---|
| P1 | Zero published videos after eight sessions | **Open** |
| P2 | No architecture proven end-to-end | **Open** |
| P3 | Every artefact describes a system that does not exist | **Open** |
| P5 | Script, factual verification and narration have no work behind them | **Open** |
| P6 | Four ADRs still `proposed` | **Open** — amended, not accepted |

---

## 3. What this round changed in the plan

| Before | After |
|---|---|
| "8 samples is enough for animation" | 8 samples is enough for card, rings, background only. Floor needs 64. |
| Floor is a neutral set element | **Floor is the quality bottleneck and an art-direction lever** |
| Local animation: one cost number | Local animation: 28 min (matte floor) to 100 min (glossy floor) per 10 s |
| Render settings are a technical choice | Render settings are a *creative* choice with a 3.6× cost span |

The last row is the substantive finding: **the biggest local performance lever is whether the floor reflects.** That belongs in `BENCHMARK_SPEC_PREMIUM.md`, not in a benchmark report.

---

## 4. Revised architecture recommendation

**Unchanged in structure, sharpened in scope.**

| Layer | Tool | Where | Why |
|---|---|---|---|
| Spine — all text, diagrams, charts, captions | SVG → resvg → FFmpeg (Architecture A) | Local | Deterministic, cheap, no GPU |
| Hero stills | Blender Eevee | **Local** — 25 s at 64 spp | Measured viable |
| Look-dev previews | Blender Eevee | **Local** — 2.9 s at 108×192 | Measured viable |
| Hero motion | Blender Eevee | **Remote** — 10 s shot exceeds every local budget | Measured non-viable locally |
| Long-form 3D (later) | Remote 4090 | Remote | $0.02–0.10 per 10 s estimated |

This is **Architecture F (hybrid)** in practice, and it is what ADR-0001 + ADR-0002 jointly describe once the amendments are read. Neither ADR needs replacing; both need sign-off.

**The recommendation is not "adopt Blender".** It is: local Blender is now a proven tool for stills and previews, and remains unproven for motion because no remote render has been run. Until B1 is approved, the motion row is an estimate.

---

## 5. Next smallest approval request

**CF-028 — the 24-frame local animation benchmark.**

- 24 frames, 540×960, 8 samples, encoded with FFmpeg.
- Estimated **under 3 minutes**; bounded in one foreground command.
- Costs €0. Installs nothing. Uses only Blender and FFmpeg already present.
- Produces: the first moving image the project has ever made, a real (not estimated) cost figure, and a check on whether an animated sequence exposes the flicker the static test could not.

It is deliberately the smallest thing that produces motion. Everything else either costs money or needs a remote host.
