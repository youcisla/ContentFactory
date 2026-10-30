# 04 — Architecture and Build Plan (PLAN ONLY — nothing here is authorised to execute)

Status: proposal for approval. No installation, no benchmark, no repository clone has been performed.
Design constraint carried from `00`: corporate-managed host, CPU-only Cycles, 58 GB free disk, no agent in the publish path.

---

## 1. Architecture options (plan item 4.1)

| Criterion | **A. Deterministic Blender Python templates** | **B. Agent/MCP-driven Blender** | **C. Hybrid 3D + generative footage** |
|---|---|---|---|
| Factual accuracy | High — geometry is authored, not inferred | Medium — model decides geometry per run | Low — generative video invents detail |
| Repeatability | High — same inputs, same frames | Low — non-deterministic per session | None |
| Visual quality ceiling | Medium-high, capped by template craft | High in demos, unstable in batches | High gloss, low specificity |
| Operating cost | Lowest (CPU electricity) | Medium (many LLM turns) | Highest (per-second video pricing) |
| Security | Low risk (own code only) | **High** (arbitrary code execution) | Medium (vendor APIs, uploads) |
| Commercial rights | Clear (own assets, CC0) | Clear, but vendor ToS apply | Vendor terms + disclosure duty |
| Maintainability | Good if schemas are strict | Poor — prompts are the program | Poor — model drift |
| Verdict | **Production spine** | **Authoring accelerator only** | Optional B-roll, gated |

**Recommendation:** A as the production system; B confined to an isolated VM for scene prototyping; C excluded from the first 20 videos.

`★ Why` Reproducibility is the whole product. A video that cannot be re-rendered after a correction is a liability — especially for factual content about money and security, where an error must be fixable in one commit.

---

## 2. System decomposition

```
┌──────────────────────────────────────────────────────────────┐
│ CONTROL PLANE  (Python 3.12 venv, uv-managed, no network)    │
│  schemas → validators → job queue → ledger                   │
└───────┬──────────────────────┬───────────────────┬───────────┘
        │                      │                   │
┌───────▼────────┐   ┌─────────▼────────┐  ┌───────▼──────────┐
│ AUTHORING      │   │ RENDER           │  │ ASSEMBLY         │
│ Blender 5.2.3  │   │ CPU Cycles local │  │ FFmpeg 8.1.1     │
│ templates/*.py │   │ or cloud GPU     │  │ concat + subs    │
│ (MCP in VM     │   │ PNG/EXR frames   │  │ + loudness norm  │
│  optional)     │   │ → MP4 per scene  │  │ → final MP4      │
└───────┬────────┘   └─────────┬────────┘  └───────┬──────────┘
        │                      │                   │
┌───────▼──────────────────────▼───────────────────▼───────────┐
│ AUDIO PLANE: licensed TTS → forced alignment → SRT/VTT        │
├──────────────────────────────────────────────────────────────┤
│ REVIEW PLANE: G1 claims · G2 script · G3 board · G4 render ·  │
│               G5 publish  (all human, all logged)             │
├──────────────────────────────────────────────────────────────┤
│ PUBLISH PLANE: YouTube Data API (or manual first) + Analytics │
└──────────────────────────────────────────────────────────────┘
```

### Plane responsibilities

| Plane | Owns | Must never |
|---|---|---|
| Control | schemas, validation, queue state, cost ledger | touch Blender or the network |
| Authoring | `.blend` generation from JSON, camera rigs, materials | read credentials |
| Render | deterministic frame output, telemetry capture | write outside its job directory |
| Audio | TTS calls, alignment, caption files | improvise script text |
| Assembly | muxing, normalisation, chapter/caption embedding | apply creative edits not in the storyboard |
| Review | human decisions, sign-off records | be bypassable by a flag |
| Publish | upload, metadata, disclosure flag, analytics pull | run unattended before G5 exists |

---

## 3. Data contracts (plan item 4.2)

All artefacts are JSON, validated on write and on read. `schema_version` is mandatory and semver. Unknown keys are rejected (`additionalProperties: false`) so that silent drift fails loudly.

### `episode.json`
```json
{
  "schema_version": "1.0.0",
  "episode_id": "money-credit-card-001",
  "topic": "How a credit card payment actually moves",
  "audience": "adults, no finance background",
  "outputs": ["9x16_40s", "16x9_480s"],
  "claims_ref": "claims.json",
  "storyboards": { "9x16": "storyboard_9x16.json", "16x9": "storyboard_16x9.json" },
  "disclosure": { "genai_realistic": false, "reason": "all geometry is authored; no synthetic likeness" }
}
```

