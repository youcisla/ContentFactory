# Audit archive — index and rules

The audits themselves live in [`reports/`](../../reports/) and are **immutable** (ADR-0005). This page only maps them and records the rules.

## Index

### v2 — revised architecture (2026-10-30, afternoon)

| File | Contents |
|---|---|
| [00-executive-decision-v2.md](../../reports/v2/00-executive-decision-v2.md) | Verdict, four-architecture scores, single next action |
| [01-reconciliation-v2.md](../../reports/v2/01-reconciliation-v2.md) | Contradictions found in v1 and their resolutions |
| [02-architecture-comparison-v2.md](../../reports/v2/02-architecture-comparison-v2.md) | A/B/C/D on one storyboard, weighted scoring |
| [03-publishing-tools-v2.md](../../reports/v2/03-publishing-tools-v2.md) | Postiz, OpenPost, Mixpost, YouTube API |
| [04-tts-assets-render-v2.md](../../reports/v2/04-tts-assets-render-v2.md) | TTS, editing, assets, GPU pricing |
| [05-cost-resource-model-v2.md](../../reports/v2/05-cost-resource-model-v2.md) | Cost and resource model |
| [06-dependency-matrix-v2.csv](../../reports/v2/06-dependency-matrix-v2.csv) | Component matrix |
| [07-roadmap-v2.md](../../reports/v2/07-roadmap-v2.md) | Phases, acceptance, rollback, B0 spec |
| [08-adversarial-review-v2.md](../../reports/v2/08-adversarial-review-v2.md) | Weak assumptions, evidence that would flip the decision |

### v1 — initial preflight (2026-10-30, morning)

| File | Contents |
|---|---|
| [00-executive-decision.md](../../reports/00-executive-decision.md) | Initial verdict (**contains the superseded 66/100 figure**) |
| [01-machine-inventory.md](../../reports/01-machine-inventory.md) | Measured hardware, redacted |
| [02-dependency-matrix.csv](../../reports/02-dependency-matrix.csv) | Initial component matrix |
| [03-repository-due-diligence.md](../../reports/03-repository-due-diligence.md) | Blender-centric candidate review |
| [04-architecture-and-build-plan.md](../../reports/04-architecture-and-build-plan.md) | Contracts, queue, isolation, benchmark design |
| [05-scorecard.md](../../reports/05-scorecard.md) | Weighted scoring, sensitivity |
| [06-questions-and-approvals.md](../../reports/06-questions-and-approvals.md) | Open questions Q1–Q8 |
| [07-adversarial-review.md](../../reports/07-adversarial-review.md) | First adversarial pass |

## Rules

1. No edits to published reports. Corrections go in a new version.
2. v1 is retained deliberately: it shows what the audit got wrong and how it was caught.
3. Raw evidence captures (`reports/evidence/`) are git-ignored — they contain local paths. Use the URLs in the reports to re-fetch.
4. Machine-specific identifiers were redacted before publication (ADR-0006).

## Known correction trail

| Issue | Where it was introduced | Where it was fixed |
|---|---|---|
| 66 vs 69 score | v1 `00` | v2 `01` §R1 |
| Pessimistic case 44.5 | v1 `05` | v2 `01` §R2 |
| Cost envelope mismatch | v1 `00` vs `04` | v2 `01` §R3 |
| Review rate applied to shorts | v1 `00` | v2 `01` §R4 |
