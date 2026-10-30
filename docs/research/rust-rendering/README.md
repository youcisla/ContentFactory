# Rust Rendering Evaluation

As of 2026-10-30. Read-only repository and documentation review. **No Rust code written, no crates downloaded, no build executed.**
Status labels: VERIFIED · DOCUMENTED · ESTIMATED · UNKNOWN.

---

## 1. The question

Does a Rust-based renderer give a measurable advantage over the current vector-first plan (Python-generated SVG → `resvg` → FFmpeg)?

## 2. Components reviewed

| Project | Licence | Stars | Last push | Role |
|---|---|---:|---|---|
| `linebender/resvg` | Apache-2.0 | 4,164 | 2026-10-30 | SVG → PNG rasteriser; contains `usvg` (SVG parsing/normalisation) and `tiny-skia` (2D raster) |
| `rust-skia/rust-skia` | MIT | 1,834 | 2026-10-26 | Bindings to Skia; broad 2D feature set; C++ build dependency |
| `gfx-rs/wgpu` | Apache-2.0 | 18,421 | 2026-10-30 | Cross-platform GPU abstraction (Vulkan/Metal/DX12) |
| `bevyengine/bevy` | Apache-2.0 | 49,385 | 2026-10-30 | Game engine; 3D/2D scenes, ECS |
| `image-rs/image` | Apache-2.0 | 5,898 | 2026-09-15 | Image encode/decode |
| `rust-av/rust-av` | MIT | 918 | 2026-02-05 | Multimedia toolkit; narrower than FFmpeg |
| `nathanbabcock/ffmpeg-sidecar` | MIT | 546 | 2026-10-18 | Wrap an FFmpeg binary from Rust |

Local toolchain, measured: `rustc 1.96.0`, `cargo 1.96.0` — already installed. Building anything still requires downloading crates, which is not authorised.

## 3. Critical distinction

**`resvg` renders static SVG. It is not an animation engine.** A Rust pipeline would still need:

1. a frame generator (your code),
2. a rasteriser (`resvg`/`usvg`),
3. a video encoder (FFmpeg or `rust-av`).

That is the same three-stage shape as the current plan. Rust changes the language of stage 2, not the architecture.

Do not confuse "resvg is a fast SVG rasteriser" with "a Rust video pipeline is fast". Encoder time, disk I/O, and frame generation dominate at 1080×1920×300 frames.

## 4. Suitability

| Requirement | resvg | rust-skia | wgpu | Bevy |
|---|---|---|---|---|
| Static SVG | **Yes** | Partial (no bundled SVG parser) | No | No |
| CSS/SMIL animation | **No** (no timeline; you generate frames) | No | No | Timeline via ECS |
| 2D vector quality | High | High | Manual | Medium |
| 2.5D (depth, camera) | No | Limited | Yes, hand-built | Yes |
| 3D | No | No | Yes (low level) | Yes |
| Windows build without C++ | **Yes** | No (Skia build) | Yes | Yes |
| Headless CPU render | Yes | Yes | Software adapter only | Software adapter only |

## 5. Windows and build considerations

| Factor | Assessment | Status |
|---|---|---|
| Toolchain present | `rustc`/`cargo` 1.96.0 installed | VERIFIED |
| MSVC linker | Visual Studio Community 2026 present | VERIFIED (registry) |
| Crate download required to build | Yes — not authorised | BLOCKED |
| `resvg` CLI binary size | roughly 3–8 MB stripped | ESTIMATED |
| `bevy` binary size | tens of MB; long first build | ESTIMATED |
| Build time (first) | minutes for resvg, much longer for Bevy | ESTIMATED |

## 6. Performance: what is known and what is not

| Claim | Status |
|---|---|
| resvg is among the fastest SVG rasterisers | DOCUMENTED (project claim) — not measured here |
| Rasterisation is the bottleneck for 1080×1920 frames | UNKNOWN |
| Python frame generation is slower than Rust | UNKNOWN — Python emits strings; likely negligible versus raster+encode |
| FFmpeg encode dominates total time | ESTIMATED — typical for 300-frame clips |

**No benchmark was run.** B0 remains blocked: it requires the `resvg` binary, which is a download, and downloads are not authorised.

## 7. Architecture comparison (same storyboard, same weights)

Weights: accuracy 20 · visual 20 · efficiency 20 · cost 15 · automation 10 · maintainability 10 · compliance 5.

| Arch | Accuracy | Visual | Efficiency | Cost | Automation | Maintain | Compliance | **Total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A — SVG + resvg + FFmpeg (Python driver) | 18 | 14 | 16 | 13.5 | 9 | 7 | 5 | **82.5** |
| B — Manim + selective Eevee | 18 | 18 | 10 | 12 | 7 | 8 | 5 | **78.0** |
| C — three.js / R3F headless | 16 | 18 | 12 | 12 | 7 | 8 | 5 | **78.0** |
| D — remote Blender | 18 | 20 | 16 | 10.5 | 8 | 7 | 4 | **83.5** |
| **E — Rust + resvg + FFmpeg** | 18 | 15 | 15 | 12 | 9 | 6 | 5 | **80.0** |
| F — hybrid A + D hero shots | 18 | 17 | 15 | 11 | 9 | 7 | 4 | **81.0** |

E loses to A on maintainability (second language, build toolchain, contributors) and gains at most one point on raster quality/speed that has not been measured. **Rust is not justified yet.**

## 8. Recommendation

1. **Do not write Rust now.** Use the `resvg` CLI as a process from Python once its download is approved. That captures the rasteriser benefit without a Rust codebase.
2. If profiling later shows rasterisation above ~50 % of render wall-clock, embed `resvg` as a Rust library and expose a narrow CLI — a measured decision, not a stylistic one.
3. Do not use Bevy or wgpu for this project. They solve 3D/game problems; the content is diagrammatic.
4. `rust-skia` is rejected: C++ dependency for no feature the plan needs.

## 9. Unknowns

- Actual resvg throughput at 1080×1920 on this CPU.
- Memory peak during batch rasterisation.
- Whether process-spawn overhead per frame matters (one process can render many frames).
- Whether `resvg`'s SVG feature coverage handles every template the design system needs.

## 10. What would change the recommendation

| Evidence | Change |
|---|---|
| Raster > 50 % of render time | Embed resvg in Rust |
| resvg CLI missing needed SVG features | Evaluate rust-skia |
| Need for real 3D scenes | Bevy/wgpu, but compare against remote Blender first |
| Batch sizes above ~10k frames/day | Consider a long-running Rust worker |
