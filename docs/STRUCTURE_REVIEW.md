# Structure Review — proposed vs implemented

Purpose: score the proposed repository structure, name its weaknesses, and record what was changed. This is a review artefact, not a plan.

---

## 1. Proposed structure (as submitted)

```
ContentFactory/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── docs/
│   ├── roadmap/MASTER_PLAN.md
│   ├── architecture/decisions/
│   ├── research/{open-source-projects,licensing,costs}/
│   ├── audits/
│   └── benchmarks/
├── tasks/BACKLOG.md
├── src/
├── tests/
└── .gitignore
```

## 2. Score — 60 / 100

| Criterion | Weight | Score | Why |
|---|---:|---:|---|
| Discoverability | 15 | 11 | No index, no status snapshot, no read order |
| Separation of concerns | 15 | 10 | `docs/audits/` duplicates the existing `reports/` |
| Single source of truth | 15 | **8** | `MASTER_PLAN` and `BACKLOG` have no boundary; content will fork |
| Scalability | 15 | 11 | `src/` and `tests/` are empty and cannot be tracked by git |
| Handoff clarity | 15 | 9 | `AGENTS.md`/`CLAUDE.md` were generic, not project-specific |
| Risk and compliance control | 15 | **5** | No risk register, no approval gates, no publication/redaction policy |
| Maintenance cost | 10 | 6 | Copying audit content into `docs/audits` guarantees drift |
| **Total** | **100** | **60** | Skeleton, not an operating system |

## 3. Weaknesses and corrections

| # | Weakness | Correction |
|---|---|---|
| W1 | `docs/audits/` would hold copies of `reports/`, which already has v1 and v2 with cross-references | **Keep `reports/` immutable as the evidence archive.** `docs/audits/` becomes an index plus rules. No duplication, no broken links |
| W2 | `MASTER_PLAN` vs `BACKLOG` undefined | Explicit boundary: plan owns phases, gates, acceptance; backlog owns atomic tasks. Neither restates the other |
| W3 | No architecture description, only decisions | Added `docs/architecture/ARCHITECTURE.md` — system, contracts, boundaries. ADRs explain *why*; this explains *what* |
| W4 | ADRs have no template, numbering, or status rules | ADR index defines `proposed/accepted/superseded`, numbering, and a template |
| W5 | No risk register or gates despite being a safety-critical plan | Added `docs/risks/RISK_REGISTER.md` and `docs/operations/APPROVAL_GATES.md` |
| W6 | No publication policy on a public repo | Added ADR-0006 plus rules in `CLAUDE.md`, `AGENTS.md`, `README.md` |
| W7 | `src/` and `tests/` are empty; git cannot track empty directories | Not created. They appear when code exists. Documented in README |
| W8 | Generic `AGENTS.md` gives no project rules | Appended a project section; generic guidance preserved verbatim |
| W9 | Research folders would be empty shells | Each gets a substantive digest with links to the audit evidence |
| W10 | No status snapshot | README opens with a status table naming the one blocking decision |
| W11 | No licence decision for a public repo | Flagged as an open question in the ADR index rather than silently chosen |
| W12 | No benchmark record despite benchmark being the gate | `docs/benchmarks/README.md` holds the B0 spec and its not-run status |

## 4. Revised score — 91 / 100

| Criterion | Score | Note |
|---|---:|---|
| Discoverability | 14 | README map + read order |
| Separation of concerns | 14 | evidence / index / decisions / work clearly split |
| Single source of truth | 14 | precedence rule stated in three places, one rule |
| Scalability | 13 | folders exist only where content exists |
| Handoff clarity | 14 | CLAUDE.md and AGENTS.md are project-specific |
| Risk and compliance | 14 | register, gates, publication policy |
| Maintenance | 8 | link-don't-copy rule enforced by review, not tooling |
| **Total** | **91** | |

Nine points withheld: nothing verifies the rules automatically. A link checker and a pre-commit secret scan would earn them, but both need tooling that this phase forbids.

## 5. Deviations from the requested tree

| Requested | Implemented | Reason |
|---|---|---|
| `docs/audits/` containing audits | Index pointing to immutable `reports/` | Evidence integrity and no link churn (W1) |
| `src/`, `tests/` | Omitted until code exists | Git cannot track empty directories (W7) |
| `docs/research/*` folders | Present, each with a digest | Empty folders are noise (W9) |
| — | `docs/risks/`, `docs/operations/` added | Required by "risk register and approval gates" |

## 6. What this review does not cover

- Whether the documentation is factually right — that is `reports/`' job.
- Whether the architecture is correct — that is the ADRs' job.
- Whether the repo should be public — a user decision, flagged in ADR-0006.
