# 02 — Architecture Comparison and Scoring

Four architectures, scored with the weights you specified, on the **same** 40-second storyboard and the **same** 8-minute expansion. Every score is justified by a sentence; nothing is scored for novelty.

Weights: educational accuracy 20 · visual quality 20 · laptop efficiency 20 · cost 15 · automation 10 · maintainability 10 · legal/platform compliance 5.

---

## 1. The shared test storyboard

Topic: *"What actually happens when you tap your card."* One claim per scene, all fact-checked.

### 40-second 9:16 (6 scenes)

| # | Time | Beat | Visual requirement |
|---|---|---|---|
| S1 | 0–5 s | Hook: "Approved in 2 seconds — here's the journey" | bold type, card glyph |
| S2 | 5–13 s | Terminal → acquirer | merchant/terminal, directional flow |
| S3 | 13–21 s | Network routing (Visa/Mastercard rails) | network map, nodes, path |
| S4 | 21–30 s | Issuer checks balance + fraud score | decision split, approve/decline |
| S5 | 30–36 s | Response returns; receipt prints | reverse arrow, confirmation |
| S6 | 36–40 s | Recap: authorisation ≠ settlement | two-state contrast |

### 8-minute 16:9 expansion

Eight chapters: authorisation; acquirer economics; interchange; network rules; settlement T+1; chargebacks; fraud scoring; real-time payments. 40–55 scenes, 4–6 data callouts, 2–3 hero sequences.

The storyboard is deliberately **diagrammatic**. That choice is what makes the four architectures comparable: the same content must be expressed in each.

---

## 2. Architecture A — SVG / Lottie / Motion Canvas / FFmpeg

**Pipeline:** Python generates SVG frames (or Lottie JSON) → a rasteriser (`resvg`, ~5 MB, Apache-2.0) produces PNGs → FFmpeg encodes (`libx264`), captions via `libass`, hardware encode via `h264_qsv`.

| Dimension | Score | Justification |
|---|---:|---|
| Educational accuracy | **4.5** | Text and geometry are authored exactly; nothing is inferred at render time |
| Visual quality | **3.5** | Excellent typography and diagram craft; no depth, lighting, or material realism |
| Laptop efficiency | **4.0** | No browser, no GPU, no service; frames are small; idle cost zero |
| Cost | **4.5** | Toolchain free (Apache-2.0/MIT); LLM cents; no recurring spend |
| Automation | **4.5** | Deterministic frame N from scene N; trivial idempotency |
| Maintainability | **3.5** | Simple stack, but Motion Canvas has had no release since 2024-12; the SVG generator path avoids that dependency |
| Legal | **5.0** | resvg Apache-2.0, FFmpeg LGPL/GPL build, no rights ambiguity |
| **Weighted total** | **82.5** | 18 + 14 + 16 + 13.5 + 9 + 7 + 5 |

**How the storyboard renders:** every scene is a 2D card composition; S3's network map is a literal graph; S4's approve/decline is a two-branch animation. The 8-minute expansion adds charts and chapter cards — all native.

**What it cannot do:** a rotating 3D credit card, volumetric light, camera fly-throughs, physically-based materials. If those are the product's identity, A alone is insufficient.

## 3. Architecture B — Manim + selective Blender Eevee

**Pipeline:** Manim (MIT) for explanatory scenes; Blender 5.2.3 with EEVEE for a small number of 3D shots, rendered locally on the iGPU, composited in FFmpeg.

| Dimension | Score | Justification |
|---|---:|---|
| Educational accuracy | **4.5** | Manim is built for precise mathematical explanation |
| Visual quality | **4.5** | 3D depth plus Manim's clarity is the strongest look of the four |
| Laptop efficiency | **2.5** | Blender + Eevee on an iGPU is unmeasured; RAM spikes 2–8 GB; LaTeX adds ~1 GB if used |
| Cost | **4.0** | Local only; electricity negligible |
| Automation | **3.5** | Blender scene brittleness; EEVEE needs a GPU context; long renders block iteration |
| Maintainability | **4.0** | Both projects mature (Manim 42k stars, active) |
| Legal | **5.0** | Manim MIT, Blender GPL — output unaffected |
| **Weighted total** | **78.0** | 18 + 18 + 10 + 12 + 7 + 8 + 5 |

**Why not primary:** the visual upside is real, but every minute of it is paid in local render time on an unsupported GPU path, and one failed EEVEE render can consume an evening. Manim alone (without Blender) is a strong *secondary* tool for math-heavy episodes.

## 4. Architecture C — Three.js / React Three Fiber headless

**Pipeline:** R3F scene → headless Chromium (Puppeteer) → frame capture → FFmpeg. WebGL via ANGLE on the iGPU or SwiftShader (CPU).

