# Six-minute production specification

Target: one 6:00 educational film, 16:9, English, captioned, with sound, produced from an approved spec. This document defines what is needed; it does **not** claim the film exists.

## 1. Cold and warm are different numbers

| | Cold production | Warm production |
|---|---|---|
| Definition | New research, fact-check, script, asset acquisition, new scene authoring, render, narration, edit, QA | Approved script + cached assets + existing templates + recorded narration pipeline + established edit |
| What dominates | Human and agent time; new geometry | Render of new hero shots only; assembly |
| Status | **Never measured** — no cold six-minute film has been made | **Never measured** — no warm run exists |

The brief's ten-minute warm target is a design constraint, not a measured result. It is written here as a target with its arithmetic shown, so it can be tested later:

- 6:00 at 24 fps = **8,640 frames**.
- At the measured 8.51 s/frame (1080×1920, 8 samples, no DOF), rendering all of it locally takes **20.4 hours**. The warm target is therefore impossible if every frame is newly rendered.
- The only way to reach a ten-minute assembly is **reuse**: cached 3D sequences, diagram overlays rendered once, and hero shots limited to a small budget.

## 2. Shot budget

| Class | Share of runtime | Source |
|---|---:|---|
| Reused 3D sequences (approved, cached) | up to 40 % | existing renders + new hero shots reused across episodes |
| Diagram / graphic layers | 30 % | SVG → raster → FFmpeg, the existing `build_animatic.py` path |
| New hero shots | 15 % | 6–10 shots × 3–5 s |
| Narration-driven stills with slow moves | 15 % | template scenes with camera moves only |

New rendering per six-minute film at the top of that budget: ~90 s of picture ≈ 2,160 frames ≈ **5.1 hours** at the measured rate, or ≈ 35 minutes if hero shots are made at 540×960 and upscaled for review only. Neither fits ten minutes; the ten-minute target requires that the *hero shots already exist*.

## 3. Structure (six minutes)

| Time | Section | Visual class |
|---|---|---|
| 0:00–0:35 | Cold open: the misconception, stated plainly | Hero shot 1 |
| 0:35–1:40 | The mechanism, part 1 | Diagram + reused 3D |
| 1:40–2:50 | The mechanism, part 2 | New hero shots 2–4 |
| 2:50–3:50 | The parties / the system | Diagram |
| 3:50–4:50 | The failure modes | Reused 3D + graphics |
| 4:50–5:40 | The reversal — what it actually means | Hero shot 5 |
| 5:40–6:00 | Close and the one sentence | Hero shot 6 + title |

## 4. Required components, and their real state

| Component | Required | State |
|---|---|---|
| Claims sheet with VERIFIED rows | yes | Exists for the contactless episode |
| Script bound line-by-line to claims | yes | Exists for 40 s; not for 6 min |
| Storyboard with shot classes | yes | Exists for 40 s |
| Studio template | yes | Built — `templates/cf_studio_v1.blend` |
| Hero props (terminal, card, hand) | yes | Card only; terminal unmodelled; no licensed hand |
| Narration | yes | **Does not exist.** No recording, no approved TTS |
| Music / foley | yes | **Does not exist** |
| Caption pipeline | yes | Exists; 12-cue SRT validated |
| Assembly | yes | Exists: `tools/build_animatic.py`, contract-asserted |
| QA gates | yes | Geometry, exposure, sequence, caption |
| Cache | yes | **Does not exist** — every render is cold |

## 5. Limiting capability, stated exactly

The film cannot be produced today because four things are missing, in order of hardness:

1. **No audio at all.** Narration and sound design are both absent and both are gated (CF-139). A six-minute silent explainer is not the deliverable.
2. **No hero assets.** The terminal must be modelled (4–6 h) and a hand licensed or modelled. Without them every shot is a diagram or a primitive.
3. **No cache layer.** Reuse is the only route to a warm ten-minute run, and nothing is content-addressed yet.
4. **No six-minute script.** The existing script covers 40 seconds and three beats.

## 6. What can be built now without new approvals

- The six-minute script and shot list, bound to the existing claim sheet (documentation).
- The cache design and a content-addressed frame store (code, local).
- Templates 1, 3, 4 from `SHOT_LIBRARY.md` once the terminal exists.
- A 60–90 s proof sequence using existing assets, as evidence of pacing.

None of these is the six-minute film, and none will be reported as such.
