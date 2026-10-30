# 05 — Scorecard and Sensitivity Analysis

Rubric and weights are taken verbatim from the plan (Phase 7). Scores are 0–5.
`weighted = Σ (weight × score / 5)`, maximum 100.

Scoring rule applied strictly: **an unknown is neither 0 nor 5**. Where evidence is missing, the score is capped at 2, marked low confidence, and re-tested in the sensitivity section.

---

## 1. Scenario S0 — the design as written, on this laptop as measured

| # | Dimension | Weight | Score | Weighted | Confidence | Basis |
|---|---|---:|---:|---:|---|---|
| 1 | Machine capability and sustained rendering feasibility | 20 | **2** | 8.0 | High | No supported Cycles GPU; 58.2 GB free; corporately managed; only 8.7 GB RAM free at audit |
| 2 | Blender pipeline functionality and accuracy | 20 | **3** | 12.0 | Medium | Deterministic templates are the right approach, but Blender is not installed and no render has been measured |
| 3 | Dependency compatibility and reproducibility | 15 | **2** | 6.0 | Medium | Python 3.14 only; no Blender; Docker daemon unverified; corporate policy unknown |
| 4 | Security and licence/commercial suitability | 15 | **3** | 9.0 | High | Blender GPL and Remotion/n8n terms are workable; Edge TTS and asset licensing are unresolved; MCP is RCE-by-design |
| 5 | Content quality and fact-checking design | 10 | **3** | 6.0 | Medium | Claims registry is designed, not implemented; no editorial pilot exists |
| 6 | Automation reliability and maintainability | 10 | **3** | 6.0 | Medium | Schema-first design is sound; no code, no tests, no queue yet |
| 7 | Costs, scalability and cloud fallback | 5 | **4** | 4.0 | Medium | Local CPU is cheap; cloud fallback is straightforward; human labour dominates and is accounted for |
| 8 | Observability, tests and pilot measurability | 5 | **3** | 3.0 | Medium | Ledger and QA records designed; benchmark not authorised |
| | **Total** | **100** | | **54.0** | | |

**S0 = 54 / 100 → NO-GO under the plan's own decision rule (<65).**

Two dimensions (1 and 3) are capped by hard evidence, not opinion. Even perfect scores elsewhere could not rescue them: the GPU limitation is physical, and the policy question is external.

## 2. Scenario S1 — revised architecture (hybrid, cloud render, deterministic spine)

What changes: host policy resolved (personal machine or written permission); Cycles renders on rented GPU; Edge TTS replaced by licensed TTS; isolation and gates enforced by schema; disk managed via external storage.

| # | Dimension | Weight | S0 | S1 | Why it moves |
|---|---|---:|---:|---:|---|
| 1 | Machine capability | 20 | 2 | **3.5** | Cloud render removes the GPU ceiling; local disk/RAM remain |
| 2 | Blender pipeline functionality | 20 | 3 | **3.0** | Unchanged — still unproven until a benchmark runs |
| 3 | Dependency compatibility | 15 | 2 | **4.0** | Pinned portable Blender + uv-locked Py3.12 + policy resolved |
| 4 | Security and licence | 15 | 3 | **3.5** | Licensed TTS, isolated worker; residual MCP and asset risk |
| 5 | Content quality | 10 | 3 | **3.0** | Design only, no change |
| 6 | Automation reliability | 10 | 3 | **4.0** | Idempotency, queue, strict schemas, rollback defined |
| 7 | Costs | 5 | 4 | **4.0** | Unchanged |
| 8 | Observability | 5 | 3 | **2.5** | Lowered: telemetry sources for thermals/VRAM are absent on this host |
| | **Total** | | **54.0** | **69.0** | |

**S1 = 69 / 100 → CONDITIONAL GO (65–79).**

This is a **projection of plan completeness under stated changes**, not a measured improvement. No line of code was written and no frame was rendered. Plan item 7.6 is respected: the score reflects readiness of the *design*, not the *system*.

## 3. Sensitivity analysis

The four dimensions carrying real uncertainty are #1, #2, #3, #8.

| Case | Assumption | Weighted total | Verdict band |
|---|---|---:|---|
| Pessimistic | Cloud render unavailable, policy unclear, benchmark never run (dims 1,3 → 2; 2,8 → 2) | **44.5** | NO-GO |
| Base S1 | As tabulated | **69.0** | CONDITIONAL GO |
| Optimistic | Benchmark passes comfortably, policy resolved, cloud budget approved (1,3 → 5; 2,8 → 4) | **80.5** | GO (if no blockers) |

Widening: the plan's core promise is currently worth somewhere between **44 and 80**, and that spread is dominated by two facts that a single approved benchmark plus one policy answer would collapse.

`★ Insight` A score range this wide is not a measurement — it is a decision waiting for two inputs. That is exactly why the next action is a question, not a task.

## 4. Hard-blocker override

Per plan Phase 7: critical blockers override numeric scores.

| Blocker | Status | Overrides score? |
|---|---|---|
| B1 corporate-managed device | **Unresolved** | **Yes** — no score permits installing on a device whose policy is unknown |
| B2 no supported Cycles GPU | Mitigated only by CPU render or cloud | No — design change handles it |
| B3 legal/execution surface | Partially mitigated (TTS, isolation) | No — but blocks monetisation until resolved |

**Result: S1's 69 is conditional on B1. With B1 unresolved, the operative verdict remains NO-GO.**

## 5. Plan-quality assessment (subjective, labelled)

The plan self-graded v1.1 at 4.8/5. That number could not have been earned before any audit existed: it predates the machine inventory, the licence checks, and the repository verification. Independent editorial scores:

| Aspect | Plan v1.1 | Revised (this report set) | Basis for change |
|---|---:|---:|---|
| Scope and deliverables | 5 | 5 | Already strong |
| Safety and reversibility | 4 | 5 | Isolation and rollback now concrete |
| Hardware diagnostics | 2 | 5 | Measured, not assumed |
| Dependencies and licensing | 2 | 5 | Primary sources fetched; traps identified |
| Open-source comparison | 2 | 5 | 13 candidates verified; omission found |
| Architecture realism | 3 | 4 | Deterministic spine justified; still unbenchmarked |
| Cost modelling | 3 | 4 | Labour included; assumptions labelled |
| Acceptance tests | 3 | 4 | Concrete thresholds; benchmark still pending |
| Evidence and uncertainty | 1 | 5 | Every claim carries a source or a label |
| Actionability | 3 | 4 | One blocking question, explicit gates |
| **Average** | **2.8** | **4.6** | |

The v1.1 average of 2.8 matches the plan's *own draft* score — the revision to 4.8 was not supported by any new evidence at the time.

## 6. What would move the verdict

| Event | Effect on S1 |
|---|---|
| Written policy approval + cloud budget approved | → solid CONDITIONAL GO, Phase A unblocked |
| B1 benchmark passes under 10 min | dim 2 → 4 → score ~77 |
| B1 benchmark fails (>30 min) | dim 1 → 2 → score ~60 → redesign to 2D/Manim |
| Personal machine with RTX-class GPU | dim 1 → 5 → score ~76 without cloud spend |
| Any monetised upload using Edge TTS | legality risk regardless of score |
