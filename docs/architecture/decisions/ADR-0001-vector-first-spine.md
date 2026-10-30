# ADR-0001 — Vector-first production spine

- Status: proposed
- Date: 2026-10-30
- Deciders: user (sign-off pending), agent (proposal)
- Related: ADR-0002, `reports/v2/02`

## Context

The pipeline must produce educational explainers on money, technology and digital safety, reliably and cheaply, on a 12-core laptop with **no supported Cycles GPU** and **58.2 GB free disk**.

Four architectures were scored on the same 40-second storyboard and 8-minute expansion, with the user's weights (accuracy 20, visual 20, laptop efficiency 20, cost 15, automation 10, maintainability 10, legal 5):

| Architecture | Score |
|---|---:|
| A — SVG/Lottie/Motion Canvas + FFmpeg | 82.5 |
| D — Remote Blender + local orchestration | 83.5 |
| B — Manim + selective Eevee | 78.0 |
| C — three.js / R3F headless | 78.0 |

D scored 1.0 point higher, inside the error bars of either score. The difference was entirely visual quality; D lost on operating risk (vendor dependency, upload step, recurring cost).

## Decision

Use **Architecture A** as the production spine: a Python frame generator emits SVG from storyboard JSON, `resvg` rasterises frames, and FFmpeg encodes with `libx264` (or `h264_qsv`). Text, diagrams, charts, transitions and captions all live here.

Manim may be added later for mathematical topics. Blender is not part of the spine.

## Alternatives considered

| Option | Why rejected as the spine |
|---|---|
| D — remote Blender | Makes an external dependency the core of every video; a vendor outage stops production |
| B — Manim + local Eevee | Eevee on an unsupported iGPU is unmeasured, RAM-hungry, and disk-heavy (15–40 GB per long episode) |
| C — three.js headless | Most complex way to obtain 3D on a machine with no supported 3D backend; headless WebGL determinism is unreliable |

## Consequences

**Positive:** deterministic output; tiny toolchain (~50 MB); no idle processes; cheapest per video; every artefact is a file.

**Negative:** no depth, lighting, or material realism. If the channel's identity depends on continuous 3D camera work, this decision is wrong and must be superseded.

**Harder:** scene craft is manual — every good-looking frame is authored, not prompted.

## Evidence

- `reports/v2/02-architecture-comparison-v2.md` — scoring and storyboard walkthrough
- `reports/01-machine-inventory.md` — measured hardware limits
- `reports/v2/05-cost-resource-model-v2.md` — cost and disk model

## Review trigger

Revisit if B0 fails, if more than ~30 % of planned episodes are spatial rather than conceptual, or if audience retention shows the visual style is insufficient.

---

## Amendment — measured Eevee evidence (2026-10-30)

**Status unchanged: still `proposed`.** This amendment records evidence; it does not accept the ADR.

### What the original text got wrong

The "B — Manim + local Eevee" rejection read *"Eevee on an unsupported iGPU is unmeasured"*. It is now measured, and the premise behind that rejection is partly obsolete.

### Measured, 1080×1920

| Fact | Value | Source |
|---|---|---|
| GPU backend | Intel Graphics, OpenGL 4.6.0 build 32.0.101.8860 — **hardware, not software** | `BLENDER_EEVEE_CORRECTION.md` §2 |
| 8 TAA samples | 7.13 s/frame | this ADR amendment |
| 32 TAA samples | 15.67 s/frame | same |
| 64 TAA samples | 25.15 s/frame | same |
| 240 frames at 32 spp | **63 min** | computed |
| Temporal stability | static frames bit-identical (SSIM 1.000000) | `SAMPLE_AND_TEMPORAL_QA.md` |

### What this does to this ADR

The spine decision rests on *determinism, toolchain size and cost*, not on Eevee's speed. None of those changed. Local Eevee at 63–100 min per 10 s remains far outside a production loop, so "Blender is not part of the spine" is **unchanged**.

One clause does need to soften. The Consequences section says *"no depth, lighting, or material realism. If the channel's identity depends on continuous 3D camera work, this decision is wrong."* The measured evidence shows 3D realism is now **reachable but not locally renderable in motion**. That strengthens the case for a hybrid (A spine + remote D for hero shots) rather than for replacing A.

### New review trigger

Revisit if a 10-second hero shot can be rendered locally in under 5 minutes at production quality. Current best is 63 min at the lowest quality that clears the QA bar.
