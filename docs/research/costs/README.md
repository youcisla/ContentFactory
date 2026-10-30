# Cost model

Sources: `reports/v2/05-cost-resource-model-v2.md`, `reports/v2/04-tts-assets-render-v2.md`.
Labels: **[M]** measured · **[E]** estimate.

## Measured inputs

| Item | Value | Source |
|---|---|---|
| Cloud GPU — RTX 4090D | **$0.108/h** | Vast.ai public offer API, 2026-10-30 [M] |
| Cloud GPU — RTX 5090 | **$0.269/h** | same [M] |
| Free disk | 58.2 GB | local measurement [M] |
| Cycles GPU support | none on this host | vendor manual [U] |

## Variable cost per video

| Architecture | 40 s Short | 8 min long-form |
|---|---:|---:|
| A — vector spine | $0.02–0.03 | $0.05–0.12 |
| A+D — vector + hero shots | $0.04–0.17 | $0.16–0.91 |
| B — Manim + Eevee | $0.03–0.06 | $0.10–0.25 |
| D — full remote Blender | $0.04–0.17 | $0.16–0.91 |

All values **[E]** except the GPU rate they are built on. Local TTS assumed free; paid TTS adds roughly $0.01 per Short and $0.10–0.15 per long-form.

## Human cost (dominant)

| Output | Review time [E] | At €25/h |
|---|---:|---:|
| 40 s Short | 30–60 min | €12–25 |
| 8 min long-form | 3–6 h | €75–150 |

Labour is over 95 % of true cost. Compute optimisation does not change the business case; review minutes do.

## Monthly scenario — 8 Shorts + 2 long-form

| Item | A | A+D |
|---|---:|---:|
| Variable | ~$0.3 | ~$1.5 |
| Human hours | 10–14 | 11–15 |
| Human cost @ €25/h | €250–350 | €275–375 |

## Sensitivity

| Change | Effect |
|---|---|
| Render time 2× | +€0–25/month; labour unchanged |
| GPU price 2× | +$2.5/month |
| Human rate €50/h | Doubles total |
| Premium TTS | +€1–3/month |
| External SSD | +€60–100 one-off |

## What would invalidate this

1. GPU marketplace prices rising sharply or hosts becoming unreliable.
2. Review time exceeding 6 h per long-form — which would cap output at ~2 videos/month.
3. Disk forcing constant cleanup or an unplanned purchase.

Costs are reviewed whenever a benchmark produces real render times; until then, treat all wall-clock figures as estimates.
