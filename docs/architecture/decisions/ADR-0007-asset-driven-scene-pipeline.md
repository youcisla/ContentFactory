# ADR-0007 — Asset-driven scene assembly, deterministic render path

- Status: proposed
- Date: 2026-10-31
- Deciders: user (sign-off pending), agent (proposal)
- Related: ADR-0001, ADR-0002, `docs/research/open-source-projects/EVALUATION_2026-10-31.md`, `docs/creative/PREMIUM_TREATMENT_V5.md`, `docs/creative/BENCHMARK_SPEC_PREMIUM.md`

## Context

V4 answered its question: Blender 5.2.3 renders headlessly on this host, Eevee on the Intel OpenGL 4.6 path, with measured costs — 1.54 s/frame at 540×960, 8.51 s/frame at 1080×1920, 8 samples. The scene teaches the mechanism and passes its geometry and sequence gates.

It does not look premium. Every object in it was generated from primitives in one Python file: box, card, cylinder, torus. Materials are a four-value helper. The camera is a mathematical dolly. There is no depth of field, no motion blur, no texture, no imperfection, no environment map, no set dressing.

The reset brief names this as the central problem and forbids continuing to polish it. The evidence supports that reading rather than contradicting it:

- **Zack D. Films** (public contractor portfolio, 2026): Blender + Cascadeur + BlenderKit + After Effects + EmberGen, with scene, compositing and edit templates and a Flamenco render farm. Premium output comes from template reuse, asset libraries and camera/light discipline — not from bespoke modelling per shot.
- **Branch Education** (public studio case study, 2026): Blender + Premiere + After Effects + Reaper; hardware is bought, disassembled, scanned, photographed, and rebuilt until "put our model next to a photo of the real part and see no difference". 1,100+ hours per video; up to 4 animators; scenes 2–3 GB.
- Both spend their quality budget on **lens, light, imperfection and sound**, which is the part that transfers to a small team. Neither depends on an agent writing scene code.

At the same time, the ten Blender agent projects evaluated on 2026-10-31 all build scenes by executing model-written Python inside Blender, and none documents a working multi-shot timeline. Putting any of them in the render path would trade determinism for a feature nobody has demonstrated.

## Decision

**Scenes are assembled from a curated, licence-verified asset library into a `.blend` template, driven by a JSON shot specification, and rendered by fixed code. Agents may author; agents never render.**

In practice:

1. `assets/` holds only assets with a recorded `source_url`, `licence`, `retrieved_at` and `commercial_ok=true` in `assets/manifest.json`. Validation fails the build otherwise.
2. One `.blend` template per episode family carries the camera rig, the light rig, the set and the linked asset collections. Hero props that cannot be licensed (the terminal, the card) are modelled once, to reference, and reused.
3. A shot spec (JSON) names template, assets, camera, lens, focus, light preset and timing. The render driver reads it — it does not invent geometry.
4. `tools/cf_qa.py` keeps its authority: geometry gate, exposure curve, sequence verdict. New criteria (focus target, safe area, set-dressing density) are added to the same file.
5. Blender agent/MCP tooling stays out of the render path. It may be trialled as an authoring accelerator in an isolated environment after a named approval (CF-143).

## Alternatives considered

| Option | Why rejected |
|---|---|
| Continue procedural V4 and polish | The brief forbids it; every added primitive is another invention competing with reference reality |
| Put an agent/MCP in the render path | All ten candidates execute model-written Python; multi-shot timeline unproven; nondeterministic output breaks reproducibility and the QA gates |
| Buy a paid model library first | Licence and cost unknown; the free CC0 path is sufficient first, and the manifest gate keeps it honest |
| Hand-model everything to Branch Education fidelity | Correct but unaffordable: 1,100 hours per video is not a solo pipeline |
| Remote-GPU-first (ADR-0002 as the spine) | ADR-0002 stands for hero shots; making it the spine adds vendor and cost risk before quality is proven |

## Consequences

**Positive.** Quality gains land where they are cheapest — lens, light, DOF, imperfect materials, set dressing — instead of in more geometry. Assets become reusable across episodes, which is the only path to sustainable output. The render path stays deterministic and testable. Licensing becomes a build gate rather than a review habit.

**Negative.** The pipeline gains a stateful artefact (`.blend` templates) that git handles poorly; template versioning must be explicit. Asset acquisition is a new approval surface. Hand-modelled hero props still cost hours.

**Harder.** Reproducibility: a `.blend` can be edited by hand outside the script. Mitigation — templates are versioned, and a render records the template hash in `render_job.json`.

## Guardrails

1. No asset enters `assets/` without a licence row; `commercial_ok=false` fails validation.
2. No agent-generated code runs in a render or on the corporate host with network access.
3. V4 is frozen as the technical baseline; it is not deleted and not further polished.
4. Every new QA criterion must be able to fail — demonstrated with a negative control, as CF-134 did.
5. A template change that alters framing re-runs the geometry gate before any sequence render.

## Evidence

- `docs/benchmarks/BLENDER_EEVEE_RESULT.md`, `BLENDER_EEVEE_CORRECTION.md` — host capability.
- `docs/progress/LOG.md` — V4 measured costs; CF-134 negative control.
- `docs/research/open-source-projects/EVALUATION_2026-10-31.md` — candidate capability, licence and security.
- Creator pipeline facts: contractor portfolio (supersets.chrisreillyportfolio.com/zackdfilms.php), Acoroid studio case study, Branch Education AI policy. Team-size and per-day figures from fan wikis are deliberately not relied on.
- `docs/research/assets/SHORTLIST.md` — existing provenance rules, reused here unchanged.
