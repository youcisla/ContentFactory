# ADR-0004 — Local TTS with licensed fallback

- Status: proposed
- Date: 2026-10-30
- Deciders: user (sign-off pending), agent (proposal)
- Related: ADR-0001, `reports/v2/04`

## Context

Narration is needed for every video. Options differ sharply on licence and on whether they run on this CPU-only machine.

| Engine | Licence | CPU viability | Maintenance |
|---|---|---|---|
| Chatterbox-Turbo | MIT | vendor claims 3× realtime on 8 cores | active |
| Kokoro-82M | Apache-2.0 weights | lightweight, ONNX | stale ~14 months |
| Piper 1 | **GPL-3.0** | very fast | active |
| Edge TTS | unofficial endpoint | cloud | no licence grant |
| Azure / ElevenLabs | commercial | cloud | mature |

Edge TTS has no commercial licence grant and is rejected for monetised output. Piper's successor changed from MIT to GPL-3.0, which affects distribution but not local use.

## Decision

Use **Chatterbox-Turbo** locally as the primary engine, **Kokoro-82M** as fallback. If local quality is rejected after a listen test, use a **licensed paid provider** (Azure or ElevenLabs). Edge TTS is never used for published output.

## Alternatives considered

| Option | Why not primary |
|---|---|
| Edge TTS | No commercial rights |
| Piper 1 | GPL-3.0 obligations on distribution; no quality advantage established |
| Paid cloud TTS | Recurring cost and network dependency; keep as fallback |
| Coqui XTTS | Weights are non-commercial; project dead |

## Consequences

**Positive:** zero marginal narration cost; no network dependency; licence permits commercial output.

**Negative:** model download of roughly 0.5–1.5 GB; CPU speed is a vendor claim until measured; quality may be below paid providers.

**Harder:** voice consistency across episodes requires pinning model version and voice/speaker settings.

## Conditions

1. Measure realtime factor before committing to local TTS in R5.
2. Store the model version and voice id in `narration.json`.
3. Voice cloning is not used without explicit consent from the speaker.
4. Any paid provider's credentials stay outside the repo.

## Evidence

- `reports/v2/04-tts-assets-render-v2.md` §1
- `reports/v2/06-dependency-matrix-v2.csv`
