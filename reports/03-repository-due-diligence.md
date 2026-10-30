# 03 — Repository Due Diligence

Verification date: 2026-10-30, via GitHub REST API and raw file fetches. No repository was cloned, no code was executed, no dependency tree was installed.
Limits: star counts and push dates are point-in-time; README claims are treated as claims and marked as such, not as verified capability.

---

## 1. Verification table

| # | Repository | Exists | Licence (SPDX) | Stars | Last push (UTC) | Latest release | Plan listed? |
|---|---|---|---:|---:|---|---|---|
| 1 | `blender/blender` | yes | NOASSERTION (site: GPL) | 21,431 | 2026-10-30 | — (mirror) | yes |
| 2 | `projects.blender.org/lab/blender_mcp` | yes | **unverified** | n/a (not GitHub) | — | v1.0.3 | yes (as blender.org/lab) |
| 3 | `ahujasid/mcp-for-blender` | yes | MIT | **32,783** | 2026-10-29 | none | **NO — omission** |
| 4 | `hotspoons/blender-agent` | yes | **NONE** | 3 | 2026-09-29 | none | yes |
| 5 | `shefq/blendrelay-mcp` | yes | MIT | 12 | 2026-10-29 | v0.7.4 | yes |
| 6 | `carlosh7/blender-mcp` | yes | MIT | 17 | 2026-08-29 | tag `docs` | yes |
| 7 | `RFingAdam/mcp-blender` | yes | **AGPL-3.0** | 33 | 2026-10-23 | v0.4.0 | yes |
| 8 | `DvaitAI-tech/anim-studio` | yes | MIT | 2 | 2026-06-30 | none | yes |
| 9 | `harry0703/MoneyPrinterTurbo` | yes | MIT | 136,437 | 2026-10-30 | v1.3.9 | yes |
| 10 | `gyoridavid/short-video-maker` | yes | MIT | 1,448 | **2025-06-21** | none | yes |
| 11 | `NeftalyRT/video-maker` | yes | MIT | 0 | 2026-01-03 | none | yes |
| 12 | `remotion-dev/remotion` | yes | Remotion License (custom) | 69,032 | 2026-10-30 | v4.0.539 | yes |
| 13 | `n8n-io/n8n` | yes | Sustainable Use (custom) | 209,105 | 2026-10-30 | n8n@2.45.7 | yes |

`★ Finding` The plan's discovery list is **inverted relative to reality**. It omits the category leader (32.8k stars) and includes four projects with fewer than 20 stars, one of which has no licence at all. Whatever produced that list did not consult current repository data.

---

## 2. Per-candidate findings

### 2.1 `blender/blender` — ADOPT (engine)

- 5.2.3 LTS is current stable; Windows 11 supported; portable ZIP available.
- Licence: Blender Foundation states GPL. GitHub's `NOASSERTION` is a licence-detection artefact, not a licence problem.
- **GPL scope:** applies to Blender and derivative builds. Rendered images/videos are **not** derivative works under the widely accepted interpretation. This is an engineering reading, not legal advice; if the channel ever ships modified Blender binaries, obligations change.
- Requirement relevant here: **Cycles GPU needs a supported backend**. This host has none (see `01`).

### 2.2 Official Blender Lab MCP — DEV SANDBOX ONLY

- Real, official, and current: release **v1.0.3**, minimum **Blender 5.1.0** (stable is 5.2.3, so it fits).
- Requires **three** manually installed pieces: the add-on, an LLM client, and the MCP server.
- Quoted from the official page: the server *"will execute LLM generated code in Blender without any guards in place to protect your data from removal or being sent to a remote location. To keep your data safe it is recommended to use a virtual machine, or a system without access to sensitive information."*
- Consequence: **unacceptable on the corporate-managed laptop as-is**, and unnecessary in a deterministic production pipeline. It is a legitimate *authoring* accelerator inside an isolated VM.
- Licence of `blender_mcp` itself: **unverified** — the repository was identified but its licence file was not fetched. Treat as unknown.

### 2.3 `ahujasid/mcp-for-blender` — REFERENCE ONLY

- The de-facto standard (32.8k stars, MIT, actively pushed). Requirements: Blender 3.0+, Python 3.10+, `uv`.
- Architecture: Blender add-on hosts a **socket server**; the MCP server sends commands including `execute_blender_code` (arbitrary Python).
- Telemetry: **on by default** as a minimal anonymous usage record; disable with `DISABLE_TELEMETRY=true`. Content capture is opt-in only.
- Risk: arbitrary code execution in a process that can read the user's files. On a domain-joined machine this is the wrong default posture.
- Verdict: useful for *learning* Blender's Python API and for one-off scene authoring; **never** in the automated render path.

### 2.4 `RFingAdam/mcp-blender` — REJECT

- AGPL-3.0 creates network-copyleft obligations if the service is ever exposed to others. 33 stars, single-maintainer, v0.4.0. External integrations download third-party models (TripoSR is not on PyPI, requiring a manual clone). Unnecessary risk for a small gain.

