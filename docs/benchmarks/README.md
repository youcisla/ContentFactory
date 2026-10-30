# Benchmarks

**No benchmark has been run.** Each requires the approval recorded in [`docs/operations/APPROVAL_GATES.md`](../operations/APPROVAL_GATES.md).

Design source: `reports/v2/07-roadmap-v2.md` §4.

---

## B0 — 10-second vector render spike (the only one requested)

| Property | Value |
|---|---|
| Purpose | Prove the laptop can rasterise and encode vector animation fast enough to iterate |
| Location | `reports/v2/b0-spike/` only |
| Download | one `resvg` release binary (~5 MB) |
| Installs | none — no admin, no package manager, no service, no PATH change |
| Models | none |
| Network | one HTTPS download; nothing uploaded |
| Cloud / GPU | none |
| Max duration | 10 minutes |

### Steps

1. Download `resvg` into `b0-spike/bin/`.
2. `gen.py` (Python standard library only) emits **300 SVG frames**: 10 s, 1080×1920, 30 fps, three scenes — title, three-node flow diagram with animated arrow, data callout with counter.
3. Rasterise with `resvg`.
4. Encode twice with the installed FFmpeg: `libx264` and `h264_qsv`.
5. Record measurements.

### Measurements

Total wall clock · raster time per frame · achieved fps · peak working set · output size · disk delta · encode speed (from FFmpeg).

### Pass criteria (all)

- Total ≤ 3 minutes
- Peak RAM ≤ 1.5 GB
- Output ≤ 15 MB per encode
- Legible at 360 px width
- No dropped or duplicated frames

### Stop conditions

Total > 10 min · peak RAM > 3 GB · free disk < 50 GB · any tool error requiring installation.

### Rollback

Delete `reports/v2/b0-spike/`. Nothing outside that folder is touched.

### What it proves

That the spine can iterate on this machine. It does **not** prove final visual quality, TTS quality, 3D capability, or long-form render time.

## Deferred benchmarks

| ID | Test | Depends on |
|---|---|---|
| B1 | 40 s 9:16 pilot, 6 scenes, measured end to end | B0 pass + R4 |
| B2 | 90 s 16:9 technical scene with reused assets | B1 |
| B3 | 5 s 3D hero shot on rented GPU, reproducibility check | R7/R8 |

## Results log

| ID | Date | Result | Notes |
|---|---|---|---|
| B0 | — | not run | awaiting approval |
| B1 | — | not run | — |
| B2 | — | not run | — |
| B3 | — | not run | — |

When a result lands: record it here, update the affected risk entries, and do not rewrite the audit reports (ADR-0005).
