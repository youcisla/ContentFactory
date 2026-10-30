# Blender Feasibility — Premium 3D on this laptop

Task: CF-018. Date: 2026-10-30. Research only. **Nothing installed, downloaded, or rendered.**
Labels: **[U]** verified upstream · **[M]** measured locally · **[E]** estimate · **[?]** unknown.

---

## 1. Framing correction

The earlier audit said "no supported Cycles GPU" and treated that as "3D is not possible". Too broad.

**Cycles GPU** and **Eevee** are different backends:

| Backend | Requirement | This machine |
|---|---|---|
| Cycles GPU | CUDA / OptiX, HIP, or Intel Arc oneAPI | **Unsupported** (iGPU is not Arc) |
| Cycles CPU | any x86-64 | Supported, slow |
| **Eevee** | GPU with **OpenGL 4.3 or Vulkan 1.3**, ≥2 GB VRAM | **Expected supported** — driver 32.0.101.8860, Arrow Lake iGPU |
| Workbench | same as Eevee | Supported |

## 2. Verified facts

| Item | Value | Status |
|---|---|---|
| Current Blender release | **5.2.3 LTS** | [U] blender.org/download |
| Windows support | Windows 11 supported; Windows 8.1 minimum | [U] |
| GPU minimum | 2 GB VRAM, OpenGL 4.3, Vulkan 1.3 | [U] requirements page |
| Intel GPU minimum | Kaby Lake architecture or newer | [U] |
| Local adapter | Intel integrated, Arrow Lake class, driver 32.0.101.8860 (2026-06-25) | [M] |
| Windows installer size | **349 MB** | [U] download page |
| Installed footprint | ~1.5 GB (portable ZIP similar) | [E] |
| Licence | **GPL** — output is not a derivative work | [U] |
| Commercial use of renders | Permitted | [U]/[I] widely accepted, not legal advice |
| Blender installed? | **No** | [M] |
| Disk free | 58.2 GB | [M] |

**Conclusion:** Eevee is *expected* to run. "Expected" is not "verified" — a background render test is required before any production claim.

## 3. Install options

| Option | Footprint | Reversibility | Notes |
|---|---|---|---|
| Windows installer (349 MB) | ~1.5 GB, Program Files | Uninstall via Windows | Needs elevation |
| **Portable ZIP into project folder** | ~1.5 GB, no registry | Delete folder | Preferred on a managed device |
| Steam | ~2 GB | Uninstall | Adds Steam dependency |
| Chocolatey/winget | download | uninstall | Package-manager policy risk |

Recommendation: **portable ZIP** under a project directory. No installer, no registry, no service, reversible by deletion.

## 4. Eevee performance expectation

| Factor | Assessment | Status |
|---|---|---|
| 1080×1920, 64 TAA samples | plausible at ~0.5–2 s/frame on this iGPU | [E] |
| 240 frames (10 s @ 24 fps) | ~2–8 minutes per pass | [E] |
| Peak RAM | 2–6 GB, scene dependent | [E] |
| VRAM | shared system memory; 2 GB reported | [M] |
| Background rendering (`-b`) on iGPU | supported on Windows; untested here | [?] |
| Motion blur / DOF | supported in Eevee; cost rises | [U] |
| Bloom | not built into Eevee Next; use compositor Glare | [U] |
| Ray-traced shadows | unavailable in Eevee; use shadow maps + AO | [U] |

Replace every [E] with a measured single-frame test before scheduling production.

## 5. Asset strategy

Realistic card and terminal are **not** well served by free libraries: generic terminals are rare and downloaded models often have unclear licences. Model both; use CC0 only for environment.

| Asset | Source | Licence | Status |
|---|---|---|---|
| Card, chip, terminal | **Model in Blender** | Original | Recommended |
| HDRIs | Poly Haven | **CC0** | [U] verified |
| PBR textures | ambientCG | **CC0** | [U] verified |
| Generic props | Kenney | **CC0** | [U] verified |
| Extra models | BlenderKit | mixed | [?] per-asset |
| Extra models | Poly Pizza | CC0 / CC-BY | [?] site unreachable this pass |
| Extra models | Sketchfab | per asset, many NC | [?] check each |
| Quixel / Fab | Epic terms | restrictive | Avoid |

