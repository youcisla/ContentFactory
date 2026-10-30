# Remediation Review — 2026-10-30

Scope: Phases 0–9 of the remediation directive. Scores are evidence-based; where evidence is missing the score says so.

---

## 1. Scorecard

| Dimension | Before (hypothesis) | Now | Evidence | What 5/5 requires |
|---|---:|---:|---|---|
| Engineering process | 4 | **4** | Gates G0–G6 + V3/V4 defined; immutable audit archive; progress log with BEFORE/AFTER; objective exposure gate added | CI running the gate; determinism test; a build that fails on regression |
| Tool discovery | 4 | **4** | `agent-reach-scan/`, `render-alternatives/`, `better-solutions/`; JANCTION, Modal, BlendFarm, TURNA, Praxilla, Farpy surfaced | Hands-on trial of at least one alternative; Reddit/X coverage restored in last30days |
| Hardware understanding | 3.5 | **4** | GPU backend named (Intel OpenGL 4.6, not software); sample/resolution/shadow cost curves measured; RAM 1.6 GB; disk 58.2 GB | Cycles measured; sustained/thermal behaviour; motion-blur and DOF cost |
| Architecture validation | 4 | **3.5** | Six options compared in research; **none compared on the same storyboard with measurements** | Same storyboard rendered by ≥2 architectures, compared blind |
| Documentation consistency | 2 | **3.5** | 15 discrepancies found and fixed; ID-reuse rule added; 10 files still unaudited (D19/D20) | Every file audited; cross-links machine-checked |
| Visual quality | 2 | **3** | `proof_final.png` — 14 materials, three-point lighting, real card geometry with chip and stripe, dark studio background, exposure gate PASS | Rings that read as a field not hoops; contact shadow; DOF; branding; and it must move |
| Production readiness | 1.5 | **1.5** | One scene script and one gate. No schema, no pipeline, no narration, no encoding integration | A 40 s episode rendered end-to-end from JSON without a human touching Blender |

**No aggregate score.** Averaging hides that the system cannot yet produce a video.

### Movement that is real

- Hardware understanding: a *hypothesis* ("maybe software OpenGL") became a *fact* ("Intel OpenGL 4.6, hardware"). That removes the largest remaining unknown in the render decision.
- Documentation: the repository no longer contradicts itself about what has been done.

### Movement that is not

- Production readiness did not move. Correctly. Nothing that produces a video exists.

---

## 2. What the corrections actually established

| Claim | Verdict |
|---|---|
| "42.64 s/frame is not a valid basis for a universal conclusion" | **Correct, for a different reason than implied.** The number is representative; the *explanation* in CF-020 was incomplete. |
| The frame was nearly black | **Confirmed.** Five compounding scene defects, all in `blender_evee_test.py`. None is a hardware finding. |
| Eevee may be falling back to software | **Refuted.** Intel OpenGL 4.6, build 32.0.101.8860, hardware. |
| Local animation is 11× over budget | **Overstated.** Measured range is 1.8× to 20.7× depending on settings. |
| Local animation is not viable | **Confirmed.** Every configuration exceeds ≤15 min per 10 s. |

---

## 3. Adversarial review — engineering

| ID | Finding | Severity | Status |
|---|---|---|---|
| E1 | The exposure gate thresholds (mean 0.04–0.40, p99 ≥0.70) were calibrated on one scene. A different art direction (high-key, white void) would fail them wrongly; a muddy grey frame could pass. | Medium | **Open** — needs per-scene expected ranges, not global constants |
| E2 | `est_240_frames_seconds` extrapolates from one frame in single-frame mode. That is the exact sin this review criticises. | Medium | **Partially fixed** — `CF_FRAMES` now measures a real sequence; the estimate should be ignored when `frames=1` |
| E3 | No determinism check. Two runs of `blender_scene_proof.py` are not compared for identical output. | High | **Open** |
| E4 | `tools/blender-test/` is gitignored, so the evidence images are outside version control. A fresh clone cannot verify the claim. | High | **Open** — needs a hash manifest committed, not the images |
| E5 | The scene relies on `bpy.ops`, which depends on selection and context state. It works headless but is fragile if reordered. | Low | Accepted |
| E6 | Shadow setting attributes are set through `setattr` in a `try/except pass`. If the names change in a future Blender, the setting silently does nothing. | Medium | Accepted — deliberate, but it means a silent quality regression is possible |
| E7 | `rounded()` applies scale but leaves rotation on the object. The chip and stripe use a matrix copy to compensate. Correct here, but two concepts for one placement. | Low | Accepted |

