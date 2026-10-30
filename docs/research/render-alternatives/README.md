# Render Alternatives — free and cheaper than local

Task: find options better than 42.64 s/frame local Eevee. Research via agent-reach (Exa, GitHub). Read-only; nothing installed or purchased.
As of: 2026-10-30.

---

## 1. The cost of the current setup

Local Eevee: **42.64 s/frame** → 240 frames (10 s @ 24 fps) ≈ **170 minutes** per pass. Cost €0, time prohibitive.

## 2. Free options

| Option | What you get | Eevee? | Catch | Status |
|---|---|---|---|---|
| **SheepIt** | Free distributed Blender render farm, 473 machines active | **Yes — Cycles, Eevee, Workbench now supported** | Your `.blend` renders on strangers' machines; queue waits; no SLA | [U] homepage, 2026-10-30 |
| **Lightning AI free** | ~80 GPU-hours/month via 15 credits (T4/L4/L40S/A100/H100) | Yes, if Blender runs in the Studio | 4-hour session restarts; setup effort | [U] free-GPU database, 2026-10 |
| **Modal Starter** | **$30/month free compute**, serverless | Yes, containerised Blender | Code-first, not a notebook; setup effort | [U] gpuperhour, 2026-09-21 |
| **Google Colab free** | T4-class, 12-hour sessions, no published quota | Possible via xvfb/GL workarounds | Fragile; idle disconnect; GPU type not guaranteed | [U] Colab FAQ |
| **Kaggle** | T4/P100, 12-hour sessions, ~30 GPU-h/week reported | Possible, same caveats | Quota floats; not in docs | [U] Kaggle docs |
| **Hugging Face ZeroGPU** | 5 min GPU/day, Gradio Spaces only | No practical path | 60-second function cap | [U] |

## 3. Paid options (cheapest verified)

| Provider | RTX 4090 / h | Notes |
|---|---:|---|
| **RunPod Community** | **$0.34** | Lowest list price; vetted independent hosts |
| TensorDock | $0.35 | $5 minimum deposit; prices partly unverified |
| **Vast.ai** lowest verified | **$0.41** | Marketplace; median $0.67; prices move daily |
| RunPod Secure | $0.89 | Tier 3/4 data centres |
| Lambda / Hyperstack | $1.35–3.29 (A100/H100) | Overkill for Eevee |

Sources: adtestbench.com cloud GPU price table (2026-10-24), askgpu.com comparison (2026-10-25), Vast.ai public offers.

## 4. Cost per 10-second scene

Assumption: Eevee on a 4090 at 1080×1920 / 64 samples renders **0.5–2 s/frame** (estimate; unmeasured).

| Rate | 240 frames at 1 s/frame | at 2 s/frame |
|---|---:|---:|
| $0.34/h (RunPod) | **$0.02** | **$0.05** |
| $0.41/h (Vast lowest) | $0.03 | $0.05 |
| $0.67/h (Vast median) | $0.04 | $0.09 |

Even at a pessimistic 10 s/frame (40 min), a 10 s scene costs **$0.23–0.45**. Rendering is not the budget problem; iteration friction and setup are.

## 5. Local optimisations (no cost)

| Change | Expected effect |
|---|---|
| TAA 64 → 16 samples | ~2–4× faster |
| 1080×1920 → 540×960 + upscale | ~3–4× faster |
| Workbench for previz | near real-time, no materials |
| Disable motion blur/DOF during look-dev | faster iteration |
| 16 samples + half-res combined | ~8–12× → ~4–5 s/frame, still 20+ min per 10 s |

Local remains viable for stills and blocked-out motion, not final animation.

## 6. Recommendation

1. **Primary: RunPod Community 4090 or Vast.ai 4090** — $0.34–0.41/h, ~$0.02–0.10 per 10 s scene.
2. **Free fallback: SheepIt** for test/non-sensitive scenes. Eevee support changes the earlier assumption that free farms were Cycles-only.
3. **Modal $30/month credit** worth evaluating if serverless automation becomes the goal.
4. **Lightning AI** best free interactive option for a persistent GPU desktop.
5. **Local:** previews, stills, composition. Not final animation.

## 7. Security and licence notes

| Risk | Detail | Mitigation |
|---|---|---|
| **SheepIt IP exposure** | `.blend` is downloaded and rendered by anonymous volunteers | Public test scenes only; never send unreleased client work or credentials |
| Cloud provider data | Scene and textures uploaded to a rented host | No secrets in `.blend`; wipe instance after use |
| Licence | Blender GPL; farm rendering does not change output ownership | — |
| Free-tier terms | Colab/Kaggle forbid remote desktop/SSH on free tier; Modal bills past credit | Read terms before automating |

## 8. What changes in the plan

- Remote rendering is **cheap enough to be routine**: under $0.10 per 10-second scene.
- **SheepIt is back on the table** for free Eevee tests, with the IP caveat.
- The blocker is no longer cost; it is scene quality and setup time.

## 9. Sources

| Source | Retrieved |
|---|---|
| https://www.sheepit-renderfarm.com/home (Eevee/Cycles/Workbench, 473 machines) | 2026-10-30 |
| https://adtestbench.com/data/cloud-gpu-prices/ | 2026-10-30 |
| https://askgpu.com/cheapest-cloud-gpu/ | 2026-10-30 |
| https://gpuperhour.com/blog/free-cloud-gpus-and-credits | 2026-10-30 |
| https://github.com/drmichaeldouglass/blenderGoogleGPU | 2026-10-30 |
| https://github.com/francescoopiccolo/free-gpu | 2026-10-30 |
