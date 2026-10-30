# Agent Reach Scan — ContentFactory research sweep

Date: 2026-10-30. Tool: Agent Reach 1.6.0 (GitHub, X, YouTube, Bilibili, web/Exa).
Purpose: apply multi-platform research to the premium-3D pipeline decision.

---

## 1. Channel availability at time of scan

| Channel | Status |
|---|---|
| GitHub | works (`gh` backend) |
| YouTube | works (`yt-dlp` backend) |
| Bilibili | search works (`bili-cli`); `read` sample broken |
| Web / Exa | works |
| X / Twitter | works (`opencli`) |
| Facebook, LinkedIn | ready |
| Instagram | cooldown (429) |
| Xiaohongshu, Xueqiu API | needs login in the Agent Reach profile |
| Reddit, BOSS, Xiaoyuzhou | not added |

## 2. GitHub findings

| Repo | Relevance | Verdict |
|---|---|---|
| `kangseyoung/deadline-renderfarm-automation` | On-prem Deadline farm, PySide UI, MongoDB, NAS; 3 stars | Reference only — enterprise stack, overkill |
| `WazzaMac/renderfarm` | Blender farm install docs + script; 1 star, 2021 | Reject — stale |

Takeaway: no maintained, small, free Blender farm tool worth adopting. Remote providers and SheepIt cover the need better than DIY.

## 3. X findings

A thread notes the common Eevee-preview / Cycles-final workflow: preview fast, render final, same scene. Useful pattern; not evidence about this hardware.

## 4. YouTube findings (look-dev references)

| Video | Why relevant |
|---|---|
| "The ABSOLUTE BEST Blender Product Animation Tutorial for Beginners" — Blender Artsy | Full product-animation workflow; 16 min |
| "Product Reveal Animation Blender using Lights" — madebyomkar | Light-driven reveal — shot-1 technique |
| "How to Make Perfect Product Animations in Blender" — Aryan | Product-animation fundamentals |

Study references, not assets. Nothing is copied.

## 5. Bilibili findings

| Video | Why relevant |
|---|---|
| BV1ga4y1u7VJ — product lighting case study | 22.9k plays; product-lighting walkthrough |
| 【Blender】产品渲染课程 — 琅泽多元派 | Structured product-rendering course |
| BV1c13vzJEgd — lighting fundamentals | Basics, 4:49 |

Chinese-language tutorials cover product lighting more densely than English YouTube for this niche.

## 6. SheepIt — the important finding

A detailed user write-up (GameDev.tv, 2022):

- **Points economy, not a free queue.** Earn points by rendering others; spend them on your renders.
- **Earning is ~4× faster than spending**, so a few hours of contributing buys one render.
- Simple client setup; multiple machines can contribute.
- Your `.blend` is rendered on volunteers' machines — it leaves your control.

Implication: SheepIt is barter + IP exposure, not free on-demand compute. Viable for open test scenes only.

## 7. Consolidated recommendation

| Need | Best option | Why |
|---|---|---|
| Look-dev stills | **Local Eevee** | 43 s/frame is fine for stills |
| Final 10 s animation | **RunPod 4090 ($0.34/h)** | ~$0.02–0.10 per scene; no barter |
| Free test renders | **SheepIt after earning points** | Free only if you contribute |
| Long-form later | Remote 4090/5090 | Cents per minute at measured rates |
| DIY farm | None | No maintained small tool exists |

## 8. Workflow pattern worth adopting

1. Block and light locally in Eevee at 16 samples and half resolution.
2. Lock the look with 2–3 full-quality stills.
3. Render final animation remotely at 64 samples.
4. Keep `.blend` and assets local; upload only the packed scene.

## 9. Sources

| Source | Date |
|---|---|
| https://github.com/kangseyoung/deadline-renderfarm-automation | 2026-10-30 |
| https://github.com/WazzaMac/renderfarm | 2026-10-30 |
| https://www.youtube.com/watch?v=eaKKfF2hHF8 | 2026-10-30 |
| https://www.youtube.com/watch?v=_nl4kcb05sQ | 2026-10-30 |
| https://www.bilibili.com/video/BV1ga4y1u7VJ | 2026-10-30 |
| https://community.gamedev.tv/t/sheepit-free-render-farm-for-blender-my-experience-after-using-it-for-a-day/208771 | 2022-08-09 |
| https://www.sheepit-renderfarm.com/home | 2026-10-30 |

## 10. Limits of this scan

- One query per platform; not exhaustive.
- Instagram/Xiaohongshu/Xueqiu unavailable, so their communities were not sampled.
- Tutorials judged from titles and metadata, not watched.
- No benchmark was run.
