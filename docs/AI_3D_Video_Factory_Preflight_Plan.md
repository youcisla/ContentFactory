# AI 3D Educational Video Factory — Preflight Audit and Decision Plan
Version: 1.1 | Status: PLANNING ONLY | Owner: Claude Code (DeepSeek) | Platform: Windows laptop, verify rather than assume

## Mission and non-negotiable boundary
Assess whether the current laptop and software ecosystem can safely support an original, educational, automated 3D YouTube production workflow (Money + Technology + Digital Safety; Shorts 9:16 and long-form 16:9). Audit prerequisites, dependencies, licenses, open-source candidates, operational costs, security and machine capabilities. Produce an evidence-backed implementation plan. **Do not install, uninstall, upgrade, clone, download, modify system configuration, start persistent services, or build the system.** Read-only inspection is authorized; request explicit approval for any operation that changes state or incurs cost. Write audit artifacts only under a user-approved report directory. Never execute third-party project scripts during the audit.

## Required outputs
- `reports/00-executive-decision.md`: GO / CONDITIONAL GO / NO-GO, blockers, uncertainty and confidence.
- `reports/01-machine-inventory.md`: CPU/GPU/RAM/VRAM/storage/OS/drivers, software versions, evidence and dates.
- `reports/02-dependency-matrix.csv`: component, candidate, purpose, OS support, minimum/recommended needs, local status, license, security, maturity, evidence URL, score, disposition.
- `reports/03-repository-due-diligence.md`: validated repo identity, license, maintenance, code risks, actual Blender coverage, compatibility, adoption and alternatives.
- `reports/04-architecture-and-build-plan.md`: phased architecture, interface contracts, tasks/subtasks, dependencies, acceptance tests, costs, risks and rollback.
- `reports/05-scorecard.md`: weighted scoring and sensitivity analysis; distinguish measured facts, documentation and estimates.
- `reports/06-questions-and-approvals.md`: unresolved questions and proposed optional active benchmarks needing approval.
- `reports/evidence/`: redacted command outputs and source URLs/commit hashes, with no secrets or personal paths in shared reports.

## Phase 0 — Guardrails and discovery (P0)
- [ ] 0.1 Confirm host OS, shell, project root, report output path, permissions and whether this is a company-managed laptop.
- [ ] 0.2 Check repository instructions (`CLAUDE.md`, `AGENTS.md`) without executing their commands automatically.
- [ ] 0.3 Establish read-only audit mode; inventory permitted commands; avoid privilege elevation, system changes, package managers and network downloads.
- [ ] 0.4 Record timestamp, machine-local versus cloud assumptions, and confidence taxonomy: verified locally / verified upstream / inferred / unknown.
- [ ] 0.5 Redact usernames, hostnames, serial numbers, MACs, device IDs, tokens and private directory names from deliverables.
**Gate:** if safe read-only inspection cannot be established, stop and request approval.

## Phase 1 — Laptop capability audit (P0)
- [ ] 1.1 CPU: exact model, architecture, physical/logical cores, clock, virtualization, thermal/power limitations if measurable.
- [ ] 1.2 GPU: vendor/model, dedicated/shared VRAM, CUDA/OptiX/ROCm/oneAPI/Metal availability as applicable, driver and supported Blender render backend; distinguish display GPU from compute GPU.
- [ ] 1.3 RAM: installed, available, slots if obtainable read-only; identify headroom for Blender plus browser/agent workflows.
- [ ] 1.4 Storage: drive types, capacity/free space, filesystem, temp/cache and render output location; no invasive disk scans.
- [ ] 1.5 OS: Windows edition/build, WSL2 availability/status, container runtime presence, Python/Node/npm/FFmpeg/Blender/Git versions and PATH conflicts.
- [ ] 1.6 Network: basic DNS/connectivity only if already allowed; distinguish blocked access from missing dependencies.
- [ ] 1.7 Power and stability: AC vs battery; optional temperature telemetry if already installed; note inability to verify sustained performance without a benchmark.
- [ ] 1.8 Compare machine against documented minimum AND recommended requirements for each candidate, with URLs and dates; do not invent GPU compatibility.
- [ ] 1.9 Classify workloads: local CPU-only, local GPU, hybrid cloud rendering, cloud-first. Record bottlenecks and upgrade alternatives.
**Gate:** recommend hardware path and confidence level, not a performance promise.

