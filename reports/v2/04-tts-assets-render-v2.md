# 04 — TTS, Video Editing, Assets, Rendering Services

All licences below were taken from the repository licence file or the vendor's own licence page on 2026-10-30 unless marked otherwise.
Tags: **[U]** verified upstream · **[M]** measured locally · **[I]** inferred/unverified · **[E]** estimate.

---

## 1. Text-to-speech

| Engine | Licence | Params | CPU viability | Maintenance | Commercial output |
|---|---|---|---:|---|---|
| **Chatterbox-Turbo** (Resemble AI) | **MIT** [U] | 350M | **Vendor: 3× faster than realtime on 8 CPU cores** [U] | Active, 27,419 stars, pushed 2026-07-21 [U] | Yes — MIT, but voice-cloning consent is on you |
| **Kokoro-82M** | **Apache-2.0** weights [U] | 82M | Designed lightweight; ONNX CPU path [U] | 9,785 stars, last push 2025-08-06 (~14 months) [U] | Yes — Apache-2.0 |
| **Piper 1 (OHF-Voice)** | **GPL-3.0** [U] | small | Very fast on CPU; the classic offline choice | 6,089 stars, active 2026-10-25 [U] | Yes for output; **GPL obligations if you distribute the binary/derivative** |
| rhasspy/piper (old) | MIT | — | — | **ARCHIVED** 2025-08-26 [U] | Do not start here |
| Edge TTS | Unofficial service | — | — | Endpoint can change without notice | **No licence grant** — reject for monetised output |
| Azure Speech | Commercial terms | — | cloud | Mature | Yes, paid per character |
| ElevenLabs | Commercial terms | — | cloud | Mature | Yes, paid; premium quality |
| Coqui XTTS | Repo MPL-2.0, **weights CPML (non-commercial)** [I] | — | — | Repo dead since 2024-08 [U] | **No** — non-commercial weights |

**Recommendation:** start with **Chatterbox-Turbo** (MIT, CPU-targeted, active). Keep **Kokoro** as fallback if Turbo's CPU claim fails in practice. Avoid Edge TTS for anything monetised. Use Azure/ElevenLabs only if local quality is judged insufficient after a listen test.

`★ Caution` "3× faster than realtime on 8 CPU cores" is a **vendor claim**, not a measurement on this machine. The benchmark in `07` includes one sentence of TTS only if you approve the model download; otherwise treat it as unverified.

## 2. Video editing and encoding

| Tool | Licence | Status | Fit |
|---|---|---|---|
| **FFmpeg 8.1.1** | LGPL/GPL depending on build (gyan.dev full build = GPL) | **Installed** [M] | Spine. Verified capabilities below |
| MoviePy | MIT | 15,057 stars, active 2026-08-26 [U] | Python compositing; optional convenience layer over FFmpeg |
| Remotion | Remotion License (free ≤3 employees / individual) | 69k stars, active | Only if React-based motion overlays become central |
| Kdenlive / Shotcut | GPL | mature | GUI editors; not needed in an automated path |

### Measured FFmpeg capabilities on this host [M]

| Capability | Result |
|---|---|
| `drawtext` (libfreetype) | present |
| `subtitles` / `ass` (libass) | present |
| `libx264`, `libx265` | present |
| **`h264_qsv`, `hevc_qsv`** (Intel Quick Sync) | **present** — hardware encode available |
| `svg_pipe` demuxer | present |
| **SVG decoder** | **absent** — FFmpeg cannot rasterise SVG by itself |

Consequence: the vector pipeline needs one rasteriser. `resvg` (Apache-2.0, 4,164 stars, active) is a single static binary of roughly 5 MB — the smallest credible dependency in this entire plan.

## 3. Asset libraries

| Source | Licence | Verified | Commercial use | Notes |
|---|---|---|---|---|
| **Poly Haven** | **CC0** | Yes — "all licensed as CC0" [U] | Yes | HDRIs, textures, models; no attribution required |
| **Kenney** | CC0 | Yes — "Can I use the game assets in a (commercial) project? Yes" [U] | Yes | 2D/3D game assets, UI, audio |
| **ambientCG** | CC0 | Site states CC0 [I] — licence text not captured this pass | Yes | PBR materials |
| Google Fonts | OFL (per family) | [I] | Yes | Font redistribution terms apply to the font files, not the rendered video |
| Pexels | Pexels Licence | **Not verified — HTTP 403** [I] | Yes, with restrictions | Cannot resell unaltered copies; no implied endorsement |
| Pixabay | Content Licence | **Not verified — HTTP 403** [I] | Yes, with restrictions | Similar restrictions |
| Sketchfab | Per-asset | [I] | Varies | Must check each model; NC licences unusable |
| Freesound | Per-sound (CC0/CC-BY/CC-BY-NC) | [I] | Varies | Filter by licence before download |

**Rule for the pipeline:** every asset row carries `licence_spdx`, `licence_evidence_sha256`, `commercial_ok`. Assets with `commercial_ok=false` fail validation. This is the only reliable defence against licence contamination at volume.

## 4. Rendering services (3D, optional)

| Provider | Price | Basis | Notes |
|---|---|---|---|
| **Vast.ai** | **RTX 4090D $0.108/h · RTX 5090 $0.269/h** | **Measured** — public offer API, 2026-10-30 [M] | Marketplace of independent hosts; reliability varies per host |
| RunPod | ~$0.2–0.8/h (community/secure cloud) | [E] — pricing page did not expose numbers to text extraction | Mature tooling, per-second billing |
| Lambda | ~$0.5–2/h | [E] — page not machine-readable this pass | Higher-end GPUs, research focus |
| Replicate / fal.ai | per-second / per-call | [E] | Convenient APIs, higher unit cost |

**Cost implication:** an 8-minute Blender render occupying 1–3 GPU-hours costs **$0.11–$0.81** at measured Vast rates. This is far below v1's $1–4 estimate and is the single biggest revision in this pass.

**Risk:** marketplace hosts are interruptible and heterogeneous. A render that must be reproducible needs a pinned image and idempotent job design, not just a cheap offer.

## 5. Legal summary

| Item | Position | Confidence |
|---|---|---|
| Blender output ownership | Renders are not derivative works of Blender | High (widely accepted, not legal advice) |
| Chatterbox / Kokoro output | MIT / Apache-2.0 permit commercial use | High |
| Piper1 output | Fine; **binary distribution** triggers GPL | High |
| Edge TTS | No commercial grant | High |
| CC0 assets | No attribution, no restriction | High |
| Pexels/Pixabay | Commercial use allowed with restrictions | Medium — pages blocked, terms not re-read |
| YouTube AI disclosure | Required for realistic synthetic content | High [U] |
| Cloud GPU terms | Vendor-specific; data leaves the device | Medium |

## 6. What remains unverified

1. Pexels and Pixabay licence text (403 on fetch).
2. ambientCG licence text (site summary only).
3. Chatterbox-Turbo realtime factor on this specific CPU.
4. RunPod/Lambda current prices.
5. Whether YouTube's API audit requirement restricts automated uploads for a new project.
