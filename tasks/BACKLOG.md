# Backlog

Atomic work only. Phase intent lives in [`docs/roadmap/MASTER_PLAN.md`](../docs/roadmap/MASTER_PLAN.md); this file does not restate it.
Status values: `blocked` · `ready` · `in progress` · `done` · `dropped`.

**Current reality (2026-10-30):** G0 is approved. Phase 1 spike tasks CF-010–CF-020 are complete. Blender 5.2.3 is installed and Eevee is measured. The only open work is V4 (one excellent scene), the vector spine (CF-015, blocked on G6), and everything downstream of V4.

**ID rule:** an ID is never reused. When a task was renumbered, the old ID is retired, not reassigned. CF-020 and CF-021 previously appeared twice with different meanings; the Phase 2 duplicates are now CF-025 and CF-026.

---

## Phase 0 — decisions

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-001 | Obtain policy answer (install rights, personal commercial use, storage) | done | — | User declaration recorded in `APPROVAL_GATES.md` G0, 2026-10-30; no IT document on file |
| CF-002 | Choose host: this device / personal device / cloud-only | done | — | This laptop chosen by user; no architecture change |
| CF-003 | Decide repository licence | ready | — | Licence file added, or "none" recorded as an ADR |

## Phase 1 — visual spike (no install)

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-010 | Author 3 static SVG frames at 1080×1920 (title, flow diagram, data callout) | done | — | 3 frames + storyboard + source notes; validator PASS |
| CF-011 | Render the 3 frames with an existing tool, no install | done | CF-010 | PNGs in `prototypes/r1/previews/`, rendered with installed Chrome |
| CF-012 | User approves visual language | ready — awaiting user | CF-011 | Written approval, or a new ADR if the style changes |
| CF-013 | 12 s animated SVG/CSS prototype | done | CF-012 (authorised in advance) | `prototypes/r2/`, validator PASS, 4 states captured |
| CF-014 | Rust rendering evaluation | done | — | `docs/research/rust-rendering/`; no build, no download |
| CF-015 | B0 render benchmark | **blocked** | resvg download approval (G6) | Wall clock, RAM, output size recorded |
| CF-016 | Cinematic treatment + shot list | done | — | `docs/creative/TREATMENT_TAP.md` |
| CF-017 | WebGL cinematic POC (10 s, 9:16) | done | CF-016 | `the-tap.mp4` rendered; **64/100**, below 90 bar |
| CF-018 | Premium 3D feasibility: Blender Eevee, assets, benchmark spec | done | — | Report + shortlist + spec; no install or render |
| CF-019 | Authoring tool for premium 3D (Blender install or personal GPU machine) | done | — | Blender 5.2.3 portable ZIP installed at `tools/blender/blender-5.2.3-windows-x64/` |
| CF-020 | Install Blender 5.2.3 portable ZIP | done | — | 5.2.3 runs; one-frame Eevee render measured (42.64 s, 1.59 GB) |
| CF-021 | V4 one-scene benchmark — 10 s @ 24 fps | **in progress** | CF-025 | Scene renders and passes an objective exposure gate; the 10 s sequence does not yet exist. See `docs/benchmarks/BLENDER_EEVEE_CORRECTION.md` |
| CF-025 | Corrected Eevee scene + objective exposure gate + GPU backend probe | done | — | `tools/blender_scene_proof.py`; gate PASS on `proof_final.png`; GPU = Intel OpenGL 4.6 |
| CF-028 | Smallest useful local animation benchmark — 24 frames, 540×960, 8 samples, encode to MP4 | done | — | `cf028.mp4` 540×960, 24 frames, 1.0 s, h264. 74.6 s total, median 2.42 s/frame. Adjacent SSIM 0.959–0.972, no flicker. Found F1 exposure drift 32 % and F2 metals render black. §8 of `SAMPLE_AND_TEMPORAL_QA.md` |
| CF-030 | Camera-relative light rig (turntable) to remove the 32 % exposure drift | **ready** | — | A 24-frame orbit holds luma within ±5 % of frame 1 |
| CF-031 | Environment reflection source so metallic materials are not black | **ready** | — | Gold chip reads as metal at every camera angle in the orbit |
| CF-029 | Visual QA automation — QA-4, QA-5, QA-10 from `SAMPLE_AND_TEMPORAL_QA.md` §4 | blocked | CF-028 | Framing, object-visibility and text-size checks run in CI on every render |
| CF-022 | Automation only after V4 | **blocked** | CF-021 | Visual acceptance precedes batch work |
| CF-023 | Remote Eevee test — one frame on RunPod Community 4090 ($0.34/h) or Vast 4090 ($0.41/h) | **blocked** | user approval + spend (~$0.05) | Wall clock recorded; cost per 10 s scene computed |
| CF-024 | Free fallback: SheepIt Eevee test with a public, non-sensitive scene | **blocked** | account + IP-risk acceptance | Eevee supported in practice; queue time recorded |

