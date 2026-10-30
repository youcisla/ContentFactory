# ContentFactory

Documentation-first repository for an automated educational video pipeline (Money · Technology · Digital Safety), producing 9:16 Shorts and 16:9 long-form.

**Phase: benchmarks and prototypes.** Blender 5.2.3 is installed and Eevee is measured on this host; SVG, CSS and WebGL prototypes exist; no production pipeline code yet. See `docs/roadmap/MASTER_PLAN.md` for gates.

---

## Status snapshot

| Item | State | Source |
|---|---|---|
| Audit v1 (machine, dependencies, repos, architecture) | Complete | [`reports/`](reports/) |
| Audit v2 (four architectures, publishing tools, live GPU pricing) | Complete | [`reports/v2/`](reports/v2/) |
| Architecture decision | **Proposed** — vector-first spine + remote Blender for hero shots; awaiting sign-off | [ADR-0001](docs/architecture/decisions/ADR-0001-vector-first-spine.md) |
| Corporate-use approval for this device | **Approved — user declaration, 2026-10-30** | [Risk R1](docs/risks/RISK_REGISTER.md) |
| Blender 5.2.3 + Eevee on this host | **Measured** — renders headlessly on Intel OpenGL 4.6; 6.7–29 s per 1080×1920 frame depending on settings | [`BLENDER_EEVEE_RESULT.md`](docs/benchmarks/BLENDER_EEVEE_RESULT.md), [`BLENDER_EEVEE_CORRECTION.md`](docs/benchmarks/BLENDER_EEVEE_CORRECTION.md) |
| Visual benchmark V3 | **Failed as creative standard** — 64/100; accepted as technical baseline only | [`VISUAL_BENCHMARK_REVIEW.md`](docs/reviews/VISUAL_BENCHMARK_REVIEW.md) |
| Prototypes | R1 static SVG, R2 CSS animation, cinematic WebGL — all built | [`prototypes/`](prototypes/) |
| Benchmark B0 (vector render) | **Not run — awaiting approval** | [`docs/benchmarks/README.md`](docs/benchmarks/README.md) |
| Production pipeline | Not started — blocked on V4 | [`tasks/BACKLOG.md`](tasks/BACKLOG.md) |

## Current recommendation

| Architecture | Score /100 | Role |
|---|---:|---|
| A — SVG + rasteriser + FFmpeg | 82.5 | **Production spine** |
| D — Remote Blender | 83.5 | 3D hero shots only |
| B — Manim + Eevee | 78.0 | Secondary (math topics) |
| C — three.js headless | 78.0 | Rejected |

D scores one point higher than A but carries vendor, network, and cost dependencies. It is used surgically, not as the spine. Rationale: [reports/v2/02](reports/v2/02-architecture-comparison-v2.md) §6.

## Non-negotiable constraints (measured 2026-10-30)

- No supported Cycles GPU (integrated Intel adapter only) → 3D needs CPU or rented GPU.
- 58.2 GB free on C: → disk is a production ceiling.
- Device is corporate-managed, non-admin shell → installations require written approval.
- Publishing target is YouTube only → no multi-platform scheduler needed.

## Documentation map

| Area | Location |
|---|---|
| Master plan and phases | [docs/roadmap/MASTER_PLAN.md](docs/roadmap/MASTER_PLAN.md) |
| System architecture | [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) |
| Decisions (ADR log) | [docs/architecture/decisions/](docs/architecture/decisions/README.md) |
| Task backlog | [tasks/BACKLOG.md](tasks/BACKLOG.md) |
| Research digests | [docs/research/README.md](docs/research/README.md) |
| Audit archive (immutable) | [docs/audits/README.md](docs/audits/README.md) → `reports/` |
| Benchmarks | [docs/benchmarks/README.md](docs/benchmarks/README.md) |
| Risk register | [docs/risks/RISK_REGISTER.md](docs/risks/RISK_REGISTER.md) |
| Approval gates | [docs/operations/APPROVAL_GATES.md](docs/operations/APPROVAL_GATES.md) |
| Structure review | [docs/STRUCTURE_REVIEW.md](docs/STRUCTURE_REVIEW.md) |

## Source-of-truth rules

1. **Decisions** live in ADRs. If code and an ADR disagree, the ADR wins until superseded.
2. **Phase and gate state** lives only in `MASTER_PLAN.md`.
3. **Atomic work** lives only in `tasks/BACKLOG.md`; it never restates the plan.
4. **Evidence** lives in `reports/` and is append-only. New findings create a new version.
5. If two documents agree today and would diverge tomorrow, one of them is wrong — link, do not copy.

## Publication safety

This repository is public. Do not commit secrets, tokens, machine identifiers, corporate domains, employer names, or raw audit evidence. Rules: [ADR-0006](docs/architecture/decisions/ADR-0006-publication-redaction.md). Raw evidence is git-ignored.

## Licence

Not yet chosen. For a public repository this is a decision that should be made deliberately — see [ADR index](docs/architecture/decisions/README.md) open questions.

## Next action requiring approval

**V4 — one excellent scene.** Blender is installed and Eevee is measured; what remains is a scene that meets the premium bar and a render budget. The V4 gate is `docs/benchmarks/BLENDER_EEVEE_CORRECTION.md`. The vector spine (B0) remains unauthorised and is independent.

Open approval requests and their exact scope: [`tasks/BACKLOG.md`](tasks/BACKLOG.md).
