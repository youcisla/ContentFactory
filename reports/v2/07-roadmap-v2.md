# 07 — Implementation Roadmap v2

Every stage below is **not authorised to execute**. The only action requested at the end is B0.

Principle: each stage must be independently abandonable. No stage creates an always-running service; every artefact is a file under version control; every tool is portable and removable by deleting a directory.

---

## 1. Stage map

| Stage | Goal | Depends on | Effort [E] | Gate to proceed |
|---|---|---|---:|---|
| **R0** | Resolve corporate-use question | — | conversation | Written answer |
| **R1** | Visual-language spike, zero install | R0 (or explicit risk acceptance) | 1–2 h | You approve the look |
| **R2** | **B0 benchmark** (single requested) | R1 | 30 min | Pass criteria below |
| **R3** | Spine: schemas + frame generator + renderer | R2 pass | 10–16 h | Deterministic re-render hash match |
| **R4** | Template library (5 scenes) | R3 | 20–30 h | Each template renders both ratios |
| **R5** | Audio: TTS + captions | R3 | 8–12 h | Caption drift < 80 ms |
| **R6** | QA gates + ledger | R3 | 6–10 h | Unverified claim cannot render |
| **R7** | Pilot: 1 Short + 1 long | R4–R6 | 15–25 h | Accuracy + budget targets met |
| **R8** | Optional 3D hero shots via rented GPU | R7 | 10–15 h | Cost per shot < $0.50 and reproducible |

R1 exists because the cheapest possible failure is discovering the visual language is wrong before installing anything.

## 2. R0 — Policy gate (blocking)

**Subtasks**
- R0.1 Ask IT/acceptable-use: may third-party software be installed without elevation?
- R0.2 Ask whether a personal monetised channel may be produced on this asset.
- R0.3 Decide host: managed laptop / personal device / cloud-only.

**Acceptance:** a written answer covering R0.1–R0.2, or an explicit decision to move to a personal device.
**Rollback:** none needed — no state changed.
**Gate:** no installation of any kind before R0.

## 3. R1 — Visual-language spike (zero install)

**Subtasks**
- R1.1 Author three static SVG frames (title, network-flow diagram, data callout) at 1080×1920.
- R1.2 Export to PNG using a method that requires no install (browser screenshot is acceptable).
- R1.3 View at 360 px width, simulate phone viewing distance.

**Acceptance:** text legible at 360 px; hierarchy obvious without audio; you would publish the style.
**Rollback:** delete the three files.
**What it does not test:** timing, motion, render speed.

## 4. R2 — B0 benchmark (the single requested benchmark)

### Scope and safety envelope

| Property | Value |
|---|---|
| Location | `reports/v2/b0-spike/` only |
| Downloads | one `resvg` Windows binary (~5 MB) from its official release page |
| Installs | none — no admin, no package manager, no service, no PATH change |
| Models | none |
| Network | one HTTPS download; nothing uploaded |
| Cloud | none |
| GPU | none |
| Duration | ≤ 10 minutes wall clock |

### Steps

1. Download `resvg` release binary into `b0-spike/bin/`.
2. Write `gen.py` (Python **standard library only**) that emits **300 SVG frames** for a 10-second, 1080×1920, 30 fps, three-scene storyboard: title card → three-node flow diagram with an animated arrow → data callout with a counter.
3. Rasterise frames with `resvg`.
4. Encode with the installed FFmpeg twice: `libx264` and `h264_qsv`, same settings otherwise.
5. Record measurements.

### Measurements

| Metric | Method |
|---|---|
| Total wall clock | start/stop timestamps around steps 2–4 |
| Per-frame raster time | `resvg` loop timing |
| Frames per second achieved | 300 ÷ raster duration |
| Peak working set | `Get-Process` sampling during render |
| Output size | file size of each MP4 |
| Disk delta | free space before/after |
| Encode speed | FFmpeg reported fps and speed |

### Pass criteria (all must hold)

- Total ≤ **3 minutes**
- Peak RAM ≤ **1.5 GB**
- Output ≤ **15 MB** per encode
- Text legible at 360 px width in the rendered MP4
- No dropped or duplicated frames

### Stop conditions (abort immediately)

- Total > 10 minutes
- Peak RAM > 3 GB
- Free disk < 50 GB
- Any tool error requiring installation to fix

### Rollback

Delete `reports/v2/b0-spike/`. Nothing outside that folder is touched. No service was started, so nothing to stop.

### What a pass proves, and what it does not

