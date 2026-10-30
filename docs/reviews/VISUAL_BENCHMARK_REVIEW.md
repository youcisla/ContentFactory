# Visual Benchmark Review — "The Tap" POC

Date: 2026-10-30. Subject: 10-second WebGL proof of concept.
Self-review. The user alone approves creative direction.

---

## 1. Deliverables inspected

| Artefact | Check |
|---|---|
| `the-tap.mp4` | ffprobe: 1080×1920, 12 fps, 10.000 s, 120 frames, 1.33 MB |
| Frame at 9.5 s | Extracted and inspected: APPROVED screen, end title legible |
| Stills at 0.5 / 3.0 / 6.0 / 9.0 s | Inspected at native size |
| Mobile check | 1080 → 360 px display = ÷3 |

## 2. Score

| Criterion | Weight | Score | Weighted | Evidence |
|---|---:|---:|---:|---|
| Cinematic visual quality | 25 | **2.5** | 12.5 | Real perspective and lighting, but flat shading, no shadows/AO/DOF, simple forms |
| Educational clarity | 20 | **3.5** | 14.0 | Card → terminal → network → approval readable; network abstraction is thin |
| Animation and camera | 15 | **3.0** | 9.0 | One continuous eased move; timing works; no secondary motion |
| Art direction | 10 | **3.0** | 6.0 | Consistent palette and type; composition sparse |
| Mobile readability | 10 | **3.0** | 6.0 | Titles strong; terminal screen small at 360 px |
| Asset reuse / automation | 10 | **3.5** | 7.0 | Fully procedural and deterministic; assets are not reusable models |
| Resource efficiency | 5 | **4.5** | 4.5 | 254 s for 120 frames, no GPU, no installs |
| Licensing / compliance | 5 | **5.0** | 5.0 | All original; no third-party assets |
| **Total** | | | **64.0** | **Experimental — below the 90 target** |

Critical failures: none factual, legal, or security-related. The failure is creative.

## 3. Pass 1 — technical

| Check | Result |
|---|---|
| Frames / duration / fps | PASS (120 / 10.000 s / 12) |
| Resolution | PASS (1080×1920) |
| Determinism | PASS (`?t=` renders one frame) |
| External assets | PASS (none) |
| WebGL in headless | PASS with SwiftShader flag |
| Memory | **NOT MEASURED** |
| Audio | absent |

Defects found and fixed during build: card back-facing (rotX sign); card/terminal invisible at low albedo; screen hidden behind bezel; chip detached (world-space offset); NFC rings in the wrong plane; network nodes visible in shot 1.

## 4. Pass 2 — creative

| Observation | Assessment |
|---|---|
| Depth | Genuine perspective; objects sit in space |
| Lighting | Key + rim, but no contact shadows, so objects float |
| Materials | Uniform matte; card does not read as manufactured |
| Camera | Motivated continuous move; the rise into the network is the strongest beat |
| Composition | Card blocks part of the terminal at the climax |
| Pacing | 10 s for 6 beats is tight |
| Originality | Original mechanism treatment; generic dark-fintech look |
| Educational payload | Correct, but "settlement" is carried by text, not image |

## 5. Pass 3 — adversarial

1. "This looks like a dark 3D diagram, not a film." — **Fair.** No shadows, DOF, or material variation.
2. "The terminal is a grey box." — **Fair.**
3. "Where is the money? You only show a dot." — **Fair.** Settlement is asserted in a caption.
4. "12 fps is choppy." — **Fair**, disclosed.
5. "The network is five spheres and lines." — **Fair.**
6. "Does it teach?" — **Partly.** Sequence is accurate; the metaphor is thin.

## 6. Remaining limitations

No ray-traced shadows, AO, DOF, motion blur, or reflections; no authored assets; no audio; 12 fps; system fonts (cross-machine determinism unverified); terminal screen unreadable at 360 px.

## 7. What would move the score

| Change | Expected gain |
|---|---|
| Blender + authored models, Cycles/Eevee lighting | +15–20 cinematic |
| Contact shadows and AO (even faked) | +5 |
| 24–30 fps capture | +3 |
| Visual metaphor for settlement | +5 educational |
| Audio design | +3 |

None possible without a DCC tool or an approved download. That is the blocker.

## 8. Verdict

**64/100 — experimental.** Proves pipeline, determinism, mechanism. Does not meet the premium bar and must not be presented as the channel's visual identity.

Recommendation: treat as the technical baseline. Approve either (a) Blender installation for real 3D authoring, or (b) a personal machine with a discrete GPU. No further pipeline work until the visual gate passes user review.