### 2.5 `shefq/blendrelay-mcp` — REJECT FOR NOW

- MIT, active (v0.7.4), but 12 stars and a single maintainer. It stores scene versions, agent logs and screenshots under `%LOCALAPPDATA%\BlendRelayMCP`. Interesting design (checkpoints, safe iteration), insufficient maturity to depend on.

### 2.6 `carlosh7/blender-mcp`, `hotspoons/blender-agent`, `DvaitAI-tech/anim-studio`, `NeftalyRT/video-maker` — REJECT

- `carlosh7`: 17 stars, thin README, "latest release" is a tag literally named `docs`. No evidence of production use.
- `hotspoons`: **no licence file**. Without a licence, default copyright applies and no rights are granted. Unusable in any product, regardless of quality.
- `anim-studio`: 2 stars, last push 2026-06-30, no releases.
- `video-maker`: 0 stars; README leads with a community-promotion banner. Not a maintained project.

### 2.7 `harry0703/MoneyPrinterTurbo` — ADAPT IDEAS, NOT ADOPT AS ENGINE

- 136k stars, MIT, released v1.3.9 on 2026-10-21, still pushed today. Genuinely maintained.
- Requirements are modest: Python 3.11+, 4 cores / 4 GB minimum; GPU optional. CPU-first design — which suits this host.
- Capability: **stock-footage** assembly with LLM script, TTS, subtitles, 9:16 and 16:9 outputs. It is **not** a 3D system and does not touch Blender.
- Two traps: (a) the free TTS path is **Edge TTS**, an unofficial endpoint with no commercial licence grant; (b) footage comes from third-party stock APIs whose terms vary per clip.
- Verdict: mine it for pipeline structure (script → TTS → subtitle timing → assembly → publish), do not adopt wholesale, do not ship its Edge TTS default.

### 2.8 `gyoridavid/short-video-maker` — REJECT

- 1,448 stars but **last push 2025-06-21**, ~16 months stale at audit date. No releases. Docker-based MCP assembly is attractive; the maintenance gap is not.

### 2.9 `remotion-dev/remotion` — CONDITIONAL

- 69k stars, v4.0.539, actively released. Requires headless Chromium (a sizeable download and a sandbox surface).
- Licence, quoted from `LICENSE.md`: free for *"an individual"*, *"a for-profit organization with up to 3 employees"*, and non-profits; commercial video creation is explicitly allowed. Disallowed: reselling or relicensing Remotion itself.
- The developer qualifies as an individual **today**. The licence must be re-checked if the channel becomes a company with >3 employees.
- Practical note: for a 3D-first pipeline, FFmpeg may cover assembly with fewer moving parts; Remotion earns its place only if motion-graphics overlays become central.

### 2.10 `n8n-io/n8n` — DEFER

- Sustainable Use License: *"only for your own internal business purposes or for non-commercial or personal use"*; no hosting as a service; files marked `.ee` require an Enterprise licence.
- For a single operator producing their own channel, this is compatible. For a future SaaS or client-production service, it is not.
- 209k stars and v2.45.7, but the value is orchestration of many integrations. A single-operator pipeline is better served by a small Python job runner.

---

## 3. Shortlist (per plan gate 3)

| Slot | Selection | Role |
|---|---|---|
| Blender integration #1 | **Official Blender Lab MCP v1.0.3** | Authoring accelerator inside an isolated VM only |
| Blender integration #2 | **`ahujasid/mcp-for-blender`** | Fallback authoring aid; telemetry disabled |
| Assembly engine #1 | **FFmpeg 8.1.1 (installed)** | Production assembly, concat, subtitle burn-in |
| Assembly engine #2 | **Remotion 4.0.539** | Only if overlay motion graphics become required |

No third-party Blender integration is proposed for the **production render path**. The production path is the user's own pinned Blender Python scripts.

## 4. Alternatives not in the plan

| Alternative | Why considered | Verdict |
|---|---|---|
| Manim / Motion Canvas | Deterministic programmatic animation, strong for explainers | Worth a benchmark if 3D proves too slow on CPU |
| Blender + Geometry Nodes templates | Deterministic, no Python needed for variation | Strong candidate for reusable scenes |
| After Effects + scripting | Industry standard | Rejected: licence cost, worse headless automation |
| Generative video APIs (Veo/Runway/Kling) | Fast B-roll | Conditional: cost, disclosure obligation, poor factual control |
| Direct WebGL/three.js renders | Lightweight, GPU-free servers | Rejected: visual quality below Blender for educational realism |

## 5. Derived requirements

1. Any adopted repo must have an explicit OSI licence, a release tag, and activity within 90 days.
2. Any component that executes LLM-written code must run in an isolated VM or container with no credentials mounted.
3. Telemetry must be disabled by default in any adopted tool that offers the switch.
4. Licences must be re-checked at the moment the entity changes (individual → company, personal → client work).