## Phase 2 — benchmark

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-026 | Approve and run B0 (10 s vector render spike) | blocked | G6 approval | Pass criteria met; results logged in `docs/benchmarks/README.md` |
| CF-027 | Update risk R2/R3 and cost model with measured numbers | blocked | CF-026 | Registers updated; audit reports untouched |

## Phase 3 — spine

| ID | Task | Subtasks | Status | Acceptance |
|---|---|---|---|---|
| CF-030 | JSON schemas + validators | episode, claims, storyboard, assets, narration, render_job, qa, publish | blocked | Invalid episode rejected with a specific error |
| CF-031 | Claim gate | enforce `verified_by_human` | blocked | Renderer refuses scenes referencing unverified claims |
| CF-032 | Frame generator | storyboard → SVG, pure functions | blocked | Same input yields identical SVG |
| CF-033 | Rasteriser integration | pinned `resvg`, bundled fonts | blocked | Static frames byte-identical across runs |
| CF-034 | Encode pipeline | FFmpeg `libx264` + `h264_qsv`, `libass` | blocked | Two encodes of the same frames match in duration and frame count |
| CF-035 | Idempotent job cache + ledger | content-addressed keys | blocked | Re-running a job returns cached output; ledger records transitions |

## Phase 4 — templates

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-040 | Five templates: concept reveal, flow, comparison, number, warning | blocked | CF-032–CF-034 | Each renders 9:16 and 16:9 without safe-area violations |
| CF-041 | Safe-area and type-size validation | blocked | CF-040 | Automated check fails on <42 px vertical text |

## Phase 5 — audio

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-050 | Evaluate local TTS (Chatterbox-Turbo, fallback Kokoro) | blocked | G6-style approval for model download | Realtime factor measured; quality accepted or rejected |
| CF-051 | Caption generation and alignment | blocked | CF-050 | Drift <80 ms on a 60 s sample |
| CF-052 | Loudness normalisation | blocked | CF-051 | −14 LUFS ±0.5 |

## Phase 6 — review and pilot

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-060 | G1–G5 gate records | blocked | CF-031 | No publish path without a G5 record |
| CF-061 | Pilot Short (40 s) | blocked | CF-040–CF-052 | Passes all gates; within budget |
| CF-062 | Pilot long-form (8 min) | blocked | CF-061 | Passes all gates; render within 2× estimate |
| CF-063 | Manual upload of first 10 videos | blocked | CF-061 | Ten published videos, retention data collected |

## Phase 7 — publishing automation

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-070 | YouTube API uploader with disclosure flag | blocked | CF-063 + API audit check | Uploads a private test video successfully |

## Phase 8 — optional 3D

| ID | Task | Status | Blocked by | Acceptance |
|---|---|---|---|---|
| CF-080 | Remote Blender hero-shot pipeline | blocked | CF-062 | 5 s shot < $0.50, reproducible on two runs |

## Standing tasks

| ID | Task | Status | Acceptance |
|---|---|---|---|
| CF-090 | Review risk register after each phase | ready | Triggers updated, rows changed only where evidence changed |
| CF-091 | Check links and redaction before every commit | ready | No broken relative links, no identifiers |

## Task template

```
| CF-0NN | Verb + object | status | dependency | measurable acceptance |
```

Every task must have a measurable acceptance criterion. "Works" is not acceptance.
