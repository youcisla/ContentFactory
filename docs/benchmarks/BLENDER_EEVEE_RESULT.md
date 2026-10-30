# Blender Eevee Result — CF-020

Date: 2026-10-30. One-frame capability test. Bounded, local, no paid service.

---

## What ran

| Item | Value |
|---|---|
| Blender | **5.2.3 LTS**, hash `e13b728c6880`, built 2026-10-22 |
| Install | Portable ZIP, `tools/blender/blender-5.2.3-windows-x64/` |
| Archive | 387 MB, SHA-256 verified against Blender's official checksum |
| Engine | `BLENDER_EEVEE` (5.x identifier) |
| Scene | Bevel card on floor, 50 mm camera, key + fill area lights, dark world |
| Output | 1080×1920 PNG, 64 TAA samples |
| Script | `tools/blender_evee_test.py` |

## Measurements

| Metric | Value |
|---|---|
| Blender start → exit | **57.8 s** |
| Render call | **42.64 s** for one frame |
| Peak working set | **1,593 MB** |
| Exit code | 0 |
| Output written | yes (`tools/blender-test/frame.png`) |

## Interpretation

- **Eevee initialises and renders headlessly on this Intel iGPU.** The earlier "no 3D" conclusion is corrected.
- **Speed is the blocker.** 42.6 s/frame for a trivial scene extrapolates to:
  - 240 frames (10 s @ 24 fps) ≈ **170 minutes** per pass.
  - Even at 16 samples (~4× faster) ≈ **40+ minutes**.
- Budget for V4 was ≤ 15 minutes for 240 frames. Local misses it by an order of magnitude.

## Caveats

- The rendered frame is nearly black: camera aim or light placement in the test scene is wrong. The test proves completion and timing, not visual correctness.
- GPU backend identity was not captured: the `gpu` module is uninitialised in background before render, and `--debug-gpu` produced no parseable output.
- If Blender is falling back to a software OpenGL renderer, a driver or session fix could change the number. Unverified.
- Peak RAM 1.6 GB: memory is not the constraint.

## Decision

| Path | Verdict |
|---|---|
| Local Eevee for animation | **Rejected** — 11× over budget |
| Local Eevee for stills / look-dev | **Accepted** — 43 s per still is workable |
| Remote Blender for animation | **Promoted to primary** |
| WebGL | Remains for diagrams |

## Next tests (not authorised)

1. Re-run at 16 samples and 540×960 for the scaling curve.
2. Capture GPU backend via `--debug-gpu` to a file, or Blender's Help → System Report.
3. Remote GPU: same scene, one frame on a rented 4090D; compare wall clock and cost.

## Evidence

- `tools/blender-test/stdout.txt` — render log with `RENDER_SECONDS 42.64`
- `tools/blender-test/frame.png` — output frame
- `tools/blender-test/gpu.txt` — failed GPU introspection (documented, not hidden)
