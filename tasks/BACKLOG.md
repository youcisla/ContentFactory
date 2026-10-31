# Backlog

Atomic work only. Phase intent lives in [`docs/roadmap/MASTER_PLAN.md`](../docs/roadmap/MASTER_PLAN.md); this file does not restate it.
Status values: `blocked` · `ready` · `in progress` · `done` · `dropped`.

**Current reality (2026-10-30):** G0 is approved. Phase 1 spike tasks CF-010–CF-020 are complete. Blender 5.2.3 is installed and Eevee is measured. The only open work is V4 (one excellent scene), the vector spine (CF-015, blocked on G6), and everything downstream of V4.

**ID rule:** an ID is never reused. Bands: **0xx** spine, **1xx** visual/3D, **2xx** audio, **3xx** publishing. CF-020/CF-021 duplicates became CF-025/CF-026. CF-028–CF-036 duplicated the Phase 3 spine IDs and are now CF-128–CF-136. Full mapping: `docs/reviews/CLEANUP_AND_ID_RECONCILIATION.md` §5.

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
| CF-021 | V4 one-scene benchmark — 10 s @ 24 fps | **rendered — awaiting visual acceptance** | CF-025 | 240 frames @ 24 fps rendered at 540×960/8 spp (median 1.54 s/frame, 371 s total) and encoded to `tools/blender-test/contactless_10s_captioned.mp4` (10.0 s, 240 frames, 729 KB). `seq_verdict=PASS`. **Resolution is half the 1080×1920 spec** — a full-resolution master is ~4× the render time and has not been run. Visual acceptance (V3/V4) is the user's, not the script's |
| CF-025 | Corrected Eevee scene + objective exposure gate + GPU backend probe | done | — | `tools/blender_scene_proof.py`; gate PASS on `proof_final.png`; GPU = Intel OpenGL 4.6 |
| CF-128 | Smallest useful local animation benchmark — 24 frames, 540×960, 8 samples, encode to MP4 | done | — | `cf028.mp4` 540×960, 24 frames, 1.0 s, h264. 74.6 s total, median 2.42 s/frame. Adjacent SSIM 0.959–0.972, no flicker. Found F1 exposure drift 32 % and F2 metals render black. §8 of `SAMPLE_AND_TEMPORAL_QA.md` |
| CF-130 | Camera-relative light rig (turntable) to remove the 32 % exposure drift | done | — | Rig A: `seq_max_deviation` **3.55 %** (target ≤5 %), flicker index 0.00043. Rig B (fixed + gradient world) failed at 33.50 %. §9 of `SAMPLE_AND_TEMPORAL_QA.md` |
| CF-131 | Environment reflection source so metallic materials are not black | done | — | Gold chip reads as metal at all 6 stills and both sequences, `metallic` unchanged at 1.0. Both rigs satisfy it |
| CF-132 | Sequence QA in the scene script — drift and flicker indices replacing SSIM-only continuity | done | — | `seq_max_deviation` and `seq_flicker_index` in every multi-frame run; `CF_INTENTIONAL_DRIFT` separates scripted light moves from accidents |
| CF-133 | Cinematic V4 scene — coil, indicator, departing packet, eased dolly, emissive backdrop | **built, not accepted** | — | `tools/blender_scene_v4.py`. Defects CF-134/CF-135/CF-136 are now closed with measured evidence and the terminal has been rebuilt. **Visual acceptance is still withheld and is still the user's decision** — nothing in this repository can grant it |
| CF-134 | Fix packet trajectory — it passed through the card and exited frame | done | — | `packet_geometry()` asserts, without rendering: in-frame with a 6 % NDC margin, ≥1.5 mm clearance from every solid, and a camera→packet ray cast for occlusion. Current path **PASS** (min edge margin 0.140, min clearance 3.19 mm, 11 moving frames). **Negative control:** the pre-fix path from `a7d4a18` **FAILS** the same gate — hidden behind the card at f14–15, 4.8 mm inside it at f16, right-edge breach at f23–24. Run `CF_GEOMETRY_ONLY=1 CF_FRAMES=24` |
| CF-135 | Dolly-invariant exposure and region QA | done | — | Declared curve now computed from the real light positions (`curve_at`, inverse-square) rather than fitted, and compared with a normalised relative error. `CURVE_MAX = 0.25` applies only when a curve is supplied, so the 5 % orbit rule is unchanged. 240-frame run: whole-frame **5.18 %**, terminal **3.37 %**, chip **19.97 %**, card **21.01 %** — all inside band; flicker **0.00006**. Card residual is view-dependent specular, **proved** by an emission-off control run (33.27 % vs 33.39 %, i.e. no change) |
| CF-136 | Backdrop seam and terminal silhouette | done | — | Terminal rebuilt from nameable parts: body, tilted head, glossy black bezel, dark display glass, amount line, green approval tick, 12-key keypad with cancel/enter, card slot, status LED. Two structural causes found and fixed: (a) the card was held **directly over the display**, hiding it — tap point moved forward and camera raised to 23°; (b) all materials were within 12 % of one another, so nothing separated screen from housing — separation is now by value and specular, with `spec` control added to `material()`. Verified in renders at f6/f14/f22 and f150 of the sequence |
| CF-137 | 40 s animatic — 3D mechanism + 2D network, captions burned in | done | — | `tools/build_animatic.py` → `render/animatic/contactless_40s_animatic.mp4`, 960 frames, 40.000 s, 540×960, 24 fps, 12 caption cues. **Animatic, not final picture: no audio of any kind, and S4–S6 are diagrams.** Scene sources in `render/scenes/`; two independent reviews and their dispositions in `docs/reviews/ANIMATIC_QA_2026-10-31.md` (one factual BLOCKER on the credit-card hold, one pipeline BLOCKER on the unbounded segment length — both fixed) |
| CF-138 | 40 s final — packet return leg and 960-frame re-time | ready | CF-137 | The only missing mechanism for a complete 3D S1–S3; geometry gate must pass before any sequence render. Est. 34 min at 1080×1920 for the 3D third, measured 8.51 s/frame |
| CF-139 | Audio for the 40 s cut — narration and music | **blocked** | approval (recording, or a G6-style model-download approval) | No audio exists. Until this closes the film ships captioned and must be labelled as such |
| CF-129 | Visual QA automation — QA-4, QA-5, QA-10 from `SAMPLE_AND_TEMPORAL_QA.md` §4 | blocked | CF-128 | Framing, object-visibility and text-size checks run in CI on every render |
| CF-140 | Asset acquisition — small curated CC0 set (one HDRI, one PBR set) with recorded provenance | done | — | `assets/manifest.json`: 10 files, **23.1 MB**, sha256 per file. `brown_photostudio_02` 2K HDR (CC0, Poly Haven); `metal_plate` 2K diffuse/rough/normal/metal (CC0, Poly Haven); `Plastic013A` 1K JPG (CC0, ambientCG). No account, no attribution owed, no collection download |
| CF-141 | Asset manifest + validator | done | — | `tools/check_assets.py` — PASS on the real manifest (`assets=10 total_mb=23.1`); negative control with `commercial_ok=false` exits 1 with two FAIL lines. Also checks sha256, file existence, https source and the 100 MB cap |
| CF-142 | `.blend` scene template — camera rig, light rig, set, linked asset collections | done | CF-140, CF-141 | `tools/build_template.py` → `templates/cf_studio_v1.blend`. Collections `CAMERAS`/`LIGHTS`/`SET`/`PROPS`/`RIGS`; two cameras (85 mm f/8 macro, 35 mm f/5.6 wide) tracking a `SubjectMarker`; HDRI world at 0.3; PBR counter/backdrop/trim; 3.0 m backdrop for usable DOF; AgX MHC; 180° shutter. Verified headless: opens, prints metadata, renders a frame in **5.33 s** at 540×960/16 spp with `mean 0.212, p95 0.526`. Light powers measured by a scale sweep, not guessed |
| CF-148 | Shot template library build-out — 5 of 10 from `docs/production/SHOT_LIBRARY.md` | blocked | CF-150 | Five templates render headless from parameters only; each passes the geometry gate |
| CF-149 | Rigged hand / character acquisition | **blocked** | user approval + CC BY credit plan | One model enters `assets/` with a licence row and a generated credit line; brand marks inspected |
| CF-150 | Terminal hero prop modelled to reference | ready | — | Modelled in-house, no brand marks, passes geometry gate; est. 4–6 h |
| CF-151 | Content-addressed render cache | ready | — | Re-running an unchanged shot returns cached frames; hit rate reported |
| CF-152 | Six-minute script and shot list bound to claims | ready | — | Every line traces to a VERIFIED claim; every shot assigned a class from `SIX_MINUTE_SPEC.md` §2 |
| CF-153 | Cold/warm production measurement harness | blocked | CF-151 | Cold and warm timings measured and recorded separately; no invented numbers |
| CF-154 | Art-direction A/B — cinematic realistic vs premium stylized | blocked | CF-150 | Two stills from the same subject, blind comparison, decision recorded |
| CF-155 | Template v2 — compositor, shot-parameter JSON, template hash in render job | blocked | CF-150 | Opens headless; renders 3 shot variants from JSON; hash recorded |
| CF-143 | Isolated trial of `ifBars/blender-agent-studio` (authoring only) | **blocked** | user approval + isolated VM/container, no network, no credentials | Builds and saves one `.blend` with a camera and a light; no render-path use; result recorded with its licence and telemetry status |
| CF-144 | V5 premium benchmark — 8–12 s, asset-driven, 1080×1920, multi-shot | blocked | CF-140, CF-142 | Shot spec in JSON; beats V4 in blind side-by-side review; render ≤ 15 min; every asset has a licence row |
| CF-145 | Camera-language pass — DOF, 180° shutter motion blur, 35/50/85 mm shot discipline | ready | — | Still A/B shows focus falloff and blur; no geometry-gate or exposure-gate regression |
| CF-146 | Comparative review — V5 vs V4 baseline | blocked | CF-144 | Before/after stills and measured render time, RAM, disk, licence rows; independent critique recorded |
| CF-147 | Hygiene manifest for the asset pipeline | ready | — | Inventory of superseded renders and candidates; no deletion; sizes recorded |
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
