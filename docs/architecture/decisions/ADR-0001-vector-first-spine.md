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
