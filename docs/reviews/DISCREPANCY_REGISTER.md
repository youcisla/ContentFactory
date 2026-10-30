# Discrepancy Register — 2026-10-30

Phase 0 of the remediation. Every status claim in the repository checked against evidence on disk. Corrections applied in place where the file is a living document; `reports/` was left untouched because audit history is immutable (ADR-0005).

---

## Found and corrected

| # | File | Claim | Reality | Action |
|---|---|---|---|---|
| D1 | `README.md:5` | "documentation only… no dependencies installed, no benchmark executed" | Blender 5.2.3 installed; Eevee measured at 42.64 s; three prototypes built | Rewritten to "benchmarks and prototypes" |
| D2 | `README.md` status table | "Benchmark B0 — not run"; "Implementation — not started" | CF-010–CF-020 complete; `prototypes/cinematic/the-tap.mp4` rendered | Table now lists Blender/Eevee, V3 64/100, prototypes, and separates B0 from the Eevee work |
| D3 | `README.md` "Next action" | "Run the R1 visual spike" | R1 was completed and reviewed | Now points at V4 |
| D4 | `MASTER_PLAN.md` status | "Premium 3D feasibility… install not approved" | Installed via CF-020 | Row replaced with measured capability |
| D5 | `MASTER_PLAN.md` status | "V4 one-scene gate — Blocked, needs Blender approval" | Blender approved and installed | Now "Open — scene quality and render budget outstanding" |
| D6 | `MASTER_PLAN.md` status | "Implementation — Not started" | Contradicts CF-010–CF-020 being done | Now "Production pipeline — not started, blocked on V4" |
| D7 | `MASTER_PLAN.md` phases | V4 "Blocked — install approval" | Install is done | Now "Open" |
| D8 | `BACKLOG.md` header | "every task is blocked on G0 or G6. No implementation is authorised" | G0 approved; 11 tasks done | Rewritten with current state |
| D9 | `BACKLOG.md` | **CF-020 defined twice** — "Install Blender" and "Approve and run B0" | Two different tasks, one ID | Phase 2 row renumbered **CF-026** |
| D10 | `BACKLOG.md` | **CF-021 defined twice** — "V4 benchmark" and "Update risk R2/R3" | Two different tasks, one ID | Phase 2 row renumbered **CF-027** |
| D11 | `BACKLOG.md` CF-019 | "blocked — user approval" | Blender installed | Marked done |
| D12 | `BACKLOG.md` CF-021 | "blocked — CF-023 + local still test" | Local still test done (CF-025) | Marked in progress |
| D13 | `RISK_REGISTER.md` R15 | "42.64 s/frame — 240 frames ≈ 170 min" | Correct order of magnitude but the *reason* was misattributed; true range is 27 min to 5.2 h depending on settings | Rewritten with the measured curve and the hardware-backend confirmation |
| D14 | `RISK_REGISTER.md` R2 | "Open — B0 measures it" | B0 unmeasured, but the 3D path is now measured and fails | Marked confirmed for 3D, still open for vector |
| D15 | `APPROVAL_GATES.md` G6 | Implies G6 governs all benchmarks | CF-020 and CF-025 were authorised directly by the user, not through G6 | Noted explicitly |

## Found and left in place

| # | File | Why not changed |
|---|---|---|
| D16 | `reports/00`–`07`, `reports/v2/00`–`08` | Immutable audit history (ADR-0005). Their known v1 arithmetic errors are already reconciled in `reports/v2/01-reconciliation-v2.md`. |
| D17 | `README.md` architecture scores (A 82.5, D 83.5, B 78.0, C 78.0) | These are v2 research results, correctly cited. But the table calls three.js "Rejected" while `prototypes/cinematic/` is a three.js/WebGL POC. The score table is a *research* result, the prototype is a *technical baseline*; both can be true. Flagged here rather than rewritten, because changing a research score without re-running the comparison would be worse. |
| D18 | `ADR-0001`–`ADR-0006` all `proposed` | Correct. None has been signed off. Blender being installed does not accept ADR-0002. |

## Not verified

| # | Item | Why |
|---|---|---|
| D19 | `ARCHITECTURE.md`, `STRUCTURE_REVIEW.md`, `docs/agent-governance/*`, `docs/research/*` (10 files) | Not read line by line in this pass. Claiming documentation consistency at 5/5 without reading them would be dishonest. |
| D20 | `docs/benchmarks/README.md`, `docs/reviews/*` | Not re-read after edits elsewhere; cross-links unverified. |

## The pattern

Every discrepancy was **stale status, not fabricated work**. The evidence files were accurate; the summary documents stopped being updated when the work moved. That is the cheapest class of documentation defect and the one most likely to recur, because nothing fails when a table goes stale.

**Structural fix applied:** `BACKLOG.md` now states an explicit ID-reuse rule, and the divergence is recorded here rather than silently overwritten.
