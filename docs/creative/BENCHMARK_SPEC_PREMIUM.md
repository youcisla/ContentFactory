# Premium 3D Benchmark — Specification

Target: one excellent 10-second scene, 24 fps, 1080×1920, Blender Eevee.
Purpose: prove visual quality **before** any automation. Not a pipeline test.

---

## 1. Why this gate exists

The WebGL POC proved the pipeline and failed the look (64/100). Automating a look that is not good enough multiplies the wrong thing. This benchmark asks one question: *can we make a single scene that looks premium?*

## 2. Deliverable

| Property | Value |
|---|---|
| Duration | 10.0 s |
| Frame rate | 24 fps (240 frames) |
| Resolution | 1080×1920, 9:16 |
| Engine | Eevee (Blender 5.2.3 LTS) |
| Audio | none in the benchmark |
| Output | H.264 MP4, CRF 18, plus 5 stills |

## 3. Shot list

| # | Time | Shot | Camera | Lighting | Content |
|---|---|---|---|---|---|
| 1 | 0.0–4.0 | Macro product shot: card on dark surface, chip catching light | 50 mm feel, slow dolly in, shallow DOF | HDRI rim + soft key upper left | Card material, bevel highlights, brandless |
| 2 | 4.0–7.0 | Card lifts toward terminal; screen wakes | Tracks card, slight parallax | Key intensifies; screen emissive | NFC rings, screen `READY` |
| 3 | 7.0–10.0 | Pull back; screen reads `APPROVED`; end title | Crane back and up | Practical glow from screen | State change, title |

One continuous camera move per shot; a hard cut at 1→2 is allowed and motivated by the lift.

## 4. Scene specification

| Element | Requirement |
|---|---|
| Card | Modelled, 1–2 mm bevel, matte plastic roughness 0.35, subtle normal map |
| Chip | Metal, anisotropic highlight, contact shadow |
| Terminal | Modelled bezel, recessed screen, keypad suggestion, matte ABS |
| Screen | Emissive plane, legible `READY` / `APPROVED`, bloom via compositor Glare |
| Surface | Dark brushed material, roughness variation |
| Environment | CC0 HDRI (Poly Haven studio) + two area lights |
| Shadows | Eevee shadow maps, soft; AO on; contact darkening under props |
| Depth of field | Shots 1 and 3, focus on card / terminal |
| Motion blur | On, 0.5 shutter |
| Composition | Card 35–50 % of frame width in shot 1; screen legible at 360 px |

## 5. Render settings (starting point)

| Setting | Value |
|---|---|
| TAA samples | 64 |
| Shadows | on, cube map 1024 |
| AO | on |
| Volumetrics | off for benchmark |
| Colour management | AgX, Medium High Contrast |
| Compositor | Glare (Bloom) + subtle vignette |
| Output | PNG RGBA 8-bit, 1080×1920 |

## 6. Acceptance criteria

1. **24 fps, 10.0 s, 240 frames**, no dropped or duplicated frames.
2. Card and terminal read as manufactured objects, not primitives.
3. No shadow acne, flicker, or z-fighting.
4. Screen text legible at 360 px display width.
5. Camera move continuous and motivated.
6. Render time ≤ **15 minutes** for 240 frames on this laptop.
7. Weighted creative score ≥ **80**, and user accepts the look.
8. Every asset has a recorded licence; hero props original.

## 7. Resource budget

| Item | Estimate |
|---|---|
| Blender portable ZIP | 349 MB download, ~1.5 GB on disk |
| HDRI + textures | 50–300 MB |
| Frames | 240 × ~1.5 MB ≈ 360 MB |
| Peak RAM | 2–6 GB |
| Render time | 2–8 min (estimate; must be measured) |
| Cost | €0 local |

## 8. Failure conditions

Stop and report if:

- Eevee fails to initialise in background mode.
- Render exceeds 15 minutes for 240 frames.
- RAM exceeds 12 GB.
- Free disk drops below 15 GB.
- Any asset licence cannot be proven.

## 9. What this benchmark does not prove

Automation, batch rendering, 8-minute long-form, audio, captions, publishing, or that the look scales to 40 topics. Those come after V4, deliberately.