## Phase 2 — Dependencies and compatibility (P0)
- [ ] 2.1 Blender stable release compatibility, Python `bpy`, background rendering, Eevee/Cycles, codec/export constraints, GPU backend and Blender version required by MCP add-ons.
- [ ] 2.2 Node.js LTS, Python supported versions, virtual environments, uv/pip, Git, FFmpeg/ffprobe, optional Docker/WSL2, n8n and Remotion.
- [ ] 2.3 Text generation: model API availability, structured output, context and token pricing, source-grounding and privacy considerations.
- [ ] 2.4 Speech: TTS engines, commercial rights, quotas, voice licensing, captions/alignment, pronunciation and multilingual needs.
- [ ] 2.5 Media: 3D asset libraries, licenses, stock footage/music/SFX, fonts, generated-image/video rights, attribution and redistribution obligations.
- [ ] 2.6 Publishing: YouTube Data API scopes/quotas, upload restrictions, analytics API, account verification, YPP eligibility and altered-content disclosure; separate public API facts from account-specific unknowns.
- [ ] 2.7 Security: MCP tool execution risks, untrusted prompts/repos, dependency pinning, secrets, network egress, sandboxing and isolation.
- [ ] 2.8 Estimate disk, RAM/VRAM, render time, API credits and monthly cost per 40-second Short and 8-minute long-form video; clearly label assumptions.
**Gate:** complete matrix; blockers and unknowns visible.

## Phase 3 — Open-source project due diligence (P0)
Candidate discovery list (unverified until audited):
- Blender official MCP initiative: https://www.blender.org/lab/mcp-server/
- blender-agent: https://github.com/hotspoons/blender-agent
- BlendRelay MCP: https://github.com/shefq/blendrelay-mcp
- blender-mcp: https://github.com/carlosh7/blender-mcp
- mcp-blender: https://github.com/RFingAdam/mcp-blender
- anim-studio: https://github.com/DvaitAI-tech/anim-studio
- MoneyPrinterTurbo: https://github.com/harry0703/MoneyPrinterTurbo
- short-video-maker: https://github.com/gyoridavid/short-video-maker
- video-maker: https://github.com/NeftalyRT/video-maker
- Blender: https://github.com/blender/blender
- Remotion: https://github.com/remotion-dev/remotion
- n8n: https://github.com/n8n-io/n8n

For **every** candidate:
- [ ] 3.1 Verify repository exists, canonical URL, latest release/commit, maintenance activity, issues, CI, release tags and documentation; do not assume popularity means quality.
- [ ] 3.2 Inspect exact SPDX license and dependency licenses; flag GPL/AGPL, dual licenses, noncommercial assets and hosted-service restrictions for legal review (do not offer legal certainty).
- [ ] 3.3 Map capabilities: scene creation, keyframes, physics, headless rendering, camera control, asset import, TTS, captioning, 9:16/16:9 and pipeline API.
- [ ] 3.4 Identify OS/Blender/Python/Node/GPU version compatibility, hardcoded assumptions and installation side effects.
- [ ] 3.5 Threat model: arbitrary Python execution, shell/network permissions, credential access, unsafe dependencies and supply-chain risks.
- [ ] 3.6 Assess tests, reproducibility, failure handling, observability and ability to pin commits.
- [ ] 3.7 Score, compare alternatives, and recommend adopt / adapt / reference only / reject with reasons.
- [ ] 3.8 If remote access unavailable, mark **unverified**; do not invent latest version, license or stars.
**Gate:** shortlist no more than two Blender integrations and two assembly engines for later approved benchmarking.

