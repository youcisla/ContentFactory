# Quality scorecard — 2026-10-31

Scores use the brief's weights. Each is anchored to something that exists in the repository, not to intent. A category with no artefact scores 0–2.

| Category | Weight | Score /5 | Evidence |
|---|---:|---:|---|
| Cinematic visual quality | 25 % | **2** | V4 scene and one template still. Recognisable objects, correct perspective, a dark set with real PBR texture. Still primitive geometry, no hero prop, no human, no set dressing. The 64/100 WebGL POC was worse; this is better but far from premium |
| Educational accuracy | 20 % | **4** | Six script lines, every one traced to a VERIFIED claim; a factual review corrected three overstatements; prohibited language listed and enforced. Not 5 because no human has signed G1/G2 and tokenisation is deliberately unused |
| Animation and editing | 15 % | **2** | A 10 s rendered dolly and a 40 s animatic exist. Camera language is one continuous move; the lens probe showed DOF currently destroys legibility at tabletop scale. No cuts, no focus pull, no sound |
| Art direction | 10 % | **3** | Palette, a colour-location rule (green never on the card), and a lighting formula with measured levels. The identity is coherent but thin: one look, few materials, no typography |
| Mobile / desktop readability | 10 % | **3** | 9:16 framing verified by geometry gate; captions burned and validated; terminal screen verified unreadable at wide aperture. The latter is a known open defect |
| Reusability and automation | 10 % | **3** | `templates/cf_studio_v1.blend` with named collections, two cameras, rig and measured lights; asset catalog + validator that can fail. Shot library exists as a spec, not as working templates |
| Resource efficiency | 5 % | **3** | Measured: 8.51 s/frame 1080p/8 spp; 14.83 s baseline 32 spp; motion blur +45 %; HDRI +81 %. One render worker, no idle services. No caching layer yet |
| Licensing and compliance | 5 % | **5** | Ten assets, all CC0, sha256-verified, no attribution owed, validator enforces `commercial_ok`. Paid and NC sources excluded. This is the strongest category |

**Weighted: 58 / 100.** (2.9 of 5)

## What the number means

This is a **technical production baseline**, not a creative acceptance candidate. The brief's bar is 90+. The gap is not spread evenly:

- 25 % of the score (cinematic quality) sits at 2 because there is no hero prop and no human in frame. That is the single largest lever.
- 15 % (animation) sits at 2 because nothing has been cut or choreographed yet.
- The strongest categories are accuracy and licensing, which are also the cheapest to keep.

## What would move it

| Change | Expected gain | Cost |
|---|---|---|
| Import one licensed terminal + hand, light them in the template | +6–10 points (quality, art direction) | 1 session + 8 MB assets |
| Cut the 11 s treatment into 4 shots with the rack focus | +4–5 (animation, readability) | 1 session |
| Add foley + a sub hit | +2–3 (editing) | blocked on CF-139 |
| Build 5 of the 10 shot templates | +2–3 (reusability) | 2 sessions |

No score here is a substitute for watching the film. The film does not exist yet at this quality level.