### `claims.json`
```json
{
  "schema_version": "1.0.0",
  "claims": [{
    "claim_id": "C-014",
    "text": "The issuer's interchange fee is typically a small percentage of the transaction.",
    "sources": [{ "url": "...", "retrieved_at": "2026-10-30", "quote": "...", "sha256": "..." }],
    "confidence": "high",
    "verified_by_human": true,
    "verified_at": "2026-10-30"
  }]
}
```
Rule: a claim without `verified_by_human: true` **cannot** appear in narration. The renderer refuses to build a scene that references an unverified claim.

### `storyboard_<ratio>.json`
```json
{
  "schema_version": "1.0.0",
  "ratio": "9x16",
  "resolution": [1080, 1920],
  "fps": 30,
  "scenes": [{
    "scene_id": "S03",
    "duration_s": 4.5,
    "template": "concept_reveal",
    "params": { "title": "Authorisation", "accent": "#3B82F6" },
    "claims": ["C-014"],
    "camera": { "type": "ortho", "fit": "vertical" },
    "safe_area": { "top_pct": 12, "bottom_pct": 18 }
  }]
}
```

### Remaining contracts (field lists, same strictness)

| File | Required fields |
|---|---|
| `assets.json` | `asset_id, path, sha256, source_url, licence_spdx, licence_evidence_sha256, retrieved_at, commercial_ok (bool)` |
| `narration.json` | `scene_id, text, tts_provider, voice_id, chars, audio_path, duration_s, alignment_path` |
| `render_job.json` | `job_id, scene_id, template_version, blender_version, engine ("CYCLES"), samples, seed, resolution, frames, idempotency_key` |
| `qa.json` | `scene_id, frame_range_checked, legibility_pass, continuity_pass, factual_pass, reviewer, signed_at` |
| `publish.json` | `video_path, title, description, tags, chapters[], captions_path, disclosure_flag, thumbnail_path, approved_by, approved_at` |

`idempotency_key = sha256(template_version + canonical(params) + sorted(asset_sha256) + render_settings)`. Re-running a job with the same key must return the cached output, never re-render.

---

## 4. One source → two formats (plan item 4.3)

Never crop. The 16:9 master and the 9:16 short are **separate storyboards** produced from the same claims file.

| Concern | 16:9 long-form | 9:16 short |
|---|---|---|
| Resolution | 1920×1080 @ 30 fps | 1080×1920 @ 30 fps |
| Camera fit | `sensor_fit = HORIZONTAL` | `sensor_fit = VERTICAL` |
| Composition | wide establishing shots allowed | centre-weighted; subject within middle 60 % |
| Text | ≥ 28 px at 1080p | ≥ 42 px; max 6 words per card |
| Safe area | 5 % all sides | top 12 %, bottom 18 % (UI chrome) |
| Duration | 8 min target | 40 s target, one idea |
| Scene count | 35–60 | 6–9 |

Shorts are *not* trailers. Each short must be self-contained: hook, one claim, one visual metaphor, payoff.

---

## 5. Provenance and reproducibility (plan item 4.4)

1. Every asset row carries source URL, licence, evidence hash, retrieval date, and a `commercial_ok` boolean. Assets with `commercial_ok = false` fail validation.
2. Every render records `blender_version`, `template_version`, `seed`, sample count, and device (`CPU`).
3. Template code lives in git; a render is reproducible from `(commit, episode.json, assets.json)`.
4. Cache key is content-addressed; deleting the cache is always safe.
5. No model-generated code is stored as a template. If an LLM helps author a scene, its output is reviewed and committed as ordinary code.

---

## 6. Queue, idempotency, recovery (plan item 4.5)

| Concern | Design |
|---|---|
| Queue | SQLite table `jobs(id, key, state, attempts, started_at, finished_at, error)` |
| States | `queued → running → done | failed | blocked` |
| Retry | max 2, exponential backoff, only on transient errors (OOM excluded) |
| Timeout | per scene: 3× the benchmarked median, hard-killed |
| Checkpoint | per-scene output; resuming skips scenes whose key hash exists |
| Disk guard | refuse to start a job if free space < 15 GB; abort mid-job below 8 GB |
| Failure isolation | a failed scene blocks its episode, never the queue |
| Audit | every state transition appended to `ledger.jsonl` with timestamp and actor |

---

## 7. Deployment options (plan item 4.6)

| Option | Hardware | Monthly cost (est.) | Fit |
|---|---|---|---|
| Local-only CPU | this laptop | €0 variable | Prototypes; 1–2 shorts/month |
| Local authoring + cloud render | laptop + rented GPU | $10–40 | **Recommended** at 4+ videos/month |
| Cloud-first | rented CPU/GPU VM | $40–120 | Only if local policy blocks installs |
| Personal machine purchase | RTX-class laptop/desktop | capex €1,200–2,000 | Best long-term if channel earns |

All cloud figures are estimates; verify against current provider pricing before committing.

---

## 8. Human approval gates (plan item 4.7)

