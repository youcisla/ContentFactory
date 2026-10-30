# Approval Gates

No gate may be auto-approved. Each record is a written entry (file or signed note) naming who approved, what was reviewed, and when.

| Gate | Question | Evidence required | Approver | Record | Status |
|---|---|---|---|---|---|
| **G0** | Is this device permitted to host the work? | Written policy answer or host change | User / IT | This file, G0 section | **Approved — user declaration, 2026-10-30** |
| **G1** | Are all claims sourced and human-verified? | Every claim has `verified_by_human: true` and at least one source | User | `claims.json` | Not started |
| **G2** | Is the script accurate, clear, non-misleading? | Script text + claim mapping | User | `reviews/<episode>.json` | Not started |
| **G3** | Does the storyboard teach the claim visually? | Storyboard JSON + frame stills | User | `reviews/<episode>.json` | Not started |
| **G4** | Does the render pass legibility and continuity QA? | `qa.json` per scene | User | `qa.json` | Not started |
| **G5** | Is publication approved, including AI disclosure? | `publish.json` with disclosure flag | User | `publish.json` | Not started |
| **G6** | Is this specific benchmark authorised? | ID, scope, stop conditions, rollback | User | This file, G6 section | B0 pending |

## G0 — host and policy

**Required:** a written answer covering (a) whether third-party software may be installed without elevation, (b) whether a personal monetised channel may be produced on this device, (c) where project files may be stored.

**Current:** approved by **user declaration** on 2026-10-30. No separate IT document is on file; the approval is the user's own statement and is recorded as such. Installation is now gated by task approval and G6, not by G0.

**Fallbacks if refused:** personal device, or cloud-only pipeline. Architecture survives unchanged; only the render plane moves.

## G6 — benchmark authorisation

Only one benchmark is currently proposed.

| Field | Value |
|---|---|
| ID | B0 |
| Scope | 10 s vector render, 1080×1920, 3 scenes, local only |
| Downloads | one `resvg` binary (~5 MB) |
| Installs | none system-wide; project folder only |
| Services | none started |
| Models | none |
| Cloud | none |
| Location | `reports/v2/b0-spike/` |
| Pass | ≤3 min, ≤1.5 GB RAM, ≤15 MB output, legible at 360 px |
| Stop | >10 min, >3 GB RAM, <50 GB free, or any install demand |
| Rollback | delete the spike folder |
| Status | **awaiting approval** |

Full procedure: [`docs/benchmarks/README.md`](../benchmarks/README.md).

## Rules

1. A gate is closed only by an explicit statement from the approver.
2. Silence is not approval.
3. A gate cannot be waived to unblock work; the work waits.
4. If a gate is bypassed, the episode is not publishable.
5. Approval for one benchmark does not authorise the next.
