# Asset strategy — 2026-10-31

Supersedes `SHORTLIST.md` as the detailed record. The 2026-10-30 shortlist stays as history and its provenance rules are reused unchanged.
Scope: assets for an asset-driven premium 3D benchmark on contactless payments (card, terminal, hand, surface, environment).

Confidence tags: **VERIFIED** (index, licence page, or API read directly) · **DOCUMENTED** · **INFERRED** · **UNKNOWN**.

---

## 1. The finding that decides the plan

**No CC0 payment terminal or credit card exists in any of the major free libraries.** Poly Haven's 521-model index was scanned; the only regex hits for card/terminal/payment/reader are `CashRegister_01` (a vintage mechanical till) and `postcard_set_01`. Sketchfab's CC0 filter returns zero downloadable payment terminals, card readers or credit cards — the filter was sanity-checked against a control query.

Two consequences:

1. An asset-driven benchmark cannot be built from CC0 alone. Either hero props are modelled in-house (V4 already has a working card), or a **CC BY** model is used with a credit line.
2. The asset strategy is therefore a **mixed** strategy: CC0 for environment and materials (where CC0 supply is excellent), in-house or CC BY for hero props (where CC0 supply is empty).

## 2. Source-by-source

| Source | Licence model | Commercial | Attribution | Per-asset variation | Account | Verdict |
|---|---|---|---|---|---|---|
| [Poly Haven](https://polyhaven.com/license) | CC0 | yes | no | no | no | **Adopt** — HDRIs, PBR textures |
| [ambientCG](https://ambientcg.com/) | CC0 | yes | no | no | no | **Adopt** — PBR sets |
| [Blender Studio](https://studio.blender.org/) | CC BY 4.0 (asset pages state the licence) | yes | **yes** | yes | no for free assets | **Conditional** — characters with credit |
| [Sketchfab](https://sketchfab.com/) | per model, set by uploader | varies | varies | **yes** | yes to download | **Conditional** — CC BY only, credit each |
| [BlenderKit](https://www.blendkit.com/) | Royalty Free or CC0, per asset | yes | no | yes | yes + add-on | **Avoid for now** — the terminal is paid |
| [Kenney](https://kenney.nl/assets) | CC0 | yes | no | no | no | No relevant props |
| [Quaternius](https://quaternius.com/license.html) | **QAL v1.0** since 2026-08-28 | yes | no | no | no | **Reject** — licence conflict; no redistribution |
| [Poly Pizza](https://poly.pizza/) | CC0 / CC-BY 3.0 per model | yes | varies | yes | no | Optional — no payment props found |
| [Rigger](https://github.com/asu37/Rigger) | GPL-3.0-or-later | tool, not content | n/a | n/a | no | Tooling only; contains no models |
| Blender Asset Browser | n/a | n/a | n/a | n/a | no | Mechanism, not a source |

## 3. What exists that we can actually use

### Environment — CC0, unrestricted

| Asset | Source | Size | Use |
|---|---|---|---|
| `brown_photostudio_02` HDRI | https://polyhaven.com/a/brown_photostudio_02 | 4K HDR 25.4 MB; 2K 6.5 MB | Studio reflections at ≤ 0.3 strength |
| `metal_plate` PBR set | https://polyhaven.com/a/metal_plate | ~3 MB per map at 2K | Counter / chassis wear |
| Any ambientCG plastic or metal set | https://ambientcg.com/ | 1K–8K, 7–77 MB | Card body, terminal shell |

Poly Haven's studio HDRIs include `brown_photostudio_01–07`, `blue_photo_studio`, `blocky_photo_studio`, `photo_studio_01`, `art_studio`. All CC0, no account, no attribution.

### Hero props — no CC0 option

| Asset | Source | Licence | Size / complexity | Note |
|---|---|---|---|---|
| Chip and PIN card reader | https://sketchfab.com/3d-models/chip-and-pin-card-reader-ccc9d1a3f47b4537ac5b8cf75196c40c | **CC BY 4.0** | 12,874 faces | Closest usable terminal; credit required |
| PAX-A920 (high-poly) | https://sketchfab.com/3d-models/pax-a920-highpoly-1715b1517d884e4785713fcd7289f284 | CC BY 4.0 | 166,845 faces | Real brand device — **reject**: brand marks and trade dress |
| Payment terminal | https://sketchfab.com/3d-models/payment-terminal-12376a29b015453da5f7a0deede21dd8 | CC BY 4.0 | 1,848 faces | Low detail; likely a stand-in only |
| Credit card | https://sketchfab.com/3d-models/credit-card-4c4117d766f342cc9e0fa3d79e9de654 | CC BY 4.0 | 17,254 faces | Card is already modelled in-house; use only if better |

The PAX model is rejected on brand grounds, not licence grounds: the script's visual contract forbids brand marks and card-network logos. Any real device with a visible logo fails it.

### Hand — the honest gap

**No verified CC0 rigged human hand exists.**

- Poly Haven: none.
- Sketchfab CC0 "hand" results are museum casts (e.g. Life Cast of Left Forearm and Hand, ~150k faces) — reference geometry, unrigged.
- Blender Studio `Pip` and `Rain` are rigged characters under **CC BY 4.0**, free download — usable with credit, but stylised, not photographic hands.
- Blender Studio **Human Base Meshes v1.4.1** is **CC0**, 49 MB, distributed via https://www.blender.org/download/demo-files/ — unrigged; pair with Rigify or Rigger (GPL tooling).

Decision for V5: either (a) drop the hand and use a card stand / rig that holds the card, keeping the film object-focused, or (b) accept a CC BY character rig with credit, or (c) model and rig a hand in-house. (a) is the only option that needs no new licence obligation; the treatment's shot list can lose the hand without losing the argument.

## 4. Licence obligations that must reach the video

- **CC BY 4.0** requires credit. If a Sketchfab model or Blender Studio character is used, the credit line goes in the video description and in `assets/manifest.json`.
- **CC0** requires nothing, but provenance is still recorded.
- **Quaternius QAL** forbids redistribution of the assets themselves; a rendered video is not redistribution of the asset, but the site contradicts itself (pack pages still say CC0). Treat as unusable until written confirmation.
- **NC licences** are unusable for a monetised channel. Sketchfab must be filtered to CC0/CC BY only, per model.

## 5. Proposed acquisition set (smallest useful)

| Item | Licence | Size | Purpose |
|---|---|---|---|
| `brown_photostudio_02` 2K HDR | CC0 | 6.5 MB | Reflections and soft fill |
| `metal_plate` 2K PBR set | CC0 | ~12 MB (4 maps) | Counter / wear |
| One plastic PBR set (ambientCG) | CC0 | ~10 MB | Card and terminal roughness |
| **Total** | | **< 30 MB** | Well under the 100 MB task cap |

Hero props are modelled in-house. No CC BY asset is required for a first benchmark, which keeps the credit obligation at zero. If the terminal model proves too costly in hours, the Sketchfab CC BY reader is the fallback with a credit line.

## 6. Integration requirements

1. `assets/manifest.json` row per file: `path`, `source_url`, `author`, `licence`, `retrieved_at`, `commercial_ok`, `attribution_required`.
2. The validator (CF-141) fails the build on a missing field or `commercial_ok=false`.
3. Files are referenced by relative path from the `.blend` template; no absolute machine paths (ADR-0006).
4. Textures are downsampled to 2K for render; 4K/8K sources are not committed.
5. Attribution lines are generated from the manifest, not typed by hand.
6. No asset collection is downloaded wholesale; only the rows above.

## 7. Blockers

| Blocker | Needs |
|---|---|
| Download of ~30 MB CC0 set | Named approval (CF-140) |
| Terminal geometry | 4–6 h modelling, or CC BY fallback |
| Hand | Decision: drop, CC BY, or model in-house |

## 8. Open questions

1. Whether Sketchfab's CC BY models download in a Blender-importable format was not verified per asset.
2. Poly Pizza search timed out; a card asset may exist there (UNKNOWN).
3. Kenney download formats are not stated on pack pages (INFERRED only); no relevant pack was found anyway.
