# Narration options — licence and availability research

Date: 2026-10-31. Research only: **nothing was installed, downloaded or generated.** The V5 sequence ships captioned.

## What is already on the host

| Option | Availability | Licence position | Verdict |
|---|---|---|---|
| Windows SAPI (System.Speech) | **Installed**: `Microsoft Hazel Desktop` (en-GB), `Microsoft Zira Desktop` (en-US) | Governed by the Windows licence; Microsoft publishes no explicit commercial-narration grant, and the OS EULA is not a content licence. Unverified for a monetised channel | **Not used** — technically free, legally unverified |
| FFmpeg | Installed 8.1.1 | No speech synthesis | Cannot narrate |
| edge-tts | Not installed | Unofficial client for Microsoft's Edge online voices; use is subject to Microsoft service terms and is not a licensed API | **Rejected** |
| Azure Neural TTS | Not configured | Clear commercial terms, but a paid online service | **Excluded** by the no-paid-services rule |

## Options that would work with one approval

| Option | What must be downloaded | Size | Licence | Attribution |
|---|---|---:|---|---|
| **Piper, `en_US-libritts-high` voice** (recommended) | `piper` runtime + one ONNX voice | ~60 MB | Engine GPL-3.0/MIT; the LibriTTS-R dataset is **CC BY 4.0**, commercial use allowed | Credit "LibriTTS-R" in the description |
| Kokoro-82M | ONNX weights + runtime | ~80–350 MB | **Apache 2.0**, commercial use allowed, notice preserved | Recommended, not required |
| Piper `lessac` or fine-tunes | — | — | Blizzard 2013 Lessac licence is **research-only** | **Excluded** |
| Piper `ryan` | — | — | Dataset CC BY-NC-SA 4.0 | **Excluded** (NC) |

## Recommendation and exact approval needed

Approve **one download**: the Piper runtime plus `en_US-libritts-high` (~60 MB), stored under `tools/` or `assets/`, no system install, model sha256 recorded in the manifest. That is the smallest licence-clean path to narration.

Until that approval exists, no narration is produced and the film is labelled captioned-only.

## Synchronisation contract (for whichever TTS is approved)

1. **Cue file** (`narration.json`) is a list of `{shot, t_local, line, voice}`. `t_local` is seconds inside that shot's own timeline, not the assembled timeline.
2. **Assembly mapping** is already recorded: `render/assembly/v5_sequence.json` stores each shot's `timeline_start_s`, frame count and fps. A cue's global time is `timeline_start_s + t_local`.
3. **Tolerance**: a cue must land within ±1 frame (41.7 ms at 24 fps) of its line start after mixdown; drift is measured per cue, not on the whole track.
4. **Re-timing rule**: editing a shot's duration changes only that shot's timeline entry; cues are shot-local, so they move with the shot. A cue that would fall inside a crossfade is an authoring error and fails the gate.
5. **Delivery**: 48 kHz mono WAV per cue, mixed to a single 48 kHz stereo track; loudness target −14 LUFS ±0.5 (CF-052), measured with `ffmpeg -af loudnorm=print_format=json`.
6. **Captions** remain burned in the preview. When narration lands, captions are regenerated from the cue file so text and voice share one source.
