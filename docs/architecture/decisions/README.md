# Architecture Decision Records

One file per decision. ADRs are append-only: a decision is changed by writing a new ADR that **supersedes** the old one, never by editing history.

## Conventions

| Field | Values |
|---|---|
| Number | `ADR-000N`, never reused |
| Status | `proposed` · `accepted` · `superseded by ADR-000N` · `rejected` |
| Date | ISO `YYYY-MM-DD` |
| Deciders | user (final), agent (proposal) |

Filename: `ADR-000N-short-slug.md`.

## Template

```markdown
# ADR-000N — Title

- Status: proposed | accepted | superseded by ADR-000N
- Date: YYYY-MM-DD
- Deciders: user, agent
- Related: links

## Context
What forces are at play. Facts, constraints, measurements.

## Decision
The choice, in one paragraph, in the active voice.

## Alternatives considered
| Option | Why rejected |

## Consequences
Positive, negative, and what becomes harder.

## Evidence
Links to reports or measurements. No unsupported claims.
```

## Index

| ADR | Title | Status | Date |
|---|---|---|---|
| [0001](ADR-0001-vector-first-spine.md) | Vector-first production spine | proposed | 2026-10-30 |
| [0002](ADR-0002-remote-blender-hero-shots.md) | Remote Blender for hero shots only | proposed | 2026-10-30 |
| [0003](ADR-0003-direct-youtube-api.md) | Direct YouTube API for publishing | proposed | 2026-10-30 |
| [0004](ADR-0004-local-tts.md) | Local TTS with licensed fallback | proposed | 2026-10-30 |
| [0005](ADR-0005-audit-archive-immutability.md) | Audit archive is immutable | proposed | 2026-10-30 |
| [0006](ADR-0006-publication-redaction.md) | Publication and redaction policy | proposed | 2026-10-30 |

## Open questions (not yet ADRs)

| # | Question | Trigger to decide |
|---|---|---|
| O1 | Repository licence | Before accepting external contributions or reuse |
| O2 | Whether the repo stays public | Before any further machine-specific evidence is added |
| O3 | Visual language depth (2.5D vs 3D) | After B0 and audience feedback |
| O4 | Long-term storage for masters and evidence | When disk drops below 15 GB |