Proves: the laptop can rasterise and encode vector animation fast enough to iterate, with acceptable memory.
Does **not** prove: final visual quality, TTS quality, 3D capability, or long-form render time. Those are R4/R5/R7 questions.

## 5. R3 — Spine build

**Subtasks**
- R3.1 Create `control/` with JSON schemas (`episode`, `claims`, `storyboard`, `assets`, `narration`, `render_job`, `qa`, `publish`) — strict validation, unknown keys rejected.
- R3.2 Implement `gen.py`: storyboard JSON → SVG frames, deterministic (no timestamps, no random).
- R3.3 Implement `render.sh`: frames → resvg → FFmpeg, with `-fflags +bitexact` where applicable.
- R3.4 Content-addressed job cache: `idempotency_key = sha256(template_version + canonical(params) + asset hashes)`.
- R3.5 Ledger `ledger.jsonl` for every state transition.

**Acceptance:** rendering the same episode twice produces byte-identical frames for static scenes; changing one parameter changes exactly the expected frames.
**Rollback:** `control/` and `spine/` are new directories; delete them.
**Gate:** deterministic hash match demonstrated before R4.

## 6. R4 — Template library

**Templates:** concept reveal · flow diagram · comparison/split · number callout · warning/alert.
Each takes JSON params and emits both 1080×1920 and 1920×1080 variants with separate safe areas (top 12 % / bottom 18 % for vertical; 5 % all sides for horizontal).

**Acceptance:** each template renders cleanly in both ratios; text never crosses safe area; five scenes can be sequenced into a 40-second cut.
**Rollback:** templates are versioned files; revert the commit.

## 7. R5 — Audio

**Subtasks**
- R5.1 Install Chatterbox-Turbo locally **after approval** (model download ~0.5–1.5 GB).
- R5.2 Generate narration per scene; store `duration_s` and character count.
- R5.3 Build captions from TTS timing; fall back to `faster-whisper` alignment only if drift > 80 ms.
- R5.4 Normalise loudness to −14 LUFS with FFmpeg `loudnorm`.

**Acceptance:** caption drift < 80 ms across a 60-second sample; audio loudness within ±0.5 LU of target.
**Rollback:** delete model cache; narration is regenerable from text.
**Gate:** listen test — if quality is rejected, switch to Kokoro, then to a paid API.

## 8. R6 — QA gates

**Subtasks**
- R6.1 Gate G1: `claims.json` must have `verified_by_human: true` for every referenced claim; renderer refuses otherwise.
- R6.2 Gates G2–G5 as signed JSON records (script, storyboard, render, publish).
- R6.3 Disk guard: refuse job < 15 GB free; abort < 8 GB.
- R6.4 Failure isolation: one failed scene blocks its episode, not the queue.

**Acceptance:** an episode referencing an unverified claim fails validation with a specific error, not a silent render.
**Rollback:** gates are files; delete to revert to manual process (at the cost of losing enforcement).

## 9. R7 — Pilot

**Subtasks**
- R7.1 One 40-second Short, fully reviewed.
- R7.2 One 8-minute long-form, fully reviewed.
- R7.3 Publish manually (no API) and record retention for 7 days.

**Acceptance:** factual accuracy confirmed at G1; legibility confirmed on a phone; variable cost within `05`; render time within 2× estimate.
**Rollback:** unpublish; templates unaffected.

## 10. R8 — Optional 3D hero shots

**Subtasks**
- R8.1 Pin a Blender image/version and a scene template.
- R8.2 Rent GPU only when a shot is queued; destroy instance after.
- R8.3 Upload scene, render stills/sequence, download, composite locally.

**Acceptance:** a 5-second 3D shot costs < $0.50, renders reproducibly on two runs, and composites without colour mismatch.
**Rollback:** delete cloud instance and local cache; no subscription.
**Gate:** only if the channel's identity requires 3D.

---

## 11. Approval gates summary

| Gate | Question | Blocks |
|---|---|---|
| G0 | Policy answer | everything |
| G1 | Claims verified | narration |
| G2 | Script approved | storyboard build |
| G3 | Storyboard approved | render |
| G4 | Render QA | assembly |
| G5 | Publish approved | upload |
| G6 | Benchmark authorised | B0 |

## 12. What is requested now

**Approve B0 only.** It is the smallest test that can invalidate the recommendation, costs no money, installs nothing system-wide, starts no service, and is fully reversible by deleting one folder. Everything else waits for its result.
