# Open-source project assessment

Verified 2026-10-30 via the GitHub API and raw licence files. No repository was cloned or executed.
Full detail: `reports/03-repository-due-diligence.md` and `reports/v2/03-publishing-tools-v2.md`.

## Blender / 3D integrations

| Project | Licence | Stars | Verdict |
|---|---|---:|---|
| `blender/blender` | GPL | 21,431 | Adopt engine; not on this host for Cycles |
| `projects.blender.org/lab/blender_mcp` v1.0.3 | unverified | — | Sandbox only — vendor states it runs LLM code with no guards, requires Blender 5.1+ |
| `ahujasid/mcp-for-blender` | MIT | **32,783** | Reference only; missing from the original candidate list |
| `RFingAdam/mcp-blender` | AGPL-3.0 | 33 | Reject |
| `shefq/blendrelay-mcp` | MIT | 12 | Reject for now |
| `carlosh7/blender-mcp` | MIT | 17 | Reject |
| `hotspoons/blender-agent` | **none** | 3 | **Reject — no licence means no rights** |
| `DvaitAI-tech/anim-studio` | MIT | 2 | Reject |
| `NeftalyRT/video-maker` | MIT | 0 | Reject |

## Video / animation tooling

| Project | Licence | Stars | Verdict |
|---|---|---:|---|
| `ManimCommunity/manim` | MIT | 42,018 | Secondary, math topics |
| `motion-canvas/motion-canvas` | MIT | 19,597 | Optional authoring — **no release since 2024-12-14** |
| `mrdoob/three.js` | MIT | 117,220 | Rejected as primary |
| `pmndrs/react-three-fiber` | MIT | 33,365 | Rejected as primary |
| `puppeteer/puppeteer` | Apache-2.0 | 95,770 | Rejected — heaviest path |
| `Zulko/moviepy` | MIT | 15,057 | Optional convenience |
| `remotion-dev/remotion` | Remotion License | 69,032 | Conditional — free for individuals and ≤3-employee orgs |
| `linebender/resvg` | Apache-2.0 | 4,164 | **Adopt — core rasteriser** |
| `thorvg/thorvg` | MIT | 1,898 | Reference if Lottie needed |

## Publishing

| Project | Licence | Stars | YouTube | Verdict |
|---|---|---:|---|---|
| Postiz | AGPL-3.0 | 40,185 | **No provider in OSS tree** | Reject for this workload |
| OpenPost | AGPL-3.0 | 839 | Yes | Defer — only if multi-platform |
| Mixpost | MIT core | 3,890 | Yes | Reject — stale ~7 months, always-on |
| YouTube Data API | Google terms | — | Native | **Adopt** (ADR-0003) |

## Assembly / orchestration

| Project | Licence | Stars | Verdict |
|---|---|---:|---|
| `n8n-io/n8n` | Sustainable Use (fair-code) | 209,105 | Defer — overkill, always-on |
| `harry0703/MoneyPrinterTurbo` | MIT | 136,437 | Adapt ideas only — stock footage, Edge TTS default |
| `gyoridavid/short-video-maker` | MIT | 1,448 | Reject — stale 16 months |

## Standing rules

1. No dependency without an explicit OSI licence and activity within 90 days.
2. Any tool that executes LLM-written code runs only in an isolated VM or container.
3. Telemetry is disabled where a switch exists.
4. Popularity is not quality — stars are recorded, not trusted.
