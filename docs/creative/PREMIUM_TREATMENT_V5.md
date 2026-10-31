# Premium Treatment V5 — "The Handoff"

Status: pre-production. Not built, not rendered, not accepted.
Supersedes `TREATMENT_TAP.md` for 3D work. `TREATMENT_TAP.md` described the WebGL POC and stays as history.
Sibling documents: `SCRIPT_CONTACTLESS.md` (claims), `STORYBOARD_CONTACTLESS.md` (40 s cut), `BENCHMARK_SPEC_PREMIUM.md` (V4 spec).

---

## 1. Why V5 exists

V4 proved the host can render. It did not look premium, because every object in it was invented from primitives and the camera was a mathematical dolly. V5 changes the three things that actually decide perceived quality, in this order:

1. **What is in frame** — real, reference-faithful props, dressed set, no bare primitives.
2. **How it is lit and shot** — lens discipline, light ratio, depth of field, motion blur, imperfections.
3. **What the edit does** — motivated cuts and one rack focus that carries the argument.

The evidence for that order is in `docs/research/open-source-projects/EVALUATION_2026-10-31.md` and the creator-pipeline research summarised in ADR-0007: Zack D. Films buys consistency from templates and asset reuse; Branch Education buys credibility from reference fidelity. Both spend their quality budget on camera and light, not on more polygons.

## 2. The original idea — the focus pull is the argument

The film's claim is **"approved is a hold, not a payment"**, and the visual proof in V4 was a colour rule: green appears on the terminal, never on the card.

V5 makes the same argument with the lens. In shot 3, focus racks from the **card** (sharp) to the **terminal screen** (sharp) while the card falls soft. The viewer's attention moves exactly where the money did not. No narration is needed to explain it; the focus pull is the sentence.

That is the one directed moment the film is built around. Everything else supports it.

## 3. Art direction

Physical-product photography, not motion graphics. A dark counter, one hero object at a time, real depth.

| Token | Value | Use |
|---|---|---|
| Void | `#05070D` | Background falloff |
| Graphite | `#12161F` | Terminal chassis |
| Steel | `#2A3340` | Bevels, card slot |
| Signal cyan | `#22D3EE` | Field / idle screen |
| Approval green | `#34D399` | Terminal screen and indicator only |
| Warning amber | `#F5B547` | Chip |
| Paper | `#E6EDF7` | Captions |

Rules kept from the script's visual contract: green never appears on the card; no radio arcs; no money imagery; no brand marks; no diegetic text smaller than 42 px at 1080 width.

**New in V5:** surface imperfection is mandatory. Card and terminal carry a multi-scale roughness breakup (fingerprints on gloss, dust in crevices, micro-scratches on the card face). A perfectly clean CG surface is the amateur tell.

## 4. Craft standard (checkable)

| # | Rule | Value |
|---|---|---|
| C1 | Lens per shot | 85 mm macro / 50 mm / 35 mm; never the default 50 mm for everything |
| C2 | Aperture | Chosen from a depth-of-field budget at the real subject distance, not a fixed number. Measured on 2026-10-31: at ~0.35 m with a 65 mm lens, f/5.6 blurs the whole set and f/16 restores baseline sharpness. At tabletop distances, wide apertures are only usable when the background is ≥ 0.5 m behind the subject. Focus target named per shot |
| C3 | Key light | area light ≈ 2× subject width, 45° side and elevation |
| C4 | Ratio | key:fill 3:1–4:1; rim 150–250 % of key behind the subject |
| C5 | Environment | low-strength HDRI (≤ 0.3) for reflections, never as the only light |
| C6 | Shutter | 180° — `motion_blur_shutter = 0.5` at 24 fps |
| C7 | Grade | AgX Medium High Contrast, lifted blacks ≈ 8–12/255, light grain, subtle bloom |
| C8 | Movement | every camera move motivated: push, parallax, or focus pull. No locked-off shot |
| C9 | Detail hierarchy | hero prop, 2–3 supporting props, background falloff; nothing else |
| C10 | Sound | foley tap, terminal chirp, sub hit on green, room tone (blocked — CF-139) |

Blender 5.2 API confirmed on this host: camera `dof.use_dof`, `aperture_fstop`, `focus_object`; `render.use_motion_blur` with `motion_blur_shutter` default 0.5.

## 5. Shot list — 11.0 s, 24 fps, 264 frames

Four shots, three cuts. Each cut lands on an action, not on a beat of narration.

