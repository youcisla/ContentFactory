# Shot template library

Every template is parameterised and renders from `templates/cf_studio_v1.blend`. A template is only listed as **built** when a frame has been rendered and inspected from it; everything else is a **spec** with its parameters named.

Global parameters shared by all templates: `fps` 24 · `resolution` 1080×1920 or 1920×1080 · `samples` 32 · `look` AgX Medium High Contrast · `motion_blur_shutter` 0.5 · `light_rig` key/fill/rim with measured powers 2.2 / 0.55 / 7.0 W.

| # | Template | Parameters | Status |
|---|---|---|---|
| 1 | Product macro closeup | `subject`, `lens` 85, `fstop` 5.6–11, `focus_target`, `push_mm` | **Built** — `shots/t01_product_macro.json`, rendered 1080×1920/32 spp in 13.94 s, exposure gate PASS |
| 2 | Object interaction | `actor`, `prop`, `contact_point`, `duration`, `lens` 50 | **Built (prop, no hand)** — `shots/t02_object_interaction.json`, card entering the slot, 13.09 s, gate PASS. A hand remains blocked on CF-149 |
| 3 | Technical cutaway | `assembly`, `cut_plane`, `explode_distance`, `lens` 50 | **Built as mechanism reveal** — `shots/t03_cutaway.json`, hovering card over the reader, 13.51 s, gate PASS. Exploded-part variant needs append mode |
| 4 | Camera tracking reveal | `path`, `ease`, `duration`, `lens` 35 | Spec — V4 dolly is the working precedent |
| 5 | Network / data-flow | `nodes`, `edges`, `packet_path`, `depth_fog` | Spec — 2D version exists as SVG in `render/scenes/` |
| 6 | Exploded mechanism | `parts`, `axis`, `spacing`, `stagger_ms` | Spec |
| 7 | Before / after comparison | `state_a`, `state_b`, `split` or `cut` | Spec |
| 8 | Stylized character interaction | `character`, `clip`, `camera` | Spec — blocked on a licensed rig |
| 9 | Environmental establishing | `set`, `lens` 24–35, `crane_height` | Spec |
| 10 | Educational summary reveal | `lines`, `reveal_order`, `hold_ms` | Spec — 2D version shipped in the animatic |

## Why only three are built

A shot template is a promise that a shot can be produced quickly and repeatably. Producing ten empty shells would satisfy a count and prove nothing. Three are verified end to end from JSON against the linked terminal asset; seven have their parameters defined so that building them is a bounded task, not a design exercise.

## Running a template

```
blender.exe -b -P tools/shot_render.py -- shots/t01_product_macro.json
```

The spec is the only input; the renderer links `assets/models/terminal_master.blend`, applies the spec and writes a sidecar with the cache key, template hash and seconds. An unchanged spec returns from `render/cache/` in about 0.9 s.

## Template contract

A built template must satisfy all of:

1. It renders headless from the saved `.blend` with no script edits — only parameters.
2. Its camera move is defined by keyframes inside the template, not by a per-shot Python file.
3. Its light rig comes from the template's `LIGHTS` collection; a shot may move lights but not invent a new rig without recording why.
4. It records `cf_template` and the template's hash in the render job.
5. It passes the geometry gate before any sequence render.

## Colour-location rule (inherited from the script)

Green appears only on the terminal and the returning packet. Never on the card. Any new template that breaks this rule is rejected, not adjusted.

## Blockers

| Template | Blocked by |
|---|---|
| 2 (hand version), 8 | A rigged character/hand under a usable licence (CF-149) |
| 6 | Exploded-part shots need append mode or library overrides (linked collection is atomic) |
| 5 | Decision: keep the existing SVG diagram path or move it into 3D |