| Gate | Question | Who | Blocking |
|---|---|---|---|
| G1 | Is every claim sourced and true? | user | yes — narration refuses unverified claims |
| G2 | Is the script accurate, clear, non-misleading? | user | yes |
| G3 | Does the storyboard teach the claim visually? | user | yes |
| G4 | Render QA: legibility, continuity, artefacts | user | yes |
| G5 | Publish: metadata, disclosure, thumbnail | user | yes |

No gate may be auto-approved. G1–G5 records are written to `reviews/<episode_id>.json` with timestamps.

---

## 9. Isolation (plan item 4.8)

| Layer | Control |
|---|---|
| Blender worker | dedicated low-privilege Windows user **or** WSL2 container; no domain credentials |
| Network | render jobs run with no network requirement; asset fetch is a separate, audited step |
| Filesystem | read-only asset mount; write access limited to the job directory |
| MCP | only inside an isolated VM with no host mounts; never against the production Blender install |
| Secrets | API keys live in a separate user context, never exported into Blender's environment |
| Egress | TTS/LLM calls originate from the control plane, not the render worker |

The official Blender Lab warning is treated as a hard requirement, not a suggestion.

---

## 10. Publishing and analytics (plan items 2.6, 4.9)

- **Quota reality:** `videos.insert` has its own bucket of **100 uploads/day**; other endpoints share 10,000 units/day. Upload volume is not the constraint — review capacity is.
- **First 10 videos:** manual upload. This removes OAuth scope risk while the format is still changing.
- **Disclosure:** YouTube requires disclosure of realistic AI-generated or altered content. `publish.json.disclosure_flag` must be set explicitly at G5; default is "not disclosed" only when the episode contains no realistic synthetic depiction.
- **Analytics:** pull views, average view duration, retention curve, CTR. Tag experiments in the description and in a local ledger — YouTube itself has no UTM concept.
- **Cost per approved minute** is the north-star metric: `(variable cost + human hours × rate) / approved minutes`.

---

## 11. Cost model (plan item 2.8 / prompt item 6)

Every figure below is an **estimate with stated assumptions**, not a quote. Rendering time is unmeasured because no benchmark was authorised.

### Assumptions
| Assumption | Value | Confidence |
|---|---|---|
| Short length | 40 s, ~95 words, ~600 TTS characters | design target |
| Long-form length | 8 min, ~1,150 words, ~7,300 TTS characters | design target |
| Licensed TTS | $15–16 per 1M characters | medium — vendor page is JS-rendered, figure is list price |
| LLM (script/claims/storyboard) | ~30k in / 6k out per short; ~120k in / 20k out per long | low — depends on iteration count |
| LLM price (DeepSeek-class) | ~$0.15–0.30 / 1M in, ~$0.60–1.20 / 1M out | medium — extracted from pricing page, formatting lossy |
| Local CPU render | 0.3–2 h short; 3–10 h long | **low — unmeasured** |
| Cloud GPU | $0.30–0.70 / h | medium |
| Electricity | ~€0.25 / kWh, ~60 W avg | estimate |
| Human review | €25 / h opportunity cost | user-supplied assumption |

### Per-output estimate
| Line | 40 s Short | 8 min long-form |
|---|---:|---:|
| TTS (licensed) | $0.01 | $0.12 |
| LLM calls | $0.02 | $0.06 |
| Local render (electricity) | €0.01–0.03 | €0.05–0.15 |
| Cloud render alternative | $0.15–0.70 | $1.00–4.00 |
| Storage / egress | <$0.01 | <$0.05 |
| **Variable total** | **$0.05–0.75** | **$0.25–4.30** |
| Human review | 0.5–1 h → €12–25 | 3–6 h → €75–150 |
| **True cost** | **€12–26** | **€75–155** |

### Sensitivity
| Scenario | Effect |
|---|---|
| Render time 2× estimate | +€0.05 short; +€0.15 long (local) — human time dominates |
| Premium TTS (ElevenLabs-class) | TTS rises ~5–15× → still <€3 per long-form |
| Cloud GPU 2× price | +$1–4 per long-form |
| Human review doubles | **doubles total cost** |
| Subscription creep (stock, music, plugins) | €20–60/month fixed, independent of output |

`★ Conclusion` Variable compute is noise. **Human review is the cost centre.** Any automation that does not reduce review minutes is a hobby, not a business.

---

## 12. Top 10 failure modes (plan item 7.3)

