# Master Plan

Owner: user. Status: **documentation phase**. Last updated: 2026-10-30.
This file owns **phase and gate state only**. Evidence lives in `reports/`; decisions live in ADRs; atomic work lives in `tasks/BACKLOG.md`.

---

## 1. Goal

Produce original educational videos (Money · Technology · Digital Safety) in 9:16 Shorts and 16:9 long-form, with a pipeline that is reproducible, commercially usable, and cheap to run.

## 2. Non-goals

- Multi-platform publishing (YouTube only for now).
- Fully autonomous publishing (human gates G1–G5 are mandatory).
- Real-time or trend-chasing content.
- 3D for its own sake — 3D is a tool, not the product.

## 3. Operating principles

1. **Deterministic spine.** The production render path is fixed code driven by JSON, not an agent.
2. **Zero idle.** No always-running service; every tool is invoked on demand.
3. **Files are the system.** Schemas, assets, ledger, and outputs are plain files under version control.
4. **Human gates.** Claims, script, storyboard, render, publish — all human-approved.
5. **Evidence over confidence.** An unmeasured claim is labelled, never promoted.

## 4. Status

| Item | State |
|---|---|
| Policy approval for this device (G0) | **Approved** — user declaration, 2026-10-30 |
| Architecture decision | Proposed (ADR-0001) — awaiting user sign-off |
| Benchmark B0 | Authorised: **no** |
| Visual benchmark (V0–V3) | POC built, **64/100** — below 90 bar; awaiting user review (`docs/reviews/VISUAL_BENCHMARK_REVIEW.md`) |
| Implementation | Not started |
| Current phase | R1 review — awaiting visual approval; R2 benchmark blocked on G6 |

## 5. Phases

| Phase | Goal | Depends on | Gate to exit | Status |
|---|---|---|---|---|
| **R0** | Resolve corporate-use policy and host choice | — | Written answer covering installation and personal commercial use | Done — user declaration 2026-10-30 |
| **R1** | Visual-language spike: SVG frames, CSS animation, cinematic WebGL POC | R0 or explicit risk acceptance | User approves the look | Implemented — 64/100, fails premium bar; awaiting V3 (`prototypes/cinematic`, `docs/reviews/VISUAL_BENCHMARK_REVIEW.md`) |
| **R2** | **B0 benchmark** — 10 s vector render | R1 | Pass: ≤3 min, ≤1.5 GB RAM, ≤15 MB, legible at 360 px | Not authorised |
| **R3** | Spine: schemas, frame generator, rasteriser, encoder | R2 pass | Re-render produces identical frames for static scenes | Not started |
| **R4** | Template library (5 templates, both ratios) | R3 | Every template renders cleanly in 9:16 and 16:9 | Not started |
| **R5** | Audio: TTS, captions, loudness | R3 | Caption drift < 80 ms; loudness −14 LUFS ±0.5 | Not started |
| **R6** | QA gates and ledger | R3 | Unverified claim cannot render | Not started |
| **R7** | Pilot: 1 Short + 1 long-form | R4–R6 | Accuracy, legibility, budget within tolerance | Not started |
| **R8** | Optional 3D hero shots via rented GPU | R7 | Shot < $0.50, reproducible on two runs | Not started |

Rollback per phase is defined in `reports/v2/07-roadmap-v2.md`. Every phase's artefacts are files; abandoning a phase means deleting its folder or reverting its commit.

## 6. Gate summary

Full definitions and record locations: [`docs/operations/APPROVAL_GATES.md`](../operations/APPROVAL_GATES.md).

| Gate | Question |
|---|---|
| G0 | Is this device permitted to host the work? |
| G1 | Are all claims sourced and human-verified? |
| G2 | Is the script accurate and clear? |
| G3 | Does the storyboard teach the claim visually? |
| G4 | Does the render pass legibility and continuity QA? |
| G5 | Is publication approved, including AI disclosure? |
| G6 | Is this specific benchmark authorised? |
| V3 | Does the visual benchmark meet the premium bar and get user creative approval? |

## 7. Open decisions

| # | Decision | Blocks |
|---|---|---|
| Q1 | Host: this device, a personal device, or cloud-only | Everything |
| Q2 | IT policy answer in writing | Installation |
| Q3 | Disk strategy (external SSD or strict purge) | Long-form production |
| Q4 | TTS provider if local quality is rejected | R5 |
| Q5 | YouTube channel / OAuth project | R7 publishing |
| Q6 | Visual language: diagrammatic vs richer 3D | R1 approval |
| Q7 | Monthly variable budget | R8 |
| Q8 | Correction policy for published errors | Re-render workflow |

Source: `reports/06-questions-and-approvals.md`.

## 8. Change control

- Phase state changes only by editing this table and recording the date.
- A new architecture direction requires a new ADR; the plan then references it.
- Benchmarks update `docs/benchmarks/README.md` and the relevant risk entries — never the audit reports.
