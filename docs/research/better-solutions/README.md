# Better Solutions — Agent Reach + last30days sweep

Date: 2026-10-30. Tools: Agent Reach 1.6.0 (web/Exa, GitHub, YouTube) and last30days 3.3.2 (Reddit, Hacker News, GitHub, 30-day window).
Purpose: find options better than the current decision — local Eevee stills + RunPod 4090 finals + SheepIt tests.
Read-only. Nothing installed, nothing purchased, nothing rendered.

---

## 1. What this sweep corrects

The earlier scan concluded "no maintained, small, free Blender farm tool exists." **That was wrong.**

| Claim in `agent-reach-scan/` | Correction |
|---|---|
| "No maintained small Blender farm tool" | **LogicReinc.BlendFarm** — 533 stars, GPL-3.0, C#, cross-platform, pushed 2025-02, v1.1.6. Free LAN renderer with auto node discovery. |

The conclusion still holds for *this* project, but for a different reason: BlendFarm needs a second machine. With one laptop it adds nothing. Its release notes also record that **headless Eevee rendering can be unreliable** on render nodes — the exact engine we depend on.

---

## 2. The category that did not exist in the earlier scan: agent-native render APIs

The last30days engine surfaced this independently, from three sources in the 30-day window (`agmmnn/awesome-blender#122`, `docker/mcp-registry#5440`, `cline/mcp-marketplace#2767`).

**JANCTION Render** is a cloud Blender farm exposed as a remote MCP server at `https://render.janction.jp/mcp`.

| Property | Value |
|---|---|
| Input | `.blend`, `bpy` script, or glTF/FBX/USD/STL |
| MCP tools | `render_preview`, `render_estimate`, `render_final`, `render_status`, `render_download`, `scene_info`, `asset_search`, `billing`, `render_share` |
| Engine | Cycles **and Eevee** |
| GPU | NVIDIA RTX PRO 6000 (96 GB) |
| Free | 100 JPY welcome credit, no card (~1,000 GPU-seconds); +400 JPY if a card is saved; **2 free preview GPU-minutes/day** at 1080p |
| Paid | **0.1 JPY per GPU-second** ≈ 360 JPY/h ≈ **$2.35–2.40/h** |
| Caps | Default 3,000 JPY/job, 10,000 JPY/day, per-key configurable |
| Licence | GPL-3.0-or-later Blender extension |

### Cost per 10-second scene

| Path | Time | Cost |
|---|---|---|
| Local Eevee (measured) | 170 min | €0 |
| RunPod 4090 (est. 1–2 s/frame) | 4–8 min | $0.02–0.05 |
| **JANCTION (est. 1–2 s/frame)** | 4–8 min | **$0.16–0.32** |
| Managed farm (scaled from §3) | — | ~€0.60–1.50 |

**JANCTION is ~7× RunPod per GPU-second.** For a 10-second scene that difference is **$0.10–0.27** — smaller than the cost of the time spent provisioning a RunPod instance by hand.

**Why this matters to CF-022.** The 7× premium buys: no instance provisioning, no remote Blender install, no file-transfer scripting, no teardown. The agent calls a tool. At three scenes a week that is under $1/month of premium for removing an entire manual subsystem from the automation path.

**Caveat.** The free preview tier (2 GPU-min/day ≈ 120 GPU-seconds) is *less than one* 10-second render at 1 s/frame (240 GPU-seconds). It funds look-dev, not finals.

---

## 3. How expensive managed farms really are

Drop & Render published an identical-job benchmark (2026-04-27): 500 frames, 5 min/frame, single RTX 4090.

| Farm | Cost | Render time |
|---|---:|---|
| SheepIt | **€0** | not shown |
| Drop & Render | €190 | 1h 11m |
| GridMarkets | €201 | 11h |
| Fox Render Farm | €205 | not shown |
| GarageFarm | €230 | 3h 41m |
| Ranch Computing | €467 | 49m |
| RebusFarm | €486 | not shown |

That job is 2,500 frame-minutes. A 10-second 24 fps scene at 1–2 s/frame is **4–8 frame-minutes** — roughly 1/400th. Scaled, a managed farm costs about **€0.60–1.50** for our scene.

Independent confirmation: Superluminal's own 12-run benchmark reports $0.14–$1.90 per job.

**Verdict: managed farms are not a price competitor to raw GPU rental.** They sell setup convenience. For a batch of one scene at a time, that convenience is cheaper to buy from JANCTION than from a €200-tier farm.

---

## 4. Free options — what actually changed

| Option | Verdict change |
|---|---|
| **Modal Starter** ($30/month credit) | **Upgraded from "worth evaluating" to "validated".** A public working script exists: `cloud/modal_blender.py` in `rheos/secondunit-videos` PR #173 (2026-10-16). Runs Blender 5.2.2 / 4.5.14 in Modal containers; modes `probe` (CPU), `stills`, `full` (split across N containers, MP4 assembled locally). `ORB_GPU=cpu` renders EEVEE on Mesa software GL. |
| **SheepIt** | Confirmed €0 at scale by an independent benchmark. Barter economics and `.blend` exposure unchanged from `render-alternatives/`. |
| **JANCTION free tier** | New. ~1,000 GPU-seconds + 2 preview-min/day. Enough to validate one scene, not to run weekly. |
| **Sceneplane** | New. MCP/API, 30 free compute minutes/month, no card. |
| **TURNA** | New. €25 free credit, no card. Then €4.90/h single machine. |
| Colab / Kaggle / Lightning / HF ZeroGPU | Unchanged from `render-alternatives/`. |

