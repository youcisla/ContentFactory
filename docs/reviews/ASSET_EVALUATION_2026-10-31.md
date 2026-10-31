# Asset evaluation — payment terminal (CF-150)

Date: 2026-10-31. Scope: pick one hero payment terminal for the studio template under ADR-0007 rule 1 (`source_url`, `licence`, `commercial_ok=true`, sha256).
Verdict: **Innerscene "Counter Pay" payment terminal selected** — the only purpose-built card terminal found with a direct, no-account CC0 download.

## Candidates

| # | Candidate | URL | Author | Licence | Commercial | Size | Geometry | Materials / textures | Import | Visual quality | Render cost | Adaptation effort |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | **Counter Pay — Payment Terminal** (selected) | https://www.innerscene.com/tools/library/3d-parts/counter-pay-payment-terminal-74006716 | Innerscene | **CC0** | yes, no attribution | 204,384 B (0.2 MB) | **5,100 tris**, 17 meshes | 4 named PBR materials; **no image textures** | GLB → Blender 5.2.3 importer, no errors | High: clean product model, correct proportions, real-world scale | 13–16 s/still at 1080×1920/32 spp measured | **Low**: assign four base colours (the GLB ships all four at the 0.8 grey default); centre origin |
| 2 | Card payment terminal (Cafe/Bakery) | https://3dassets.dev/assets/bakery-and-cafe-card-terminal-be093cc9 | 3D Assets | **CC0** | yes | 0.06 MB | 1,254 tris, 4 meshes | 4 materials, 0 textures | GLB (CDN, direct) | Unknown — AI-generated per listing; lower detail than #1 | Would be cheaper | Not downloaded; listing states screen, 9-key pad, slot |
| 3 | GAME READY POS-TERMINAL | Sketchfab, recorded in `ASSET_STRATEGY_2026-10-31.md` §4 — URL not re-opened this pass | Oxygen3D | CC BY 4.0 (recorded) | yes with credit | not recorded | **4,146 faces** | not recorded | account-gated `glb`/`fbx` | Unknown | unknown | **Gated**: Sketchfab login required |
| 4 | Chip and PIN card reader | https://sketchfab.com/3d-models/chip-and-pin-card-reader-ccc9d1a3f47b4537ac5b8cf75196c40c | not recorded | CC BY 4.0 (recorded) | yes with credit | not recorded | 12,874 faces | not recorded | account-gated | Unknown | higher poly | **Gated** |
| 5 | POS terminal (Vladyslav.Yarovyi) | recorded in `ASSET_STRATEGY_2026-10-31.md` §4 | Vladyslav.Yarovyi | CC BY 4.0 (recorded) | yes with credit | not recorded | 38,444 faces | not recorded | account-gated | Unknown | higher | **Gated**; brand inspection needed |
| 6 | Payment terminal | https://sketchfab.com/3d-models/payment-terminal-12376a29b015453da5f7a0deede21dd8 | not recorded | CC BY 4.0 (recorded) | yes with credit | not recorded | 1,848 faces | not recorded | account-gated | Low detail stand-in | low | **Gated** |
| 7 | POS terminal digital cash register (brief's fallback) | https://sketchfab.com/3d-models/pos-terminal-digital-cash-register-dd3b0ff62c044d8ebe59c8cdab2c6fc9 | not recorded | CC BY (per brief) | yes with credit | not recorded | ~86,600 tris (brief) | not recorded | account-gated | Unknown | ~17× #1's triangles | **Gated**; complexity excessive for this host |
| 8 | Card Reader | https://poly.pizza/m/ZhjtUap8Ng | J-Toastie | CC BY 3.0 | yes with credit | not recorded | not shown (low-poly) | GLTF/FBX | direct download | Stylised only, low-poly | low | Attribution + likely too simple for macro |
| 9 | POS Machine | recorded in `ASSET_STRATEGY_2026-10-31.md` §4 | J-Toastie | CC BY 3.0 | yes with credit | not recorded | not shown | GLTF/FBX | direct | Low-poly, stylised | low | Attribution |
| 10 | Cash Register 01 | https://polyhaven.com/a/CashRegister_01 | Joe Seabuhr | **CC0** | yes, no attribution | 1.0 MiB GLB (1k textures) | 9,927 tris | 2 materials, PBR maps | glTF via public API `api.polyhaven.com/files/CashRegister_01` | Photoreal | similar | **Wrong subject** — vintage mechanical till; valid as set dressing only |

## Why #1 wins

- **It is the actual subject.** Every other terminal is either gated, low-poly, or the wrong device.
- **Direct download, no account**: `https://www.innerscene.com/api/library/counter-pay-payment-terminal-74006716/download` returns `302` to a 204 KB GLB. No login, no email.
- **CC0**, so no attribution obligation and no NC risk on a monetised channel.
- **5,100 triangles** import and render in 13–16 s per 1080×1920 still; the 86k fallback would cost roughly 17× the geometry for an unverified look.
- The mesh is **partitioned by function** (`Card-insertion slot`, `Tactile key.000–011`, `Terminal display`, `Receipt roll enclosure`, `Payment-terminal base`), which makes part-level shots possible without editing the asset.

## Verified defects found during adaptation

1. **All four materials import with base colour `0.8, 0.8, 0.8`.** The GLB carries material *names* ("Black molded polymer", "Charcoal fine-textured powdercoat", "Dark inactive display glass", "Warm ivory satin cabinet enamel") but not usable colours. Rendering without adaptation produces a uniformly grey object and a blown top panel. Fixed in `tools/build_terminal_master.py` by assigning colour, roughness, metallic and coat per name.
2. **No texture maps.** "Textured PBR" in the listing means PBR parameters, not image maps. All appearance comes from the four material definitions; there is nothing to pack or relink.
3. **Screen is a flat upward-facing glass panel**, not a tilted HMI. Screen content is added by `tools/shot_render.py` as emissive text parented to the terminal instance, not modelled into the asset.

## Licence record

Manifest row `receipt-pos-terminal-cc0` in `assets/manifest.json`: `source_url`, `author` = Innerscene, `licence` = CC0, `retrieved_at` = 2026-10-31, `retrieved_from` = the download endpoint, `commercial_ok` = true, `sha256` = `fd49c9304bc1a9e617203c64b7188608faabbc0855902e5b135311b2f9aa93b6`, 204,384 bytes. No credit line is owed; one is given anyway in the project README.

## Not verified

- Sketchfab items were **not** re-opened this pass; their rows carry the earlier research's licence readings. A download would need an account, which is the gating condition.
- Candidate 2's visual quality is listed, not inspected; it was not downloaded.
- No brand-mark audit was performed beyond the mesh names and renders; the renders show a generic dark terminal with no visible logo.
