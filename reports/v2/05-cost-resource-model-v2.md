# 05 — Cost and Resource Model v2

Rule applied throughout: **[M]** measured · **[U]** verified upstream · **[E]** estimate. No estimate is presented as a measurement, and every estimate names its assumption.

---

## 1. Measured inputs (this machine, 2026-10-30)

| Fact | Value | Tag |
|---|---|---|
| Usable RAM | 31.5 GB (8.7 GB free at audit) | [M] |
| Free disk C: | 58.2 GB of 943.7 GB (6.2 %) | [M] |
| CPU | Intel Ultra 7 255U, 12 cores / 14 threads | [M] |
| GPU | Intel integrated only; no Cycles backend | [M]/[U] |
| FFmpeg | 8.1.1 with libx264, libx265, **h264_qsv**, drawtext, libass; **no SVG decoder** | [M] |
| Cloud GPU price | RTX 4090D **$0.108/h**; RTX 5090 **$0.269/h** | [M] Vast.ai offer API |

## 2. Toolchain footprint (estimated, per architecture)

| Architecture | Install size | Idle RAM | Idle processes | Disk per 8-min episode |
|---|---:|---:|---:|---:|
| **A** vector + FFmpeg | ~50 MB (resvg + Python stdlib) | 0 | 0 | 2–6 GB (frames + proxies + master) |
| **B** Manim + Blender Eevee | 3–6 GB (Blender 1.5, MiKTeX ~1, Python libs) | 0 | 0 | 15–40 GB (EXR + renders) |
| **C** Three.js + Chromium | 1–2 GB | 0 | 0 | 3–8 GB |
| **D** remote Blender | ~50 MB local | 0 | 0 | 1–3 GB local cache |

All size figures are **[E]**. Only the disk ceiling (58.2 GB) is measured.

## 3. Variable cost per output

### 40-second Short

| Line | A | B | C | D |
|---|---:|---:|---:|---:|
| TTS (local, Chatterbox/Kokoro) | $0.00 | $0.00 | $0.00 | $0.00 |
| LLM (script/claims/storyboard) | $0.02 | $0.02 | $0.02 | $0.02 |
| Render (local electricity) | $0.00–0.01 | $0.01–0.03 | $0.01–0.02 | — |
| Render (cloud) | — | — | — | **$0.02–0.14** |
| Storage/egress | $0.00 | $0.00 | $0.00 | $0.00–0.01 |
| **Total** | **$0.02–0.03** | **$0.03–0.06** | **$0.03–0.05** | **$0.04–0.17** |

### 8-minute long-form

| Line | A | B | C | D |
|---|---:|---:|---:|---:|
| TTS (local) | $0.00 | $0.00 | $0.00 | $0.00 |
| LLM | $0.05–0.10 | $0.05–0.10 | $0.05–0.10 | $0.05–0.10 |
| Render (local electricity) | $0.00–0.02 | $0.05–0.15 | $0.02–0.06 | — |
| Render (cloud) | — | — | — | **$0.11–0.81** |
| **Total** | **$0.05–0.12** | **$0.10–0.25** | **$0.07–0.16** | **$0.16–0.91** |

### Premium TTS sensitivity

If local TTS quality is rejected and a paid provider is used, add roughly **$0.01 per Short** and **$0.10–0.15 per long-form** at list prices. This does not change any architecture ranking; it is noise next to labour.

## 4. Human cost (the dominant line)

| Output | Review time [E] | Cost at €25/h |
|---|---:|---:|
| 40 s Short | 30–60 min | €12–25 |
| 8 min long-form | 3–6 h | €75–150 |

Labour is **>95 %** of true cost in every architecture. Any optimisation that does not reduce review minutes is financially irrelevant.

## 5. Monthly scenario — 8 Shorts + 2 long-form

| Architecture | Variable cost | Human hours | Human cost @ €25/h | Total |
|---|---:|---:|---:|---:|
| A | ~$0.3 | 10–14 h | €250–350 | **€250–350** |
| A+D | ~$1.5 | 11–15 h | €275–375 | **€275–375** |
| B | ~$0.6 | 14–20 h | €350–500 | **€350–500** |
| C | ~$0.5 | 13–18 h | €325–450 | **€325–450** |
| D | ~$2.5 | 12–17 h | €300–425 | **€300–425** |

Fixed costs (none required): €0. Optional: cloud storage €0–5/mo, TTS subscription €0–22/mo.

## 6. Sensitivity

| Scenario | Effect on monthly total | Changes ranking? |
|---|---|---|
| Render time 2× | +€0–25 (labour unchanged) | No |
| GPU price 2× | +$2.5 | No |
| Human rate €50/h | **doubles** total | No, but makes automation of review the only lever |
| Local TTS rejected → paid TTS | +€1–3 | No |
| Disk forces external SSD | +€60–100 one-off | No |
| Corporate device disallowed → personal laptop | +€0–2,000 capex | **Decision-level** |

## 7. Resource behaviour during production

| Architecture | Peak RAM | CPU during render | Disk churn | Typ. render wall clock |
|---|---:|---|---|---|
| A (10 s scene) | 0.3–0.8 GB | 1–2 cores | ~50–150 MB | 5–20 s [E] |
| A (8-min) | 0.5–2 GB | 2–4 cores | 2–6 GB | 10–40 min [E] |
| B (10 s Eevee) | 2–6 GB | 2–12 cores + iGPU | 0.5–2 GB | 2–10 min [E] |
| B (8-min) | 3–10 GB | 8–12 cores | 15–40 GB | 1–4 h [E] |
| C (8-min) | 1–3 GB | 2–8 cores + iGPU | 3–8 GB | 40 min–2 h [E] |
| D (8-min) | 0.3–1 GB local | ~1 core | 1–3 GB | 1–3 h incl. transfer [E] |

`★ Constraint` B's 8-minute render at 3–10 GB RAM runs against an idle-free baseline of 8.7 GB. It fits only if the browser and agent processes are closed — an operational rule, not a guarantee.

## 8. Disk budget against the measured ceiling

| Item | A | B | C | D |
|---|---:|---:|---:|---:|
| Toolchain | 0.05 GB | 3–6 GB | 1–2 GB | 0.05 GB |
| Per 8-min episode | 2–6 GB | 15–40 GB | 3–8 GB | 1–3 GB |
| Episodes before hitting 15 GB reserve | ~7–20 | **1–2** | ~5–15 | ~15–40 |

This is the quiet argument for A: on a 58 GB-free disk, B supports **one** long-form episode in flight, A supports a working library.

## 9. Cost conclusion

1. Compute is not the constraint. At measured prices, even the cloud path costs under **$1 per long-form**.
2. Disk and human review are the real constraints.
3. A is cheapest and lightest; D buys visual quality for under $1/video; B buys the same quality with local time and disk.
4. The financial case for any architecture is decided by **review minutes per published minute**, not by render price.