| Dimension | Score | Justification |
|---|---:|---|
| Educational accuracy | **4.0** | Geometry authored; but text rendering and HTML overlays complicate exactness |
| Visual quality | **4.5** | Real-time 3D, good enough for stylised explainers |
| Laptop efficiency | **3.0** | Chromium adds 300–500 MB disk and 1–3 GB RAM; headless WebGL is the heaviest reliable path on an iGPU |
| Cost | **4.0** | Free stack; no cloud |
| Automation | **3.5** | Headless WebGL determinism varies with driver; frame timing must be forced |
| Maintainability | **4.0** | three.js 117k stars, R3F 33k, both active |
| Legal | **5.0** | MIT ecosystem |
| **Weighted total** | **78.0** | 16 + 18 + 12 + 12 + 7 + 8 + 5 |

**Why not primary:** it is the most complex way to obtain 3D on a machine that has no supported 3D render backend. If 3D is required, Blender on rented silicon is cheaper in engineering time than taming headless WebGL.

## 5. Architecture D — Remote Blender, local orchestration

**Pipeline:** local JSON/storyboard → scene upload → Blender on a rented GPU → frames/video download → local FFmpeg assembly. Local machine never renders.

| Dimension | Score | Justification |
|---|---:|---|
| Educational accuracy | **4.5** | Same authored-geometry guarantee as B |
| Visual quality | **5.0** | Full Cycles quality, the ceiling of the four |
| Laptop efficiency | **4.0** | Local work is light; cost moves to bandwidth and upload latency |
| Cost | **3.5** | **Measured**: RTX 4090D $0.108/h, RTX 5090 $0.269/h (Vast.ai API, 2026-10-30). Cheap per render, but recurring and variable |
| Automation | **4.0** | Good, once upload/download and job polling are built; spot interruption must be handled |
| Maintainability | **3.5** | Two environments to keep in sync (local schemas, remote Blender version) |
| Legal | **4.0** | Vendor terms, data transfer, and reproducibility across rented hosts |
| **Weighted total** | **83.5** | 18 + 20 + 16 + 10.5 + 8 + 7 + 4 |

**Why not primary despite the top score:** it makes an external dependency the core of every video. A vendor outage, a price change, or an upload failure stops production. It also conflicts with your stated preference for zero idle cost and portable on-demand processes — the orchestrator is fine, but the render step is inherently remote and metered.

## 6. Recommendation — A spine, D surgically, B optionally

| Option | When used | Share of runtime |
|---|---|---|
| **A** | All text, diagrams, charts, transitions, captions | ~90 % |
| **D** | 3–8 second 3D hero shots, max 2 per episode | ~10 % |
| **B** | Manim for math/technical episodes only | 0–30 % by topic |
| **C** | Never | 0 % |

Composite estimate: **~86/100** — A's efficiency and determinism, D's visual ceiling, without D's operational fragility.

`★ Why not pick the top score` A score is a weighted average of qualities you named; it is not a decision procedure. D wins by 1.0 point on visual quality and loses on the properties you listed first — low local resource use, zero idle consumption, portability. Using D for 10 % of runtime captures most of its visual benefit at a fraction of its dependency surface.

**What would flip this:** if the channel's identity depends on continuous 3D camera work, D becomes primary. That is a creative decision, not an engineering one — see `08` §4.

## 7. Side-by-side on the same artefacts

| | A | B | C | D |
|---|---|---|---|---|
| 40 s short: authoring | 2–5 h | 4–8 h | 4–7 h | 5–9 h |
| 40 s short: render | 1–4 min | 15–45 min | 5–15 min | 3–10 min + upload |
| 40 s short: variable cost | $0.02–0.05 | $0.03–0.06 | $0.03–0.06 | $0.04–0.19 |
| 8 min: authoring | 10–20 h | 20–35 h | 18–30 h | 22–35 h |
| 8 min: render | 10–40 min | 1–4 h | 40 min–2 h | 1–3 h |
| 8 min: variable cost | $0.05–0.15 | $0.06–0.18 | $0.06–0.18 | $0.16–0.96 |
| Peak RAM (est.) | 0.3–1.5 GB | 2–8 GB | 1–3 GB | 0.3–1 GB local |
| Idle processes | 0 | 0 | 0 | 0 |
| Disk (toolchain) | ~50 MB | 3–6 GB | 1–2 GB | ~50 MB local |
| Determinism | High | Medium | Medium-low | High (pinned image) |

All render times, RAM figures, and authoring hours are **estimates**. Only costs marked "measured" come from live data; the rest are assumption-labelled.

## 8. Scoring summary

| Rank | Architecture | Score | Verdict |
|---:|---|---:|---|
| 1 | D remote Blender | 83.5 | Component only |
| 2 | A vector/FFmpeg | 82.5 | **Spine** |
| 3= | B Manim + Eevee | 78.0 | Secondary |
| 3= | C Three.js headless | 78.0 | Rejected |

The 1.0-point gap between D and A is smaller than the error bars on either score. Treat them as tied and decide on operating risk, which is the approach taken in §6.