| # | Failure | Prob. | Impact | Mitigation | Trigger to act |
|---|---|---|---|---|---|
| 1 | Corporate policy forbids installs/use | Med | Fatal | Resolve in writing before Phase A | Policy answer = no |
| 2 | Local render too slow to iterate | High | High | Cloud GPU fallback; low-poly visual language | 10 s test > 10 min |
| 3 | Disk exhaustion during render | Med | High | Disk guard; per-episode purge; external drive | <15 GB free |
| 4 | Factual error ships | Med | High | G1 gate; claims registry; corrections workflow | any post-publish correction |
| 5 | Agent-generated code damages files | Low | High | No MCP on host; VM only; no credentials | any MCP use request |
| 6 | TTS rights challenge | Low | High | Licensed provider only | any monetisation review |
| 7 | Asset licence contamination | Med | High | `commercial_ok` field; evidence hash | asset with unknown licence |
| 8 | Visual quality below audience threshold | High | Medium | Template craft; benchmark at 10 s; feedback loop | retention < 40 % |
| 9 | Schema drift breaks rerender | Med | Medium | Strict validation; pinned versions; git | validation error |
| 10 | Human bottleneck caps output | High | Medium | Templates that reduce review minutes; checklist QA | >60 min review per minute |

---

## 13. Benchmark suite — DESIGNED, NOT AUTHORISED (plan Phase 5)

Nothing in this section may run without a separate explicit approval.

### B1 — 10-second capability probe
| Field | Value |
|---|---|
| Scene | one sphere, one plane, one area light, one HDRI, one glass material |
| Engine | Cycles, CPU, 64 samples, denoise on |
| Output | 1920×1080, 240 frames @ 24 fps → MP4 |
| Telemetry | wall clock, peak working set, per-frame time, free disk delta |
| Pass | completes < 10 min; peak RAM < 20 GB; no thermal shutdown |
| Stop | > 30 min, RAM > 28 GB, free disk < 8 GB, BSOD/thermal event |

### B2 — 40 s 9:16 pilot
| Field | Value |
|---|---|
| Content | "how a card payment is authorised", 6 scenes, authored templates |
| Pass | total render < 90 min; captions aligned within ±80 ms; legibility at 360 px width; script fact-checked |
| Stop | any render failure twice, or 2× the time budget |

### B3 — 90 s 16:9 technical scene
| Field | Value |
|---|---|
| Content | reused assets, camera move, one diagram overlay |
| Pass | < 3 h; no frame with broken geometry; audio loudness −14 LUFS |
| Stop | as B2 |

### Measured criteria (plan item 5.5)
Wall-clock time · peak RAM · peak VRAM (n/a on iGPU) · frames/hour · failure count · human correction minutes · file size · repeatability (two runs, identical frame hashes on a static frame).

`shortcut: EEVEE-on-iGPU is excluded from the benchmark, add it back only if Cycles CPU proves too slow.`

---

## 14. Roadmap (plan Phase 6) — all tasks blocked until Q1 in `06` is answered

| Stage | Tasks | Depends on | Effort (est.) | Acceptance | Rollback |
|---|---|---|---|---|---|
| **A0** | Resolve host policy; choose personal vs managed vs cloud | — | 1 conversation | written answer | none needed |
| **A** | Install Blender portable, uv-managed Python 3.12 venv, FFmpeg confirm, isolated worker user | A0 | 2–4 h | `blender --version` on 5.2.3; venv imports validate schemas | uninstall portable dir; venv is disposable |
| **B** | Schemas + validators + claims registry + ledger | A | 6–10 h | invalid episode rejected with a specific error; claim gate blocks narration | delete `control/`; no external state |
| **C** | 5 Blender templates (concept reveal, flow, comparison, number, warning) | B | 20–30 h | each renders 9:16 and 16:9 deterministically from JSON | git revert per template |
| **D** | TTS + alignment + SRT/VTT + loudness normalisation | B | 8–12 h | caption drift < 80 ms on a 60 s sample | swap provider; captions regenerate from audio |
| **E** | Review gates G1–G5 + provenance UI (files first, UI later) | B | 6–10 h | no path to publish without G5 record | gates are files; revert to manual |
| **F** | 1 short + 1 long pilot, end to end | C, D, E | 15–25 h | accuracy, legibility, budget within `05` targets | discard episode; templates unaffected |
| **G** | 12 shorts + 4 long over 60 days | F | ongoing | instrumented results; cost per approved minute tracked | stop publishing; archive ledger |

Effort ranges are estimates for one experienced operator plus an agent; no measured velocity exists for this stack.

---

## 15. Rollback strategy (cross-cutting)

1. **Everything is a file.** Templates, schemas, assets manifest, ledger — all in git or plain JSON. No database, no external state.
2. **Portable Blender.** Installing to a folder under the project (or an external drive) makes removal a directory delete and avoids touching a managed system.
3. **Pinned versions.** `blender==5.2.3`, `ffmpeg==8.1.1`, Python 3.12 with a lockfile. Upgrades are a deliberate, git-committed event.
4. **No destructive automation.** Nothing deletes source assets; caches are content-addressed and safe to purge.
5. **Publish gate.** Until G5 is proven over 10 videos, publishing stays manual.
