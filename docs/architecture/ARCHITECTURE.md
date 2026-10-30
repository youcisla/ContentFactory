# Architecture

Status: proposed direction (ADR-0001), awaiting user sign-off. No component is implemented.
This document describes **what** the system is. ADRs explain **why**.

---

## 1. Shape

```
┌─────────────────────────────────────────────────────────────┐
│ CONTROL PLANE  — Python 3.12, pinned, no network at render  │
│  schemas → validators → job queue → ledger                  │
└──────┬───────────────────────┬──────────────────────┬───────┘
       │                       │                      │
┌──────▼─────────┐   ┌─────────▼────────┐   ┌─────────▼──────┐
│ FRAME PLANE    │   │ ENCODE PLANE     │   │ AUDIO PLANE    │
│ storyboard JSON│   │ FFmpeg libx264 / │   │ TTS → captions │
│ → SVG frames   │   │ h264_qsv + libass│   │ → SRT/VTT      │
│ → resvg → PNG  │   │ → MP4            │   │ loudnorm       │
└──────┬─────────┘   └─────────┬────────┘   └─────────┬──────┘
       │                       │                      │
       └───────────────┬───────┴──────────────────────┘
                       ▼
              ┌─────────────────┐        ┌──────────────────────┐
              │ ASSEMBLY        │        │ OPTIONAL 3D PLANE    │
              │ concat + mux    │◄───────│ remote Blender (GPU) │
              │ → final master  │        │ hero shots only      │
              └────────┬────────┘        └──────────────────────┘
                       ▼
              ┌─────────────────┐
              │ REVIEW GATES    │  G1 claims · G2 script · G3 board
              │ human, recorded │  G4 render · G5 publish
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ PUBLISH PLANE   │  YouTube Data API (manual first 10)
              └─────────────────┘
```

## 2. Components and responsibilities

| Component | Owns | Must never |
|---|---|---|
| Control | schemas, validation, queue state, cost ledger | touch the network at render time |
| Frame generator | storyboard JSON → deterministic SVG frames | read credentials, call an LLM |
| Rasteriser (`resvg`) | SVG → PNG | be upgraded without a version bump |
| Encoder (FFmpeg) | frames + audio → MP4, captions, loudness | make creative decisions |
| Audio | TTS synthesis, timing, captions | alter script text |
| Assembly | concat, mux, chapters | publish |
| Optional 3D | Blender render on rented GPU | run locally against an unsupported backend |
| Review | human decisions, signed records | be bypassable |
| Publish | upload, metadata, disclosure flag | run unattended |

## 3. Data contracts

All artefacts are JSON, validated strictly (`additionalProperties: false`). `schema_version` is mandatory semver.

| File | Required fields |
|---|---|
| `episode.json` | `episode_id, topic, audience, outputs[], claims_ref, storyboards{9x16,16x9}, disclosure` |
| `claims.json` | per claim: `claim_id, text, sources[{url,retrieved_at,quote,sha256}], confidence, verified_by_human` |
| `storyboard_<ratio>.json` | `ratio, resolution, fps, scenes[{scene_id,duration_s,template,params,claims[],camera,safe_area}]` |
| `assets.json` | `asset_id, path, sha256, source_url, licence_spdx, licence_evidence_sha256, retrieved_at, commercial_ok` |
| `narration.json` | `scene_id, text, provider, voice_id, chars, audio_path, duration_s, alignment_path` |
| `render_job.json` | `job_id, scene_id, template_version, engine, samples, seed, resolution, frames, idempotency_key` |
| `qa.json` | `scene_id, frame_range_checked, legibility_pass, continuity_pass, factual_pass, reviewer, signed_at` |
| `publish.json` | `video_path, title, description, tags, chapters[], captions_path, disclosure_flag, approved_by, approved_at` |

Full field-level specification: `reports/04-architecture-and-build-plan.md` §3.

## 4. Determinism and idempotency

- Frame generation is pure: `frame(scene_id, index, template_version, params)`.
- `idempotency_key = sha256(template_version + canonical(params) + sorted(asset hashes) + render settings)`.
- Re-running a job with the same key returns the cached output; it never re-renders.
- Rasteriser binary, font files, and template version are pinned. A change to any of them is a new template version.
- Static scenes must produce identical frame hashes across runs; animated scenes must produce identical frame counts and durations.

## 5. Format rules

| Concern | 16:9 | 9:16 |
|---|---|---|
| Resolution | 1920×1080 @ 30 fps | 1080×1920 @ 30 fps |
| Camera fit | horizontal | vertical |
| Safe area | 5 % all sides | top 12 %, bottom 18 % |
| Minimum text | 28 px | 42 px |
| Duration target | 8 min | 40 s |
| Scene count | 35–60 | 6–9 |

Shorts are separate storyboards, never crops of the long-form.

## 6. Deployment modes

| Mode | Local work | Remote work | When |
|---|---|---|---|
| Local-only | everything | none | Prototypes, 1–2 videos/month |
| Hybrid | frames, audio, assembly | 3D hero shots only | **Default** |
| Cloud-only | editing only | render | If local installation is forbidden |

## 7. Boundaries

1. No agent in the production render or publish path.
2. No always-running service.
3. No credentials reachable by generated code.
4. No unverified claim can be narrated — enforced at schema level.
5. No 3D render on an unsupported GPU backend.

## 8. Deferred components

| Component | Trigger to add |
|---|---|
| Manim | Topic requires mathematical/technical animation |
| Blender (remote) | Episode needs spatial/3D explanation |
| faster-whisper | Caption drift exceeds 80 ms |
| MoviePy | FFmpeg filter graphs become unreadable |
| Any self-hosted publisher | Multi-platform distribution becomes a requirement |
