# Quality scorecard — 2026-10-31B (asset-first milestone)

Supersedes nothing; the 2026-10-31 scorecard (58/100) remains the record of that state. This version scores the repo after CF-150/151/154 and the three built shot templates.

Scores use the brief's weights. Each is anchored to an artefact that exists.

| Category | Weight | Score /5 | Evidence |
|---|---:|---:|---|
| Cinematic visual quality | 25 % | **3** | Asset terminal, four real finishes, 85 mm product framing, DOF, emissive screen. `render/stills/artA_premium_realistic.png` is a credible product photograph. Not 4: no human, no set dressing, single prop, studio not film frame |
| Educational accuracy | 20 % | **4** | Unchanged. Six script lines traced to VERIFIED claims; no new factual claims added this session. G1/G2 still unsigned |
| Animation and editing | 15 % | **2** | Unchanged. No new animation; the assembly proof is a three-still slideshow with hard cuts and fades, not choreography. No audio |
| Art direction | 10 % | **4** | Two coherent directions exist from the same asset (`artA`, `artB`), one selected, with a recorded rejection reason for the other. Up from 3 |
| Mobile / desktop readability | 10 % | **3** | Screen text legible at 1080; at 360 px it survives but is small. Interaction shot's card is readable; no safe-area automation yet |
| Reusability and automation | 10 % | **4** | Three templates render from JSON alone; content-addressed cache; one master + linked instance; shot sidecar records cache key and template hash. Up from 3. Not 5: 7 of 10 templates unbuilt, no compositor |
| Resource efficiency | 5 % | **4** | 13–16 s/still at 1080×1920/32 spp; cache hit 0.90 s vs 15.89 s (−94 %); one worker; 340 MB render dir. Up from 3 |
| Licensing and compliance | 5 % | **5** | Eleven assets, all CC0, sha256-verified; new terminal has a full provenance row; no NC or gated source entered the repo |

**Weighted: 68 / 100.** (3.4 of 5)

## What changed and what did not

- **+10 points**, almost entirely from the asset (quality +1, art direction +1, reusability +1, efficiency +1).
- The two heaviest categories still cap the score: cinematic quality is 3 because the frame has no human and no set; animation is 2 because nothing has been choreographed.

## Critical defects

None open. The baseline V4 frame fails its own exposure gate; that is recorded, not hidden, and does not affect the candidate.

## What would move it

| Change | Expected gain | Cost |
|---|---|---|
| Licence a rigged hand (CF-149) and add it to t02 | +4–6 (quality, art direction, readability) | approval + asset |
| Cut a 12 s four-shot sequence with a focus pull and a card-insert animation | +4–6 (animation, editing) | one session of keyframes |
| Add set dressing (receipt strip, counter props) | +2–3 (quality) | low |
| Build 2 more of the 10 templates | +1–2 (reusability) | one session |

The 90 bar is not reachable without the hand and a moving sequence. Neither is claimed here.
