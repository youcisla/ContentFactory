# 00 — Executive Decision

Audit date: 2026-10-30 (local, UTC+01:00)
Auditor: Claude Code (DeepSeek) — read-only preflight. No installations, no builds, no benchmarks executed.
Scope contract: `AI_3D_Video_Factory_Preflight_Plan.md` v1.1 + `Claude_Code_DeepSeek_Preflight_Prompt.md`

---

## Verdict

**CONDITIONAL GO — but not in the shape the plan assumes.**

| Question | Answer | Confidence |
|---|---|---|
| Can this laptop run the pipeline as originally framed (local Blender + local GPU render)? | **NO-GO** | High — measured |
| Can it author, iterate, and render short CPU test scenes? | **CONDITIONAL** | Medium |
| Is there a viable commercial path from here? | **YES, with 3 conditions** | Medium-high |

The original framing presumed a local GPU-accelerated 3D factory. Measurement disproves that premise: there is no discrete GPU, Cycles does not support the integrated Intel adapter, and the device is corporate-managed.

## Machine verdict (one line)

**Adequate CPU and RAM for Blender authoring; no supported Cycles GPU; insufficient free disk for a production media library; and not a device on which unvetted installations should be assumed permissible.**

## Top 3 blockers

### B1 — Corporate-managed device (highest severity, lowest certainty about consequences)

`Win32_ComputerSystem.PartOfDomain = True` (corporate domain withheld); the shell runs **non-admin**. Every component in this plan (Blender, Python packages, Docker images, browser automation) would need either elevation, a policy exemption, or vendor approval. Acceptable use for a **personal monetised YouTube channel** on an institutional asset is an open question only the user or IT can answer. This audit cannot resolve it and must not assume it away.

Impact: gates Phase A of any build. Not technically fatal — fatal only if policy forbids it.

### B2 — No discrete GPU; Cycles unsupported on the integrated adapter

Measured: single display adapter `Intel(R) Graphics`, driver 32.0.101.8860 (2026-06-25), no `nvidia-smi`, no second adapter. The Blender 5.2 LTS manual states the Intel Cycles backend (oneAPI) "requires an Intel® Arc™ graphics card with the Xe HPG architecture". An Arrow Lake-U integrated GPU is not an Arc part.

Therefore **Cycles renders on CPU only** (12 cores). EEVEE can use the iGPU through OpenGL 4.3 / Vulkan 1.3, but EEVEE is a rasteriser — weaker for the physically-correct explanatory visuals (light, materials, transparency) that educational 3D relies on.

Secondary: **C: has 58.2 GB free of 943.7 GB (6.2 %)**. One project with cached textures, EXRs and intermediates can consume 20–60 GB. That is a hard operational ceiling.

### B3 — Unvalidated legal and execution surface

Four exposures, verified from primary sources:

1. **Official Blender Lab MCP ships an explicit warning** that it "will execute LLM generated code in Blender without any guards in place to protect your data", recommending a VM. Running it on a domain-joined machine holding institutional credentials is a direct conflict.
2. **Edge TTS** (MoneyPrinterTurbo's free default) is an unofficial consumer endpoint, not a licensed commercial TTS API. Using it in monetised output is a rights risk.
3. **Remotion and n8n are not OSI open source.** Remotion is free for individuals and ≤3-employee organisations (the developer qualifies today; a future company may not). n8n's Sustainable Use License permits personal/internal use but forbids hosting it as a service.
4. **YouTube requires disclosure** of realistic AI-generated or altered content. Design must include the disclosure flag, not bolt it on later.

No legal certainty is offered; these are flags for the user's own review.

## What the audit changed in the plan

| Plan v1.1 assumption | Verified reality |
|---|---|
| Candidate list is representative | The dominant project, `ahujasid/mcp-for-blender` (32,783 stars, MIT), was **missing**; four listed candidates have 0–17 stars |
| Blender MCP is an emerging experiment | An **official** Blender Lab MCP exists (v1.0.3) but requires Blender **5.1+** and is explicitly unsafe by default |
| GPU compatibility is a "check later" item | It is **decisive**: no supported Cycles GPU exists on this host |
| Machine ownership is a Phase 0 checkbox | It is **blocker #1** and reframes the hardware path |
| YouTube quota = 10,000 units, upload = 1,600 | Current API gives `videos.insert` its **own bucket of 100 uploads/day** |
| Free/open-source implies commercially usable | Remotion, n8n, and Edge TTS each carry material conditions |

## Required conditions for GO

1. **B1 resolved in writing** — written confirmation that personal side projects are permitted on this device, or the pipeline runs on a personal machine.
2. **Rendering moved off the iGPU** — CPU-only Cycles with a deliberately low-complexity visual language, or a cloud GPU render step (rented, batched).
3. **Deterministic spine** — LLM/MCP may author scenes, but the production render path is fixed Python templates with pinned versions and hashed inputs. No agent in the publish loop.

If all three hold: CONDITIONAL GO, proceed to Phase A on written approval.
If B1 cannot be resolved: migrate to personal hardware; the software architecture survives unchanged.

## Numbers at a glance

| Item | Value | Basis |
|---|---|---|
| Weighted readiness score (as designed, this host) | **54 / 100** | Measured + verified; see `05` |
| Weighted score after redesign (hybrid, cloud render) | **66 / 100** | Projection, labelled |
| Variable cost, 40 s Short | **$0.05 – $3** | Assumption-labelled; see `04` |
| Variable cost, 8 min long-form | **$0.5 – $6** | Assumption-labelled; see `04` |
| Human review per finished minute | **20 – 45 min** | Estimate — dominant cost |
| Free disk headroom | **58.2 GB** | Measured |

## Single next action requiring approval

Choose the host path (see `06-questions-and-approvals.md`, Q1). Nothing else can be sequenced until that is answered. No installation, download, or benchmark is authorised by this report.
