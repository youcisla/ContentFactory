# CLAUDE.md — project operating rules

Read in this order before acting:

1. `README.md` — status and map
2. `docs/roadmap/MASTER_PLAN.md` — phases, gates, current state
3. `tasks/BACKLOG.md` — atomic work and what is blocked
4. `docs/architecture/decisions/` — accepted decisions
5. Only the specific `reports/` file relevant to the question

## Current phase

**Documentation only.** Do not install packages, create environments, download models, run benchmarks, start services, or write implementation code unless a task in `tasks/BACKLOG.md` is marked approved and unblocked.

## Hard rules

- **No installation** until gate G0 (corporate policy) is answered in writing.
- **No benchmark** without the specific approval named in `docs/operations/APPROVAL_GATES.md`.
- **No commit or push** without explicit user approval. The user commits.
- **No agent in the publish path.** Automation may draft; a human approves every gate G1–G5.
- **Never commit** secrets, tokens, corporate domains, employer names, machine identifiers, or raw audit evidence. See ADR-0006.
- **Audit reports are immutable.** Corrections go in a new versioned report, never by editing history.

## Source-of-truth precedence

1. ADRs decide architecture.
2. `MASTER_PLAN.md` decides phase and gate state.
3. `BACKLOG.md` decides what work exists.
4. `reports/` is evidence — it can be superseded, never rewritten.

If a request conflicts with an accepted ADR, say so and propose a new ADR rather than silently diverging.

## Tool-use constraints for this repository

- Prefer read-only inspection. Nothing here needs a package manager yet.
- Do not run `npm install`, `pip install`, `uv sync`, `docker compose`, or model downloads.
- Do not execute third-party project code.
- Keep writes inside the repository; do not write outside it without approval.

## Style of work

- Smallest change that satisfies the request.
- Every changed line traces to an explicit instruction.
- Surface uncertainty; do not convert an unknown into an assumption.
- When a benchmark result arrives, update the register, not the narrative.
