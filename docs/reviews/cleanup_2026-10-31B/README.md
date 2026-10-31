# Cleanup manifest — 2026-10-31 (second pass)

Authorised by the user in the asset-first brief §10, under its ten conditions. Only files that met all ten were removed.

## Removed

| Group | Files | Bytes | Why | Regenerate with |
|---|---:|---:|---|---|
| `v4seq` | 24 | 11.2 MB | Superseded exploration sequence, class D in the 2026-10-31 audit | `CF_PREVIEW_RES=50 CF_PREVIEW_SAMPLES=8 CF_FRAMES=24 CF_TAG=v4seq` + `tools/blender_scene_v4.py` |
| `candB_seq` | 24 | 11.2 MB | Superseded candidate B | same, `CF_TAG=candB_seq` |
| `candB_seq2` | 24 | 11.2 MB | Superseded candidate B, second run | same, `CF_TAG=candB_seq2` |
| `c136seq` | 24 | 11.6 MB | Superseded by `v4final` | same, `CF_TAG=c136seq` |
| `seqA` | 24 | 11.9 MB | Superseded Rig A/B experiment | same, `CF_TAG=seqA` |
| `seqB` | 24 | 11.3 MB | Superseded Rig A/B experiment | same, `CF_TAG=seqB` |
| `v4seq_verify` | 24 | ~11 MB | Regeneration proof produced during this cleanup | re-run the command above |
| `tmpl_*` probes | 5 | ~2 MB | Light-scale calibration frames; measured result recorded in the template | `tools/build_template.py` |
| **Total** | **173** | **≈ 81 MB** | | |

Per-file sha256 for the 144 quarantined frames: [`inventory.json`](inventory.json).

## Verification before deletion

Method copied from `CLEANUP_AND_ID_RECONCILIATION_V2.md` §6: quarantine, regenerate one group from its recorded settings, compare, then delete.

- `v4seq` was regenerated into `v4seq_verify` from `tools/blender_scene_v4.py` at 50 % resolution, 8 samples, 24 frames.
- Result: **24 of 24 frames**, and the same QA outcome — `CF seq_verdict=region 'card' deviates from expected curve by 26.2%`, against the 26.3 % recorded when the original ran.
- That is a reproduction of the artefact class, not a byte-identical copy; Eevee sampling is not bit-stable across runs and no claim of identity is made.

## Retained

| Item | Reason |
|---|---|
| `v4final_*` (240 frames, 115.9 MB) | Class B — frames behind the delivered 10 s cut |
| `proof_seq_*` (4 frames, 85.2 MB) | Class B — 4K stills behind the sample-count curve |
| `c136noemit_*` (24 frames) | Class B — the controlled experiment cited by CF-135 |
| `c136*` single stills | Class C — record of what was rejected and why |
| `anim_*` (24 frames, 11.4 MB) | **Not removed.** Its `.txt` records settings but no generator command, so provenance is uncertain. The brief says leave uncertain files untouched |
| `*.txt` QA logs | Evidence |
| `tools/blender/` (929 MB) | The render toolchain — never delete |
| Every MP4 | Delivered artefacts |

## Result

- `tools/blender-test`: **411 MB → 340 MB**
- Disk free: **77 GB → 81 GB**
- Nothing tracked by git was touched; `git status` shows no deletions.

## Candidates still needing a decision

| Candidate | Size | Why it needs the user |
|---|---:|---|
| `proof_seq` frames | 85.2 MB | Class B evidence, but the numbers are already extracted into `SAMPLE_AND_TEMPORAL_QA.md`; deleting them removes the raw 4K stills |
| `v4final` frames | 115.9 MB | Frames behind a delivered cut; regenerating costs ~34 min at 1080×1920 |

## Retention rules introduced

1. A generated sequence is deletable only when its generator and tag are both recorded next to it.
2. Any sequence referenced by a delivered artefact stays until a replacement artefact exists.
3. Class A/B artefacts (evidence behind a published number) are never deleted by an agent.
4. Probe frames are deleted at the end of the session that created them.
