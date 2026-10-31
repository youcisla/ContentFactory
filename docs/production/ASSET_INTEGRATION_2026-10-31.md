# Asset integration — payment terminal into the studio template (CF-151 integration half)

Date: 2026-10-31. Implements ADR-0007 rule 1–3 for one hero prop. Reproducible from two commands.

## Pipeline

```
assets/models/receipt-point-of-sale-terminal.glb   (untouched download, sha256 in manifest)
        │  tools/build_terminal_master.py
        ▼
assets/models/terminal_master.blend                (adapted master, collection ASSET_Terminal)
        │  tools/shot_render.py  — bpy.data.libraries.load(link=True)
        ▼
templates/cf_studio_v1.blend  +  collection instance PROP_Terminal
        │  JSON shot spec
        ▼
render/stills/<shot>.png  +  <shot>.json sidecar (cache key, template hash, seconds)
```

## Link vs append vs override — what was evaluated

| Mechanism | Verdict here |
|---|---|
| **Link collection + `Collection Instance` object** | **Used.** One master file; the instance object's transform is editable without a library override, so every shot places/rotates/scales the terminal from JSON. The master stays immutable during rendering. |
| Append (local copy) | Not used. Every delivered shot only moves the whole asset; nothing edits its meshes, materials or hierarchy per shot. Appending would duplicate 5,100 tris per render with no benefit. |
| Library override | Not needed. Overrides would only be required to edit linked *object* or *material* data per shot; the only per-shot data are the instance transform and the additive screen text, which are local objects. |

One limitation is recorded rather than worked around: a linked collection is atomic, so a per-part shot (e.g. exploding keycaps) would require append or overrides. The mechanism-reveal shot therefore uses an additive local card prop, not an edit of the linked asset.

## Adaptation performed (the whole of it)

`tools/build_terminal_master.py`:

1. Imports the GLB into an empty scene and moves every object into one collection, `ASSET_Terminal`.
2. Recentres X/Y on the mesh bounds and puts the base at `z = 0` (offset `(-0.0, -0.002, -0.0)` m).
3. Assigns the four material appearances the GLB omits (see `ASSET_EVALUATION_2026-10-31.md` §defects):
   - Black molded polymer — base `0.012`, roughness 0.45
   - Charcoal powdercoat — base `0.030/0.031/0.034`, roughness 0.58
   - Dark inactive display glass — base `0.004`, roughness 0.10, coat 0.8
   - Warm ivory satin enamel — base `0.68/0.63/0.54`, roughness 0.38
4. Writes scene metadata: `cf_asset_id`, `cf_asset_source`, `cf_asset_licence`, `cf_asset_triangles`.
5. Saves `terminal_master.blend`. No scale change; the GLB is already in metres.

## Checks against the brief's checklist

| Requirement | Evidence |
|---|---|
| Correct dimensions and orientation | Imported size `0.100 × 0.222 × 0.1005 m` (real terminal footprint); base at z=0; customer face on −Y |
| Valid normals | 5,100 tris render without black/inverted faces in Eevee; glTF importer computed normals |
| Proper materials | Four materials assigned and rendered; the display reads dark glass, keys ivory, body black |
| Working textures | None exist to break — the asset has no image maps; nothing to relink |
| Sensible origin and transforms | Origin centred on the footprint, base at 0; the instance object carries shot transform |
| No missing dependencies | `IMAGES []` after import; master opens standalone |
| Consistent object naming | Imported names kept (`Tactile key.000–011`, `Terminal display`, …) |
| Correct asset metadata | Scene custom properties + manifest row + this document |
| Reproducible import | `blender -b -P tools/build_terminal_master.py` then `blender -b -P tools/shot_render.py -- shots/<spec>.json` |

## Verified numbers

| Item | Value |
|---|---|
| GLB | 204,384 B, sha256 `fd49c930…a93b6` |
| Triangles / meshes / materials | 5,100 / 17 / 4 |
| Import time (headless) | < 2 s |
| Still render, 540×960/16 spp | 3.5–6.9 s |
| Still render, 1080×1920/32 spp | 13.1–15.9 s |
| Cache hit re-run | **0.90 s** wall clock vs 15.89 s rendered |

## Security note

The GLB is third-party data. It was imported in a headless Blender session with no auto-run scripts executed from the file; Blender does not execute glTF content. The master `.blend` contains no Python or drivers.