**Engineering verdict:** the work is defensible. E3 and E4 are the ones that would embarrass the project in front of an outside reviewer — a claim of "it renders and passes a gate" that cannot be reproduced from the repository is weak evidence.

---

## 4. Adversarial review — cinematic director

| ID | Finding | Severity | Status |
|---|---|---|---|
| C1 | **The NFC rings read as three independent hoops, not as an electromagnetic field.** They intersect the card, share no apparent source, and carry no falloff logic. This is physically misleading in a video about how contactless payment works — the thing the scene exists to explain. | **High** | **Open** |
| C2 | **No contact shadow.** The card floats with no shadow landing on the terminal, so the relationship between the two objects is not grounded. | High | **Open** |
| C3 | **The card is generic.** Chip and stripe are present but there is no branding, no number block, no contactless glyph. It reads as "a card", not "your card". | Medium | **Open** |
| C4 | **Composition is bottom-heavy.** The terminal is cropped at the lower-left; the top third is empty gradient. Safe, not striking. | Medium | **Open** |
| C5 | **No depth of field.** Everything is equally sharp, so the eye has no guided path. A product shot at this focal length would normally carry a shallow plane of focus. | Medium | **Open** |
| C6 | **Single-temperature lighting.** The key and rim are close in colour, so separation comes from brightness alone. | Low | **Open** |
| C7 | **It is a still of an object, not a teaching frame.** No numeral, no motion cue, no causal arrow. The viewer learns nothing from it that a stock photo would not teach. | **High** | **Open** |

**Cinematic verdict: 3/5 is generous.** The frame is a competent product render. It is not the "compelling cinematic explanation where objects and motion teach the viewer" the brief demands, because there is no teaching in it and no motion.

The single most valuable fix is C1 + C7 together: make the field visibly *originate* at the terminal's antenna, propagate upward, and be *intercepted* by the card — and put the mechanism's payoff (the transaction completing) inside the frame.

---

## 5. Adversarial review — skeptical product owner

| ID | Finding | Severity |
|---|---|---|
| P1 | Seven working sessions. **Zero published videos.** Zero 40-second episodes. | **Critical** |
| P2 | Four architectures explored in research; **none proven end-to-end** on a single real episode. | **Critical** |
| P3 | Every artefact is a document about a possible system. The system does not exist. | **Critical** |
| P4 | The analysis so far has cost more hours than a year of remote render time at measured rates ($0.02–$0.40 per scene). | High |
| P5 | **The actual bottleneck has no work behind it.** Script quality, factual verification (G1), and narration are untouched. A beautiful render of a wrong or dull explanation is worthless. | **Critical** |
| P6 | Four ADRs remain `proposed`. The architecture is still undecided after all this work. | High |

**Product verdict:** the project is over-invested in infrastructure and under-invested in content. The cheapest path to a real video is not another architecture comparison — it is one 40-second episode with a verified script, rendered by whichever path is furthest along.

---

## 6. Blockers requiring user action

| # | Blocker | What it unblocks | Cost |
|---|---|---|---|
| B1 | **Approve remote render** (RunPod 4090, $0.34/h) or JANCTION MCP | The 10 s V4 sequence. Local cannot meet the budget at any setting. | ~$0.05–0.35 |
| B2 | **Approve B0** (G6, vector spike) | The whole vector spine R3–R7 | €0, one 5 MB binary |
| B3 | **Sign off ADR-0001/0002** or reject them | Architecture certainty | — |
| B4 | **Decide the episode to produce** | Everything downstream of V4 | — |
| B5 | Approve cycling the corporate-device question | R16 | — |

---

## 7. Honest position

The repository is now internally consistent and the render question is settled with measurements instead of extrapolation. That is real progress on three dimensions.

It is also still a repository that cannot make a video. The gap between "a still passes an exposure gate" and "a 40-second educational Short exists, is accurate, and is watchable" is the entire product, and none of it has been built.

Optimising the scorecard from here would mean writing more documents. Optimising the product means picking one episode and forcing it through to a rendered file, accepting that the first one will be flawed.
