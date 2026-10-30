# The Tap — cinematic proof of concept

10-second, 9:16, real-time WebGL scene rendered frame-by-frame with Chrome and encoded by FFmpeg. Zero third-party libraries, zero external assets, zero cost.

## Artefacts

| File | What |
|---|---|
| `tap.html` | Scene source. Deterministic: `?t=<seconds>` renders one frame |
| `the-tap.mp4` | 1080×1920, 12 fps, 10.0 s, 120 frames, 1.33 MB |
| `frames/f000–f119.png` | Frame sequence |
| `stills/t0.5,t3.0,t6.0,t9.0.png` | Key stills |
| `verify-frame.png` | Frame extracted from the encoded MP4 at 9.5 s |

## Preview

Open `tap.html` in Chrome or Edge — real-time loop. Add `?t=6` to freeze one frame. Headless capture needs `--enable-unsafe-swiftshader`.

## Re-render

```
chrome --headless=new --enable-unsafe-swiftshader --window-size=1080,1920 \
  --virtual-time-budget=1200 --screenshot=frames/f000.png "file:///.../tap.html?t=0"
ffmpeg -framerate 12 -i frames/f%03d.png -c:v libx264 -pix_fmt yuv420p -crf 18 the-tap.mp4
```

Measured: **254 s for 120 frames** (≈2.1 s/frame, dominated by Chrome start-up, not rasterisation). Output 1.33 MB. Peak memory not measured.

## What is real

- Perspective camera with eased keyframes; one continuous move, no cuts.
- Directional key + fill, specular highlight, fresnel rim, distance fog.
- Procedural rounded-box, sphere, torus and plane geometry.
- Terminal screen drawn at runtime to a canvas texture, `READY → APPROVED`.
- Packet path card → terminal → issuer → return; NFC rings; network graph.

## What is not real

- No ray-traced shadows, ambient occlusion, depth of field, or motion blur.
- No authored 3D assets: the card is a rounded slab, the terminal a box.
- No audio.
- 12 fps, not 24/30 — capture cost, not a design choice.
- Text is HTML overlay, not rendered in-scene.

## Why this renderer

Blender is not installed; three.js/Remotion/Manim are not installed and downloads are blocked; the Hyperframes skills are instructional with no local CLI. Custom WebGL + installed Chrome + installed FFmpeg was the only authorised path to a moving 3D image.

## Honest verdict

This proves the *pipeline* and the *mechanism*, not the *premium look*. See `docs/reviews/VISUAL_BENCHMARK_REVIEW.md`: **64/100**, below the 90 target. The blocking gap is an authoring tool, not effort.
