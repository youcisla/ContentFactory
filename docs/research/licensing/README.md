# Licensing assessment

Verified 2026-10-30 from licence files and vendor pages. Not legal advice.
Full matrices: `reports/v2/06-dependency-matrix-v2.csv`, `reports/02-dependency-matrix.csv`.

## Tooling

| Component | Licence | Commercial output | Note |
|---|---|---|---|
| Blender | GPL | Yes | Renders are not derivative works of Blender |
| FFmpeg (gyan.dev full build) | GPL build | Yes | Local use unrestricted; redistributing the binary triggers GPL |
| resvg | Apache-2.0 | Yes | Permissive |
| Manim | MIT | Yes | — |
| Remotion | Remotion License | Yes for individuals / ≤3 employees | Paid company licence beyond; cannot resell Remotion itself |
| n8n | Sustainable Use | Personal/internal yes | No hosting-as-a-service; `.ee` files need enterprise licence |
| Postiz | AGPL-3.0 | Yes for self-use | Network-service distribution triggers source disclosure |
| OpenPost | AGPL-3.0 | Yes for self-use | Same |
| Mixpost | MIT core | Yes | Pro edition is separately licensed |
| MoviePy | MIT | Yes | — |
| Docker Desktop | Proprietary free tier | n/a | Licence terms for larger organisations differ |

## Speech

| Engine | Licence | Commercial output | Note |
|---|---|---|---|
| Chatterbox-Turbo | MIT | Yes | Voice-cloning consent is the user's responsibility |
| Kokoro-82M | Apache-2.0 | Yes | Weights are permissively licensed |
| Piper 1 | **GPL-3.0** | Yes for output | Distributing binaries/derivatives triggers GPL |
| Edge TTS | unofficial | **No grant** | Reject for monetised output |
| Azure / ElevenLabs | commercial | Yes | Paid, per-character |

## Assets

| Source | Licence | Notes |
|---|---|---|
| Poly Haven | CC0 | No attribution required |
| Kenney | CC0 | Commercial use confirmed on site |
| ambientCG | CC0 | Licence text not captured in audit — verify before bulk use |
| Google Fonts | OFL | Font files, not rendered video, carry the terms |
| Pexels | Pexels Licence | Commercial use with restrictions; page blocked during audit |
| Pixabay | Content Licence | Similar restrictions; page blocked during audit |
| Sketchfab / Freesound | per asset | Must be checked individually; NC licences unusable |

## Platform

| Item | Rule |
|---|---|
| YouTube API | Google API Services Terms; upload quota 100/day (`videos.insert` bucket) |
| AI disclosure | Required for realistic synthetic content at upload |
| Music | Must be licensed for monetised video; no "found online" audio |

## Rules enforced by the pipeline

1. Every asset row carries `licence_spdx`, `licence_evidence_sha256`, `retrieved_at`, `commercial_ok`.
2. `commercial_ok = false` fails validation — the render does not start.
3. Licences are re-checked when the entity changes (individual → company, personal → client work).
4. No licence claim is made in documentation that is not backed by a fetched source.