## Phase 4 — Architecture and interfaces (P1)
- [ ] 4.1 Compare (A) Blender Python templates + FFmpeg/Remotion; (B) MCP-agent-assisted Blender; (C) hybrid with generative AI video; score accuracy, cost, repeatability and control.
- [ ] 4.2 Define JSON Schema for episode, claims with citations, storyboard, scene, assets, narration, render job, QA and publication metadata.
- [ ] 4.3 Define one-source-to-many-output design: master research -> separate 9:16 and 16:9 storyboards; never assume automatic cropping is sufficient.
- [ ] 4.4 Define asset provenance, commercial rights, versioning, caching, deterministic seeds and render reproducibility.
- [ ] 4.5 Define queues, idempotency, retry policy, timeouts, checkpointing, storage retention and failure recovery.
- [ ] 4.6 Specify local-first, hybrid and cloud-first deployment options with hardware constraints and monthly budget estimates.
- [ ] 4.7 Define human approval gates for factual claims, scripts, final visual correctness and publication.
- [ ] 4.8 Define isolated Blender worker with restricted filesystem/network access; never expose credentials to AI-generated scripts.
- [ ] 4.9 Specify analytics instrumentation, experiment tagging, and measured costs per approved minute.

## Phase 5 — Proposed benchmarks, NOT authorized to execute (P1)
- [ ] 5.1 Design a 10-second reproducible Blender CPU/GPU render with exact scene, resolution, samples, memory telemetry and pass/fail; request approval before running.
- [ ] 5.2 Design a 40-second 9:16 'credit card payment' animated pilot with factual storyboard and source checks.
- [ ] 5.3 Design a 90-second 16:9 technical scene test using reusable assets.
- [ ] 5.4 Specify visual criteria: legibility on phone, motion coherence, camera continuity, physically correct representations and 1080p output.
- [ ] 5.5 Specify measured criteria: wall-clock render time, peak VRAM/RAM, failures, human corrections, cost per approved minute, file size and repeatability.
- [ ] 5.6 Define safe fallback if GPU rendering unsupported or crashes; stop on thermal/memory instability.
- [ ] 5.7 Benchmark plan must include estimated runtime, power/thermal cautions and explicit user approval before execution.

## Phase 6 — Implementation roadmap (P1; PLAN ONLY)
- [ ] 6.1 Stage A: approved environment setup, pinned dependencies and sandboxed worker; acceptance = reproducible environment.
- [ ] 6.2 Stage B: source-backed research, claims and script schemas; acceptance = cited claim traceability.
- [ ] 6.3 Stage C: 5 reusable Blender templates; acceptance = deterministic 16:9/9:16 test renders.
- [ ] 6.4 Stage D: TTS, captions and audio/video assembly; acceptance = synchronized final exports.
- [ ] 6.5 Stage E: approval UI, provenance and error recovery; acceptance = no automatic unreviewed publishing.
- [ ] 6.6 Stage F: 1 Short + 1 long-form pilot; acceptance = accuracy/quality/budget checks.
- [ ] 6.7 Stage G: 12 Shorts + 4 long-form 60-day editorial experiment; acceptance = instrumented results, not arbitrary view guarantees.
- [ ] 6.8 For every task add owner/agent, prerequisites, evidence, estimated effort range, acceptance test, rollback and stop condition.

## Phase 7 — Scoring, criticism and final review (P0)
Score each dimension 0–5: 0 absent/blocked, 1 poor, 2 weak, 3 workable with caveats, 4 strong, 5 verified excellent. Weighted score = SUM(weight * score / 5), max 100.

| Dimension | Weight |
|---|---:|
| Machine capability and sustained rendering feasibility | 20 |
| Blender pipeline functionality and accuracy | 20 |
| Dependency compatibility and reproducibility | 15 |
| Security and license/commercial suitability | 15 |
| Content quality and fact-checking design | 10 |
| Automation reliability and maintainability | 10 |
| Costs, scalability and cloud fallback | 5 |
| Observability, tests and pilot measurability | 5 |

