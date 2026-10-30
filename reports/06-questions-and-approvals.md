# 06 — Questions and Approvals

Every item here blocks something. Nothing in this file has been executed.

---

## A. Questions only you can answer

### Q1 — Which host will run this? (blocks everything)

The laptop is **domain-joined to a corporate identity provider** and the shell is non-admin. Three paths:

| Option | What it means | Cost | Risk |
|---|---|---|---|
| **A1. Use the managed laptop** | Requires written confirmation that personal side projects and Blender/Docker installs are permitted | €0 | Highest — policy breach, device wipe, reputational |
| **A2. Personal machine** | Buy or reuse a second device; pipeline architecture unchanged | €0–2,000 | Lowest policy risk; hardware cost |
| **A3. Cloud-only** | Rented VM for authoring + render; local device only edits text | $40–120/mo | Data residency, recurring spend |

Default if unanswered: **no Phase A work of any kind.**

### Q2 — What is the answer from IT / the acceptable-use policy?

Specifically: (a) may third-party software be installed without elevation, (b) may a personal monetised YouTube channel be produced on this asset, (c) may project files sit on the corporate disk? A copy of the policy section is enough; I do not need credentials.

### Q3 — Disk strategy

C: has **58.2 GB free (6.2 %)**. Options: external SSD for project/render cache; cloud storage for masters; aggressive per-episode purge. Which is acceptable?

### Q4 — TTS provider

The free Edge TTS path has no commercial licence grant. A licensed provider is required before monetisation. Candidates: Azure Speech (per-character), ElevenLabs (premium quality), MiniMax, Kokoro/Chatterbox self-hosted (no per-character fee, needs local compute). Which do you want priced in detail?

### Q5 — YouTube publication

Do you already have a channel? Is it under a brand account? This determines OAuth scopes, quota project, and whether the first 10 uploads stay manual.

### Q6 — Visual language

The CPU-only constraint makes a deliberate choice matter more than usual:

| Direction | Render cost | Look |
|---|---|---|
| Low-poly / flat-shaded, orthographic | **Low** | Clean, diagrammatic, very legible on phones |
| Mid-poly with simple PBR | Medium | Modern explainer |
| Photoreal / glass / volumetrics | **Very high on CPU** | Impressive but likely impractical here |

Recommendation: low-poly diagrammatic for the first 20 videos; revisit after the benchmark.

### Q7 — Budget ceiling

What monthly variable spend is acceptable for TTS + cloud render + LLM? A number lets me pick the render tier rather than hedge.

### Q8 — Correction policy

If a published video contains an error, what is the standard: silent re-upload, pinned comment, or public correction? This determines whether the pipeline needs a re-render + re-publish path from day one.

---

## B. Actions requiring explicit approval (none performed)

| # | Action | Why it needs approval | Blocked on |
|---|---|---|---|
| P1 | Install Blender 5.2.3 portable into a project subfolder | Software installation on a managed device | Q1, Q2 |
| P2 | Create a Python 3.12 `uv` environment | Adds packages to the device | Q1 |
| P3 | Start Docker Desktop / WSL Ubuntu | State change, service start | Q1, Q2 |
| P4 | Clone any candidate repository | Explicitly forbidden by the audit boundary | — |
| P5 | Run benchmark B1 (10 s Cycles CPU render) | Compute load, thermal, writes output files | P1, Q3 |
| P6 | Run benchmarks B2/B3 (40 s / 90 s) | Longer load, larger disk use | P5 passing |
| P7 | Create TTS/LLM API accounts and spend money | Cost + credentials | Q4, Q7 |
| P8 | Rent cloud GPU | Recurring spend, data upload | Q1, Q7 |
| P9 | Upload anything to YouTube | Public, irreversible | Q5, G5 gate |
| P10 | Purchase stock/music/asset licences | Spend, legal terms | Q7 |

---

## C. What I recommend as the single next step

**Answer Q1 and Q2.** Everything else is downstream. If the answer is "personal machine" or "policy permits", I will propose a 90-minute Phase A that ends with a measured B1 benchmark — the one number that decides whether the visual language is low-poly diagrammatic or something richer.

If the answer is "managed device only, no installs", the correct pivot is a **cloud-only pipeline** (A3); the architecture in `04` survives with the render plane moved, and only the cost line changes.

---

## D. Confirmed boundary

This audit did not install, clone, download to a build location, benchmark, or modify anything. The only writes are the seven report files and the `evidence/` captures under `reports/`, which you approved. Investigation stops here pending your answer.