---

## 5. Other 2026 entrants

| Service | Model | Relevance |
|---|---|---|
| **TURNA** | Blender-only add-on, €4.90/h (1 machine) to €49.90/h (8), Cycles+Eevee, RTX 5090/4090, EU hosts only | Expensive per hour, but the **in-Blender cost estimate before upload** is the UX worth copying |
| **Praxilla** | €2.50/GPU-hour, up to 15 nodes, EU storage purged after 2 weeks | Cheaper than TURNA, still 7× RunPod |
| **Rendertz Studio** | Blender extension, **EEVEE Next**, A10G / multi-GPU up to 96 GB, billed only during ray-tracing | One-click cloud rendering inside Blender |
| **Farpy** | Pay-per-frame, no subscription, **failed frames free**, Blender + Octane, launched 2026-07 | Failure-free pricing is the differentiator |
| **EvaFarm** | Public read-only MCP at `https://evafarmstore.ru/mcp`; `list_nodes` returns live GPU availability and hourly rates | Useful for **programmatic price discovery** before booking |
| **RenderStreet** | Established, has a dedicated **EEVEE-optimised** farm page | Only established farm marketing Eevee specifically |

---

## 6. Look-dev references that match our exact Blender

Agent Reach YouTube returned five, two of which are Blender 5.x + Vulkan specific — the version we have installed (5.2.3).

| Video | Length | Views | Why |
|---|---:|---:|---|
| Blender Guru — "How to use Eevee — Full Blender Course" | 77 min | 633k | Reference course |
| **Gleb Alexandrov — "How to Render REALISM in Seconds with EEVEE \| Blender 5 Course"** | 4:51 | 68k | **Blender 5.x + Vulkan — matches our install** |
| **Extra 3d — "Photorealistic Eevee Renders In Blender 5.1"** | 15 min | 145k | **Blender 5.1 — closest to 5.2.3** |
| Edin Spiegel — "How to make EEVEE Next look like Cycles" | 4:01 | 108k | Closes the Eevee/Cycles gap |
| Ryan King Art — "How to Make Eevee More Realistic" | 11 min | 195k | Fundamentals |

Not watched — judged from metadata. Watching one before V4 is still an open task.

---

## 7. Recommendation delta

| Need | Before | Now |
|---|---|---|
| Look-dev stills | Local Eevee | Local Eevee (unchanged) |
| Final 10 s render | RunPod 4090 | **RunPod 4090 stays primary; JANCTION is the automation path** |
| Agent-driven render (CF-022) | Not addressed | **JANCTION MCP** — no provisioning, no remote install |
| Free burst | Modal "worth evaluating" | **Modal validated** — public script, $30/month |
| Free fallback | SheepIt | SheepIt (unchanged, €0 confirmed) |
| Multi-machine | None | BlendFarm if a second machine appears |
| Look-dev reference | Tutorials from metadata | **Two Blender 5.x/Vulkan-specific videos identified** |

### The principle this sweep establishes

Render cost is no longer the constraint and cannot become one. At $0.02–$0.40 per scene across every option examined, a 40-video quarter costs **under $16** on the most expensive path. The constraint is **iteration count and scene quality**, which is exactly what V4 measures. Do not optimise render price further; optimise how often the look can be re-shot.

---

## 8. Sources

| Source | Date |
|---|---|
| https://render.janction.jp/blender-render-farm | 2026-10-30 |
| https://render.janction.jp/faq | 2026-10-30 |
| https://github.com/JasmyLab-JANCTION/janction-render | 2026-10-30 |
| https://github.com/agmmnn/awesome-blender/pull/122 | 2026-10-15 |
| https://github.com/docker/mcp-registry/pull/5440 | 2026-10-05 |
| https://github.com/rheos/secondunit-videos/pull/173 (Modal Blender lab) | 2026-10-16 |
| https://dropandrender.com/blog/ultimate-render-farm-comparison-2026 | 2026-04-27 |
| https://superlumin.al/compare/blender-render-farms | 2026-07-29 |
| https://geturna.com/en/blender-render-farm | 2026-10-30 |
| https://render.st/engine-blender-eevee/ | 2026-10-30 |
| https://github.com/LogicReinc/LogicReinc.BlendFarm | 2025-02-02 |
| https://github.com/jaw9c/awesome-remote-mcp-servers/pull/1175 (EvaFarm) | 2026-10-08 |

## 9. Limits of this sweep

- JANCTION, TURNA, Praxilla, Farpy, Rendertz and Sceneplane pricing read from vendor pages, not invoices.
- The 1–2 s/frame Eevee estimate on any GPU remains **unmeasured**. CF-023 exists to replace it.
- Video tutorials judged from titles and metadata, not watched.
- last30days could not reach X, YouTube or TikTok in this run (3 sources returned: GitHub, Hacker News, Reddit; its config file reports permissions 644 and should be `chmod 600`).
- New-entrant services are young; all launched or pivoted in 2026. Vendor stability is unproven.
- No benchmark run. No account created. No spend.
