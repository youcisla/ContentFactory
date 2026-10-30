# Asset Shortlist — premium payment scene

Scope: assets for a realistic card / terminal / environment scene. Hero props are modelled, not downloaded.

---

## 1. Hero props (model in Blender)

| Asset | Why model it | Effort [E] |
|---|---|---|
| Payment card | Exact proportions, clean topology, custom material, no brand marks | 2–4 h |
| EMV chip | Simple hard-surface; metal material | 30 min |
| Payment terminal | Generic design, screen plane, keypad recess | 3–5 h |
| Counter / surface | Simple bevels, procedural material | 1 h |

Rationale: generic terminal models are scarce, often branded, and licence-unclear. Modelling removes all three problems.

## 2. Environment and lighting

| Source | Licence | Use | Status |
|---|---|---|---|
| **Poly Haven** | **CC0** | HDRIs for reflections and ambient light | [U] verified |
| **ambientCG** | **CC0** | Plastic, metal, concrete PBR sets | [U] verified |
| **Kenney** | **CC0** | Generic props if needed | [U] verified |

CC0: no attribution, commercial use permitted.

## 3. Secondary model libraries (optional)

| Source | Licence model | Risk | Recommendation |
|---|---|---|---|
| BlenderKit | mixed: CC0 and royalty-free, account + add-on | varies per asset | Use only if it saves hours; record ID and licence |
| Poly Pizza | CC0 / CC-BY | site unreachable during audit | Verify per model |
| Sketchfab | per model, many CC-BY-NC | NC unusable for monetised video | Filter to CC0/CC-BY and record |
| Fab / Quixel | Epic account terms | not clearly commercial-safe for standalone video | Avoid |
| CGTrader / Free3D | per model, often unclear | high contamination risk | Avoid |

## 4. Audio (future)

| Source | Licence | Note |
|---|---|---|
| Freesound | per sound (CC0 / CC-BY / CC-BY-NC) | filter to CC0 or CC-BY |
| Kenney audio packs | CC0 | UI and interface sounds |

No audio in the current POC.

## 5. Provenance rules

1. Every asset row carries `source_url`, `licence`, `retrieved_at`, `commercial_ok`.
2. `commercial_ok=false` fails validation.
3. CC-BY requires attribution in the video description.
4. No asset enters the pipeline without a recorded licence.

## 6. What not to use

- Brand logos, card-network marks, bank trade dress.
- Any model licensed "personal use only" or "editorial only".
- AI-generated assets whose model terms forbid commercial use.
