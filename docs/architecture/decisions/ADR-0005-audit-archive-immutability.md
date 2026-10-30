# ADR-0005 — Audit archive is immutable

- Status: proposed
- Date: 2026-10-30
- Deciders: user (sign-off pending), agent (proposal)
- Related: ADR-0006, `docs/STRUCTURE_REVIEW.md`

## Context

Two audit generations exist: `reports/` (v1) and `reports/v2/`. They contain measurements, licence checks, and a documented correction of their own errors (the 66-vs-69 reconciliation, the sensitivity miscalculation).

The proposed documentation structure placed audits under `docs/audits/`, which would duplicate or move these files. Moving them would break internal cross-references and sever the trail that shows what changed between versions.

Audit reports are also the only record that can later prove *why* a decision was made.

## Decision

`reports/` is the **immutable audit archive**. It is never edited after publication. New findings create a new versioned folder (`reports/v3/`, …). `docs/audits/` contains only an index and the rules for using the archive.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Move reports into `docs/audits/` | Breaks cross-references; implies the archive is living documentation |
| Copy reports into `docs/audits/` | Guarantees drift between two copies |
| Rewrite v1 to fix the 66/69 error | Destroys the evidence that the audit caught its own mistake |

## Consequences

**Positive:** trustworthy evidence trail; corrections are visible as corrections; links stay stable.

**Negative:** the repository has two documentation locations (`docs/` and `reports/`) and readers must know the difference.

**Harder:** every new audit version adds files rather than improving existing ones. That is the intended cost.

## Rules

1. No edits to published report files.
2. Corrections go in a new versioned report that names what it supersedes.
3. Evidence raw captures are git-ignored; reports cite source URLs so they can be re-fetched.
4. `docs/audits/README.md` is the map — keep it current when a new version lands.