Decision rule: >=80 GO only if no critical blockers; 65–79 CONDITIONAL GO; <65 NO-GO for current design. Any critical security, legal, hardware or unverified core capability overrides numeric score. An unknown is NOT a zero and is NOT assumed a five: score provisionally <=2, explicitly mark low confidence and show sensitivity analysis.

- [ ] 7.1 Score each project and each architecture with evidence and confidence.
- [ ] 7.2 Independently challenge the favored choice: what if Blender MCP fails, GPU lacks VRAM, dependency license blocks commercial use, or cloud costs double?
- [ ] 7.3 Identify 10 highest-impact failure modes, probability/impact/mitigation/owner and trigger.
- [ ] 7.4 Check for contradictions, missing tasks, hidden costs, unsupported assertions, unbounded agent autonomy and missing rollback.
- [ ] 7.5 Improve the plan after criticism; document changes and remaining uncertainty.
- [ ] 7.6 Report scores before and after review, but **do not fabricate measured improvement**: the score reflects plan completeness, not system readiness.
- [ ] 7.7 End with one recommended path, alternatives, explicit blockers, next approved action and questions requiring user input.

## Pre-handoff self-critique and revision record
Version 1.0 draft risks identified and corrected in v1.1:
1. Risk: 'read-only' audit could silently install or execute unsafe third-party code. Fix: strict no-change boundary and separate active-benchmark approval.
2. Risk: benchmark performance could be guessed from GPU model. Fix: distinguish documented compatibility from measured sustained performance.
3. Risk: open-source license assumed to mean unrestricted commercial use. Fix: explicit repository/dependency/asset licensing review.
4. Risk: all videos auto-cropped into Shorts. Fix: distinct 9:16 and 16:9 storyboards.
5. Risk: a composite score hides fatal issues. Fix: hard blockers override numeric score.
6. Risk: AI-generated Blender scripts access sensitive local files. Fix: sandboxed worker and no secret exposure.
7. Risk: research based on stale repository descriptions. Fix: exact URLs, dates, commits and explicit unknowns.
8. Risk: cheap API estimates ignore human work. Fix: separate variable cost, subscriptions, hardware and labor.
9. Risk: plan confuses code maturity with popularity. Fix: CI, reproducibility, maintenance and threat model.
10. Risk: an agent might start implementing immediately. Fix: planning-only deliverables and explicit approval gate.

### Plan-quality self-assessment (not an external audit)
| Aspect | Draft /5 | Revised /5 | Remaining caveat |
|---|---:|---:|---|
| Scope and deliverables | 4 | 5 | Need user's output path |
| Safety and reversibility | 2 | 5 | Read-only commands must be reviewed on host |
| Hardware diagnostics | 3 | 5 | Sustained load requires permission |
| Dependencies and licensing | 3 | 5 | Remote sources may be unavailable |
| Open-source comparison | 3 | 5 | Repos not yet inspected locally |
| Architecture realism | 3 | 4 | Render quality unproven |
| Cost modeling | 2 | 4 | API tariffs and usage unknown |
| Acceptance tests | 3 | 5 | Test execution is a later stage |
| Evidence and uncertainty | 2 | 5 | No machine inventory yet |
| Actionability | 3 | 5 | Owners/effort assigned after inspection |

**Self-assessment average: 2.8/5 draft -> 4.8/5 revised** (editorial judgment only; no machine or repository audit has yet been performed).

## Completion criteria
The audit is complete only when every P0 task is either completed with evidence or explicitly blocked, all candidate claims are attributed, the laptop capability and compatibility matrix is filled, weighted scores are reproducible, and the final plan contains executable future tasks with dependencies, effort, acceptance criteria and approval gates. **Stop after writing the reports. Do not implement.**