Full shortlist: `docs/research/assets/SHORTLIST.md`.

## 6. Options compared

| Criterion | Weight | Local Blender Eevee | Remote Blender | Improved WebGL |
|---|---:|---:|---:|---:|
| Cinematic visual quality | 25 | 4.0 | 4.5 | 3.0 |
| Educational clarity | 20 | 4.5 | 4.5 | 4.0 |
| Animation / camera | 15 | 4.0 | 4.5 | 3.5 |
| Art direction | 10 | 4.0 | 4.5 | 3.5 |
| Mobile readability | 10 | 4.0 | 4.0 | 3.5 |
| Reuse / automation | 10 | 4.0 | 4.5 | 4.0 |
| Resource efficiency | 5 | 2.5 | 3.5 | 4.5 |
| Licensing / compliance | 5 | 5.0 | 4.0 | 5.0 |
| **Weighted total** | | **81.5** | **87.5** | **73.0** |

### Interpretation

- **Remote Blender** wins on quality and reuse; loses on recurring cost, transfer, and vendor terms.
- **Local Eevee** is ~6 points behind, entirely on render speed and hardware ceiling — not output quality.
- **Improved WebGL** can gain polish but cannot reach authored hard-surface realism.

## 7. Adversarial review

| # | Challenge | Response |
|---|---|---|
| A1 | "Eevee might not work on this iGPU." | Requirements met on paper; a 1-frame background test is the only proof. Gate on it. |
| A2 | "Corporate device may forbid installs." | Portable ZIP reduces footprint; it does not grant permission. Install needs explicit approval. |
| A3 | "58 GB free is tight." | Blender 1.5 GB + assets 1–3 GB + frames ~0.4 GB fits; a long-form library does not. External SSD likely. |
| A4 | "Eevee can't do ray-traced shadows." | True. Premium look must come from lighting discipline, not brute force. |
| A5 | "Remote is cheaper to start." | ~$0.1–1 per scene; recurring with iteration and adds upload friction. Local wins for iteration. |
| A6 | "Asset packs solve modelling." | Mostly false for payment hardware. Model hero props; CC0 environment only. |
| A7 | "WebGL is already installed." | Retained for diagrams, not the premium path. |
| A8 | "Automation before quality wastes effort." | Correct; roadmap now gates on one excellent scene. |

## 8. Recommendation

1. **Primary: Blender 5.2.3 LTS portable ZIP, Eevee, local.**
2. **Fallback: remote Blender** for heavy scenes once local limits are measured.
3. **Keep WebGL** for diagrams and layout.
4. **Model hero props**; use CC0 HDRIs/textures only.
5. **Before any production claim:** a measured single-frame Eevee background render.

## 9. Risks added

| ID | Risk | Severity |
|---|---|---|
| R15 | Eevee unstable or unusably slow on the iGPU | High — blocks local path |
| R16 | Corporate policy blocks Blender installation | High — forces remote |
| R17 | Asset licence contamination from aggregators | Medium |
| R18 | Disk pressure from Blender + assets + frames | Medium |

## 10. Open questions

1. Does background Eevee rendering initialise the iGPU correctly under this driver?
2. Actual seconds per frame at 1080×1920 / 64 samples?
3. Does corporate policy permit a portable ZIP in a project folder?
4. Is Eevee's Vulkan backend stable here, or must OpenGL be forced?

## 11. Sources

| Source | Retrieved |
|---|---|
| https://www.blender.org/download/ (5.2.3 LTS, 349 MB installer) | 2026-10-30 |
| https://www.blender.org/download/requirements/ (GPU/OpenGL/Vulkan) | 2026-10-30 |
| https://docs.blender.org/manual/en/latest/render/eevee/ | 2026-10-30 |
| https://docs.blender.org/manual/en/latest/getting_started/installing/windows.html | 2026-10-30 |
| https://polyhaven.com/license (CC0) | 2026-10-30 |
| https://ambientcg.com/license (CC0) | 2026-10-30 |
| https://kenney.nl/support (commercial use) | 2026-10-30 |