| # | Time | Lens | Aperture | Focus | Camera | Action | Why the cut is here |
|---|---|---|---|---|---|---|---|
| S1 | 0.0–2.6 | 85 mm | f/2.0 | chip | Slow push, low | A hand brings the card into a dark frame; rim light finds the card edge; chip catches amber | Establishes the object before the mechanism |
| S2 | 2.6–5.6 | 50 mm | f/2.8 | card face | Low angle, slight parallax | Card crosses into the reader's field; coil lights from the edge inward; screen wakes cyan | Cut on the coil ignition — the cause begins here |
| S3 | 5.6–8.8 | 35 mm | f/4.0 | **racks card → screen** | Slow lateral drift | Both objects in frame; screen turns green; focus leaves the card and lands on the terminal | The argument: attention moves, the money does not |
| S4 | 8.8–11.0 | 85 mm | f/2.0 | screen | Static frame, hand-held micro-motion | Screen holds green, card soft in foreground; caption lands | Room for the reversal to stick |

Mobile framing: card occupies 35–50 % of frame width in S1; screen text region stays inside the centre 60 % safe area; no element within 8 % of any edge.

## 6. Asset requirements

| Slot | Requirement | Source status |
|---|---|---|
| Terminal | Modelled in-house to reference; generic design, no brand | To model (est. 4–6 h) |
| Card + chip | Modelled in-house; exact ISO/IEC 7810 proportions | Reuse V4 geometry, re-material |
| Hand | Rigged, CC0, neutral skin tone; only fingers and edge of palm in frame | **Unverified** — see asset strategy |
| Counter surface | PBR material set, CC0 | **Acquired** — `metal_plate` 2K + `Plastic013A` 1K, `assets/manifest.json` (CF-140) |
| HDRI | Studio interior, CC0, ≤ 0.3 strength | **Acquired and load-tested** — `brown_photostudio_02` 2K HDR renders headless via `CF_ASSET_HDRI` (26.81 s at 1080×1920 / 32 spp) |
| Set dressing | 2–3 small props, CC0 or modelled | To decide |

No asset enters the scene without a `commercial_ok=true` row in `assets/manifest.json`.

## 7. What V5 changes against V4

| | V4 (baseline) | V5 |
|---|---|---|
| Geometry | 100 % procedural primitives | Modelled hero props + CC0 assets |
| Camera | One continuous dolly | Four shots, three motivated cuts |
| Lens | Single FOV | 35 / 50 / 85 mm discipline |
| Depth of field | None | Per-shot, with one rack focus |
| Motion blur | None | 180° shutter |
| Materials | Four-value helper, uniform | Multi-scale imperfection, texture |
| Environment | Procedural gradient | Low HDRI + formula light rig |
| Grade | AgX, look None | AgX Medium High Contrast + grade |
| Sound | None | Foley + sub hit (blocked) |

## 8. Cost, measured and estimated

| Item | Value | Basis |
|---|---|---|
| Frames | 264 at 1080×1920 | 11.0 s × 24 fps |
| Render, 8 spp | ≈ 10–13 s/frame → 44–57 min | V4 measured 8.51 s/frame **without** DOF or motion blur. Lens probe at 1080×1920 / 32 spp measured **14.83 s** baseline, **21.46 s** with f/2.8 DOF + 180° blur (+45 %), **21.91 s** at f/5.6 + blur, **17.42 s** at f/5.6 without blur, **13.01 s** at f/16 without blur. DOF alone is not the cost; motion blur is. Adding the CC0 HDRI world raises the same still to **26.81 s** (+81 % over baseline): the HDRI is the single most expensive change measured so far, and at strength 0.3 it changed the image only subtly. Environment is not a substitute for geometry |
| Disk | ≈ 480 MB PNG | V4 measured 1.82 MB/frame |
| Samples | 32 for final stills, 8 for motion preview | V4 sample-count evidence |

264 frames exceeds the 15-minute benchmark rule in `BENCHMARK_SPEC_PREMIUM.md`. Two honest options: preview at 540×960 (≈ 2.5–3 s/frame → 11–13 min), or accept a longer final and record it as a deliberate exception. This document does not silently relax the rule.

## 9. Acceptance criteria

1. Every asset has a licence row; no brand marks.
2. The focus pull in S3 reads at 360 px width without captions.
3. Card and terminal read as manufactured objects, not primitives — checked against a real photograph.
4. No shadow acne, flicker, z-fighting, or visible intersection.
5. Geometry gate and exposure gate pass unchanged.
6. Blind side-by-side against V4: an independent viewer prefers V5, and can say why.
7. Creative acceptance is the user's. A passing render is not an acceptance.

## 10. Blockers, stated exactly

| Blocker | What it needs | Task |
|---|---|---|
| Asset download | Named approval for a small CC0 set (~50–100 MB) | CF-140 |
| Hand asset | Licence-verified rigged hand, or drop the hand and use a card stand | open |
| Scene template | `.blend` template with rigs and linked collections | CF-142 |
| Render budget | Decide preview resolution vs 15-minute rule | CF-144 |
| Audio | Recording or model-download approval | CF-139 |

Until CF-140 and CF-142 close, no V5 frame can be rendered. That is the exact authorisation blocker, not a scheduling preference.
