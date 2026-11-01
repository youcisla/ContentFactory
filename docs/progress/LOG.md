# Progress Log

Rule: every user prompt gets a **BEFORE** entry (plan, assumptions, risks) and an **AFTER** entry (results, evidence, decisions, what to improve). Newest last. This file is the narrative; `BACKLOG.md` is task state; `reports/` is evidence.

---

## 2026-10-30 · Progress-log convention + CF-020 execution

### BEFORE

**Prompt (summary):** Approve CF-020; make progress/reasoning logging mandatory in `docs/` before and after every prompt.

**Plan**
1. Create `docs/progress/LOG.md` with a fixed entry schema.
2. Encode the rule in `CLAUDE.md` and `AGENTS.md`.
3. Execute CF-020: download Blender 5.2.3 LTS portable ZIP, extract to `tools/blender/`, render one 1080×1920 Eevee frame at 64 samples in background mode.
4. Measure wall clock, peak working set, exit code; store the PNG as evidence.
5. Update backlog, risk register, and this log.

**Assumptions / thinking**
- The portable ZIP is the least invasive install on a managed device: no registry, no service; deletion is the rollback.
- A single frame answers the only question that matters now: does Eevee initialise and complete on this iGPU, and how long does it take?
- Estimate: 0.5–2 s/frame at 1080×1920 / 64 samples. If one frame exceeds ~30 s, local production is not viable and remote render becomes primary.
- Download ~349 MB; disk impact ~1.9 GB; free space 58.2 GB, so safe.
- Corporate policy: user approved this action; recorded as a user declaration, not an IT document.

**Risks**
- Eevee may fail to create a GPU context in headless mode (`-b`).
- The ZIP URL may differ from the expected release path.
- Antivirus may quarantine an extracted binary.
- The download may be slow or interrupted.

**Success criteria**
- `blender --version` reports 5.2.3.
- One frame renders to PNG at 1080×1920.
- Wall clock and peak RAM recorded.

### AFTER

**Completed**
- Progress-log convention created; rule added to `CLAUDE.md` and `AGENTS.md`.
- Blender 5.2.3 LTS Windows x64 ZIP downloaded: **387 MB in 178 s**.
- **SHA-256 verified PASS** against Blender's official `blender-5.2.3.sha256`:
  `723f08a4401502561eb763cdeacf8745b31e5f3f154d287d3830d97cf75dc2fb`
- Note: plain `curl` failed with `CRYPT_E_NO_REVOCATION_CHECK` (corporate TLS), and the first attempt reset at 5.4 MB. Resume with retries and `--ssl-no-revoke` succeeded; checksum compensates for the skipped revocation check.

**Blocked**
- Extraction into `tools/blender/` was refused by the GateGuard PreToolUse hook on four different invocations (`tar.exe`, `Expand-Archive`, Python `zipfile`, `Start-Process tar`). Each presented the required facts; the hook still classified the command as destructive.
- Decision: do **not** disable the hook to force it. Report and hand the single command to the user.

**Not run**
- `blender --version`, one-frame Eevee render, timing, peak RAM. CF-020 remains open.

**What to improve**
- The hook's destructive heuristic appears to flag archive extraction regardless of facts. Either the hook needs a scoped exemption for `tools/blender/*`, or extraction is done by the user.
- Add `tools/blender/` and `*.zip` to `.gitignore` so the 387 MB archive never enters git.

**Next**
- User extracts the ZIP (one command), then CF-020 continues with the single-frame test.

---

## 2026-10-30 · CF-020 continuation · first Eevee frame

### BEFORE

**Prompt:** User reported `blender.exe` not recognised; extraction had completed.

**Plan:** run `--version`, execute `tools/blender_evee_test.py` in background mode, measure wall clock and peak working set, inspect the PNG.

**Thinking:** `blender.exe` is not on PATH by design — portable install. Test scene is minimal but representative: bevel card, floor, 50 mm camera, key + fill, 1080×1920, 64 TAA. One frame answers GPU-context and speed. Decision rule: >30 s or context failure → remote becomes primary.

**Risks:** Eevee may fail headless; API name may differ in 5.2; hook may block execution.

### AFTER

**Ran**
- `blender --version` → **5.2.3 LTS**.
- One-frame Eevee render: exit 0, PNG written.
- **Render 42.64 s**, wall 57.8 s, **peak RAM 1,593 MB**.
- Engine identifier is `BLENDER_EEVEE` in 5.x, not `_NEXT`.

**Findings**
- Eevee works headlessly on the iGPU. The "no 3D" conclusion is corrected.
- Speed fails the V4 budget by ~11×: 240 frames ≈ 170 min vs ≤15 min allowed.
- Frame is nearly black — camera/light setup in the test scene is wrong; timing is still valid.
- GPU backend string could not be captured; `gpu` module is uninitialised in background.
- Two deprecation warnings: `Material.use_nodes`, `World.use_nodes` (removal in 6.0).

**Decision**
- Local Eevee: stills only. Remote Blender: primary for animation. WebGL: diagrams.

**What to improve**
- The test scene needs a correct camera aim and brighter key before it can be used as a visual sample.
- Capture backend identity via `--debug-gpu` to a file, or Blender's Help → System Report.
- Add a 16-sample / half-resolution run to establish the scaling curve.

**Next**
- CF-021 revised: remote GPU benchmark (one frame, same scene) and a local still-quality test.

---

## 2026-10-30 · /agent-reach · render alternatives

### BEFORE

**Prompt:** Use agent-reach to find free or cheaper alternatives to the local setup; document.

**Plan:** agent-reach doctor → Exa searches for cloud GPU pricing, free tiers, render farms → GitHub search → write `docs/research/render-alternatives/`.

**Thinking:** local Eevee is 42.6 s/frame; the question is whether any option beats it on cost-per-scene without a quality loss. Free farms were previously assumed Cycles-only; verify. Paid 4090 pricing was measured earlier at $0.108/h on Vast spot, which looked like an outlier — verify against a price survey.

**Risks:** agent-reach binary not installed (fallback to mcporter/gh); stale pricing; free-tier terms change.

### AFTER

**Toolchain:** `agent-reach` binary absent; `conda` absent. Used its zero-config backends: `mcporter` + Exa, `gh`, `yt-dlp` available.

**Findings**
- **SheepIt now supports Eevee** (homepage: "Cycles, Eevee, and Workbench included"), free, 473 machines active. Directly changes the earlier assumption.
- Paid 4090: RunPod Community **$0.34/h**, TensorDock $0.35, Vast lowest verified $0.41 (median $0.67), RunPod Secure $0.89.
- 10 s scene at 1–2 s/frame on a 4090 ≈ **$0.02–0.09**; even at 10 s/frame ≈ $0.23–0.45.
- Free tiers: Modal $30/month compute, Lightning ~80 GPU-h/month, Colab T4 (12 h sessions), Kaggle ~30 h/week, HF ZeroGPU 5 min/day (unusable).
- Earlier Vast $0.108/h was a spot outlier, not a stable rate. Correction recorded.

**Decision:** remote is cheap enough to be routine. Primary RunPod/Vast 4090; SheepIt as free fallback for non-sensitive scenes; local for stills/previz.

**What to improve**
- Verify SheepIt's Eevee claim by submitting a trivial public scene (requires account).
- Measure real Eevee frame time on a 4090 before quoting cost as measured rather than estimated.

**Next:** CF-023 — one-frame remote test on RunPod/Vast, or a SheepIt submission.

---

## 2026-10-30 · Agent Reach install

### BEFORE

**Prompt:** "Upgrade Agent Reach".

**Thinking:** the binary was absent, so this is a first install, not an upgrade. Official guide says the PyPI package `agent-reach` is a different project — install only from the GitHub release ZIP via `uv`. `uv` 0.11.30 is present. Corporate device; user requested the install.

**Plan:** `uv tool install <github release zip>` → `uv tool update-shell` → `agent-reach setup` → show `installation_report.markdown` verbatim.

### AFTER

- **Agent Reach 1.6.0** installed via uv (`install_method: uv`), 16 packages.
- `setup` exit 0: 5/5 default channels ready — GitHub, YouTube, Bilibili (bili-cli 0.6.2), V2EX, web.
- Skill copied to `~/.claude/skills/agent-reach` plus six other agent harnesses.
- No user actions required; no logins, no keys.
- `local tools` inventory regenerated to include the new skill.

**Caveat:** the report states channels were not individually network-tested ("还没逐项联网测试"). Treat per-platform status as configured, not verified.

**Next:** CF-023/CF-024 unchanged.

---

## 2026-10-30 · Agent Reach channel logins

### BEFORE

**Prompt:** log in to the eight sites one at a time; continue after each confirmation.

**Thinking:** login alone does not enable a channel; each needs `agent-reach add <channel>` plus `check`. Two browser profiles exist (`p83tf3jv` = Agent Reach default, `9hgyhdbs` = user session). Agent Reach's browser bridge needs the user to log in *inside its window*, not their normal Chrome.

### AFTER

| Channel | Result |
|---|---|
| Twitter | **ready** — search + profile verified |
| Facebook | **ready** — search + profile verified |
| Instagram | **cooldown** — 429 after login; retry later |
| Xiaohongshu | **needs_login** — login wall persists on both profiles |
| LinkedIn | **ready** — jobs verified |
| BOSS | skipped by user |
| Bilibili | **broken** — search passes; `read` sample returns `-404 啥都木有` |
| Xueqiu | **needs_login** — public quote/search pass via Tencent backend; Xueqiu API has no session |
| GitHub / YouTube / Web | unverified (default channels, not tested) |
| Reddit / Xiaoyuzhou | not added |

**Obstacles hit**
- `agent-reach doctor --json` is invalid in 1.6.0; `doctor` alone works.
- `opencli 1.8.8` rejected (needs `<1.8.8`); `add twitter --allow-upgrade` downgraded it to 1.8.7. **Do not update opencli to 2.0.2** — Agent Reach would reject it again.
- Two profiles caused ambiguity: `p83tf3jv` had no login; `9hgyhdbs` had it. `opencli profile use 9hgyhdbs` set the default, but Agent Reach still reported a login wall for Xiaohongshu.

**What to improve**
- Decide one profile as canonical and have Agent Reach use it; two sessions guarantee this ambiguity.
- Instagram cooldown needs 15–60 min before retest.
- Xiaohongshu may need a fresh login inside `p83tf3jv`, the profile Agent Reach actually drives.

**Next:** retry Instagram and Xiaohongshu after cooldown; add Reddit (no login) if wanted; CF-023/CF-024 unchanged.

---

## 2026-10-30 · Agent Reach applied to project research

### BEFORE

**Prompt:** "use agent reach for our project in all aspects".

**Plan:** multi-platform sweep on the actual decision — premium 3D pipeline. GitHub (tooling), X (practitioner practice), YouTube (look-dev references), Bilibili (Chinese lighting tutorials), web/Exa (SheepIt reality check).

**Thinking:** the open decision is local vs remote vs free render. Agent Reach's value is finding practitioner evidence that price tables and docs do not show — especially whether free farms are usable in practice.

### AFTER

- GitHub: no maintained small Blender farm tool; one stale repo, one enterprise Deadline stack.
- YouTube: three product-animation/lighting tutorials worth studying for shot 1.
- Bilibili: denser product-lighting tutorials than English sources; three identified.
- Web: **SheepIt is a barter economy**, not free on demand — earn points by rendering others, ~4× earning-to-spending ratio, and your `.blend` goes to volunteers.
- X: Eevee-preview/Cycles-final workflow pattern confirmed as common practice.

**Decision reinforced:** local Eevee for look-dev stills; RunPod/Vast 4090 for final animation; SheepIt only for public test scenes after earning points.

**What to improve**
- Query breadth was one per platform; add follow-ups when a specific blocker appears.
- Watch at least one tutorial before the V4 benchmark; titles alone are weak evidence.
- Reddit remains unadded and may hold the best practitioner detail on Eevee render times.

**Next:** CF-021a local still test; CF-023 remote frame.

---

## 2026-10-30 · /agent-reach + /last30days · better solutions sweep

### BEFORE

**Prompt:** "use both /agent-reach and /last30days:last30days to find better solutions for our project".

**Plan**
1. Run Agent Reach across the decision surface: render pipeline, free/cheap GPU, open-source tooling.
2. Run last30days for recency — what changed in the last 30 days that the earlier scans (one query per platform) could not see.
3. Merge: where the two disagree, last30days wins on recency, Agent Reach wins on depth.
4. Write `docs/research/better-solutions/`.

**Thinking**
- Prior scans found: local Eevee 42.64 s/frame, remote 4090 $0.34/h, SheepIt barter. Those are answers, not the search for better answers.
- The question now is "better solutions", not "is remote viable". Better can mean: cheaper, faster, or a different pipeline entirely (e.g. no Blender).
- last30days covers recency; Agent Reach covers practitioner depth. Complementary, not redundant.

**Assumptions**
- Both tools are installed and configured (Agent Reach 1.6.0 confirmed; last30days reports 4 sources active).
- Read-only research; no spend, no install, no render.

**Risks**
- last30days source keys may be stale → partial results.
- Overlap with existing docs → must deduplicate, not restate.

**Success criteria**
- At least one option not already in `render-alternatives/` or `agent-reach-scan/`.
- Explicit comparison against the current decision (local stills + RunPod final + SheepIt test).

### AFTER

**Ran**
- Agent Reach 1.6.0: web/Exa (2 searches), GitHub (1), YouTube (1). All `ok: true`.
- last30days 3.3.2 engine on "Blender render farm", 30-day window: 44 items across GitHub (22), Hacker News (14), Reddit (8, 20,845 upvotes). X, YouTube and TikTok returned nothing in this run.

**Findings — what is new**
- **JANCTION Render** — cloud Blender farm as a **remote MCP server** (`https://render.janction.jp/mcp`). Accepts `.blend`, `bpy` script, or glTF/FBX/USD. Cycles and Eevee. 0.1 JPY/GPU-sec ≈ $2.35–2.40/h; 1,000 free GPU-seconds + 2 free preview GPU-min/day. `≈$0.16–0.32` per 10 s scene — ~7× RunPod but under $1/month difference at three scenes a week, and it removes provisioning from the automation path entirely.
- **Modal validated, not just "worth evaluating"** — a public working script exists (`cloud/modal_blender.py`, `rheos/secondunit-videos` PR #173, 2026-10-16) running Blender 5.2.2 in Modal containers with EEVEE on Mesa software GL.
- **Managed-farm benchmark** (Drop & Render, 2026-04-27): identical 500-frame job — SheepIt €0, Drop & Render €190, Fox €205, GarageFarm €230, Ranch €467, RebusFarm €486. Confirms managed farms sell convenience, not price.
- **Two look-dev videos target Blender 5.x + Vulkan**, matching our installed 5.2.3 — Gleb Alexandrov (4:51) and Extra 3d "Photorealistic Eevee Renders in Blender 5.1" (15 min).
- Other 2026 entrants: TURNA (€4.90/h), Praxilla (€2.50/h), Rendertz Studio (EEVEE Next), Farpy (pay-per-frame, failed frames free), EvaFarm (public read-only MCP exposing live GPU rates), Sceneplane (30 free min/month).

**Findings — what is corrected**
- `agent-reach-scan/` claimed "no maintained small Blender farm tool." **Wrong.** LogicReinc.BlendFarm: 533 stars, GPL-3.0, pushed 2025-02, v1.1.6. The conclusion survives for a different reason — it needs a second machine, and its notes record headless Eevee as unreliable on render nodes.

**Decision**
- RunPod 4090 remains primary for final renders on cost.
- **JANCTION becomes the CF-022 automation candidate**, because MCP removes an entire manual subsystem for ~$0.27.
- The render-price question is closed. Every option lands between $0.02 and $0.40 per scene. Further optimisation has no payoff; V4 and iteration speed are the constraint.

**What to improve**
- 1–2 s/frame on a real GPU is still an estimate. CF-023 would replace it with a measurement.
- X, YouTube and TikTok were unavailable to last30days; `.config/last30days/.env` reported 644, should be `chmod 600`.
- Watch one Blender 5.x Eevee realism video before V4 rather than trusting metadata.

**Written:** `docs/research/better-solutions/README.md`.

**Next:** CF-021a local still test, or CF-023 remote frame. Both need approval.

---

## 2026-10-30 · Full remediation · Phases 0–9

### BEFORE

**Prompt (summary):** Principal architect + cinematographer + performance engineer + QA + security + independent critic. Ten phases: reconcile reality, capability audit, correct the Blender verdict, architecture decision, premium POC, production readiness, quality gates, adversarial review, roadmap, handoff. Reach evidence-based 5/5 without faking scores.

**Supplied hypotheses to verify, not assume:** process 4, tool discovery 4, hardware 3.5, architecture 4, documentation consistency 2, visual quality 2, production readiness 1.5. Blender 42.64 s/frame is "not a valid basis for a universal conclusion."

**Plan**
1. Phase 0 — git state, then diff every status claim against evidence.
2. Phase 1 — probe actual binaries; separate skills from executable tools.
3. Phase 3 — diagnose the black frame by reading `tools/blender_evee_test.py` before rendering anything.
4. Phases 2/4/5/6 — spec, architecture, POC, pipeline.
5. Phases 7/8 — score with evidence, then three adversarial passes.

**Thinking**
- The black frame is a scene bug, not a hardware finding. If diagnosable from source, no render is needed to explain it.
- The user's autonomy clause authorises "lightweight tests with existing approved tools" and bounded preview tests. It does not authorise full-resolution jobs, installs, or spend.
- Documentation consistency scoring 2/5 is most likely correct: README still says "no benchmark executed" while `BLENDER_EEVEE_RESULT.md` holds a measured result.

**Assumptions**
- The repo is the same directory the user opened; `origin` is `youcisla/ContentFactory`.
- No commit or push will be made.

**Risks**
- A bounded preview render may still be blocked by the PreToolUse gate. If blocked, document and stop at code diagnosis.
- Context budget: ten phases in one prompt invites shallow work. Mitigation: write each deliverable to a file rather than chat.

**Success criteria**
- Every status claim in the repo either matches evidence or is corrected.
- The black-frame cause is named specifically, with a fix and proof.
- Scores are 0–5 with named artifacts, not opinions.

### AFTER

**Phase 0 — reconciled.** 20 discrepancies recorded in `docs/reviews/DISCREPANCY_REGISTER.md`; 15 corrected in place (`README.md`, `MASTER_PLAN.md`, `BACKLOG.md`, `RISK_REGISTER.md`, `APPROVAL_GATES.md`), 3 deliberately left (immutable reports, ADR statuses, a research score that would need a re-run to change), 2 flagged as unaudited.

**Phase 1 — capability audit.** Blender 5.2.3 at `tools/blender/blender-5.2.3-windows-x64/`; FFmpeg 8.1.1; Node 26.12.1; Python 3.14.6; Rust 1.96.0; Chrome installed; git 2.54.0. Distinction recorded: the ~2,200 skill/agent entries in `localtools.md` are instructional and grant no capability — only the binaries above execute.

**Phase 3 — Blender verdict corrected.** `docs/benchmarks/BLENDER_EEVEE_CORRECTION.md`.
- Black frame: five compounding scene defects (albedo 2–6 %, world 1 %, lights not tracked, AgX uncompensated, 50 mm framing cropped a 1.6 m card in a 0.99 m-wide frame). None is a hardware finding.
- **GPU backend resolved:** `Intel(R) Graphics`, OpenGL `4.6.0 - Build 32.0.101.8860`, backend `OPENGL`. **Not software.** The original "maybe software fallback" risk is closed as refuted.
- Curve at 1080×1920: **6.67 s @ 8 spp, 15.67 s @ 32, 29.14 s @ 64** (identical luminance to 4 d.p. across all three), **77.41 s @ 64 with raised shadow sampling** (2.7×).
- 240 frames: 27 min to 5.2 h. The "11× over budget" figure was overstated; the true range is 1.8× to 20.7×. Verdict unchanged.
- **The dominant cost is shadow sampling, not TAA.** Optimising sample count buys nothing visually and modest time.

**Phase 5 — proof artifact.** `tools/blender_scene_proof.py` renders a 14-material contactless-payment still at 1080×1920 with three-point lighting, real ID-1 card geometry, gold chip, magnetic stripe, emissive NFC rings, and a dark studio sweep. Output `proof_final.png`. It **passes an objective gate** the original benchmark lacked: mean luminance 0.2468 in [0.040, 0.400], p99 0.7107 ≥ 0.70, dark fraction 0.0447. The gate caught two real regressions during iteration (a lost highlight; a blown floor hotspot).

**Not done**
- No 10 s sequence. Local cannot meet the budget at any measured setting; remote needs approval and spend.
- Phases 2, 4, 6 not newly produced: `TREATMENT_TAP.md`, `BENCHMARK_SPEC_PREMIUM.md` and `reports/v2/02` already cover spec, architecture and pipeline intent. Re-writing them without new evidence would add words, not information.
- No architecture was compared on the same storyboard. That is the honest gap in "architecture validation".

**Scorecard** (`docs/reviews/REMEDIATION_REVIEW_2026-10-30.md`): process 4, tool discovery 4, hardware 4 (was 3.5), architecture 3.5 (was 4), documentation 3.5 (was 2), visual 3 (was 2), production readiness 1.5 (unchanged). No aggregate — averaging hides that no video can be produced.

**Defect found while checking the diff:** `tools/.gitignore` was a bare `*`, so `blender_evee_test.py` — the CF-020 evidence script — was invisible to git. A fresh clone could not reproduce any render claim. Narrowed to `blender/`, `blender-test/`, `*.zip`. **Revert if that was deliberate.**

**What to improve**
- E3 (no determinism check) and E4 (evidence images unversioned) are the two engineering findings that matter most.
- C1 and C7 from the cinematic pass: the NFC rings read as hoops, and the frame teaches nothing. Fixing those is the difference between a product mockup and an explainer.
- P5 from the product pass: script, factual verification and narration have no work behind them at all.

**Next:** approval needed on remote render (B1) or B0 (B2) before any further rendering.

---

## 2026-10-30 · V4 quality validation + architecture correction

### BEFORE

**Prompt (summary):** The corrected Eevee *measurements* are accepted; the *visual-quality and architecture* decisions are not. Nine tasks: update ADR-0001/0002 with measured data; compare 8/32/64 samples on crops, edges, shadows, reflections and noise rather than mean luminance; test temporal flicker; write an objective visual-QA spec; preserve the scene and its sources; find the smallest useful local animation benchmark; reassess local Eevee for hero shots/previews/unattended; fix stale docs; adversarial review scored on observable evidence. Produce a contact sheet if the proof image exists.

**Hard constraint repeated by the user:** no installs, no cloud purchase, no heavy benchmarks, no commit, no push, no full pipeline.

**Plan**
1. Re-render the *current* scene at 8/32/64 with identical shadow settings, so the sample comparison is not confounded by material or lighting changes made after the first curve.
2. Write a comparison tool: per-region crops, edge-gradient statistics, flat-region noise variance, RMSE/PSNR against the 64-sample reference.
3. Temporal test: render the same static frame twice at 8 samples and measure pixel difference. TAA sampling noise is what flicker looks like.
4. Contact sheet from actual crops.
5. Docs, ADR amendments, QA spec, scorecard.

**Thinking**
- The previous claim "8, 32 and 64 samples are visually identical" rested on mean luminance to four decimals. That is a weak test: mean luminance is blind to noise, to edge stability and to shadow stippling. If it is wrong, it is wrong in exactly the place that matters.
- The earlier `spp8/32/64` frames predate the material, card-detail and lighting fixes. Comparing them to each other is valid, but comparing them to `proof_final` is not.
- Flicker is the decisive question for animation. A frame that looks fine alone can strobe when 240 of them run.

**Risks**
- Re-rendering may push past the "no heavy benchmarks" line. Mitigation: three stills at ~51 s total plus two 8-sample frames, all 1080×1920, all bounded.
- The comparison could invalidate the earlier "8 samples is enough" claim. That is the point of running it.

**Success criteria**
- Every claim in the sample-count table is backed by a number computed from pixels, not by eye.
- A contact sheet exists showing where the image is strong and where it fails.
- The architecture recommendation states what changed and why, or states that nothing changed and why.

### AFTER

**The earlier claim was wrong and is withdrawn.** "8, 32 and 64 samples are visually identical" was based on mean luminance. Region-level SSIM refutes it.

**Renders** (identical scene, default shadows, 1080×1920): 8 spp **7.13 s**, 32 spp **15.67 s**, 64 spp **25.15 s**. 8 spp + raised shadow sampling **11.02 s**.

**Per-region convergence vs 64-sample reference:**

| Region | 8 vs 64 SSIM | 32 vs 64 SSIM | 8+shadow SSIM |
|---|---:|---:|---:|
| card | 0.9989 | 0.9997 | — |
| rings | 0.9983 | 0.9994 | — |
| background | 0.9988 | 0.9995 | — |
| bevel | 0.9689 | 0.9941 | **0.9844** |
| **floor** | **0.7876** | **0.9292** | **0.8447** |
| whole frame | 0.9565 | 0.9878 | — |

- **Floor is the failure.** It never converges below 64 samples. Cause is glossy specular sampling, not shadows — raising shadow quality moved it only 0.788 → 0.845.
- **Whole-frame SSIM 0.9565 masked it.** Averaging a converged card against a failing floor produced "acceptable". That is why QA-7 now requires per-region convergence.
- **Bevel noise IS shadow sampling** — 0.9689 → 0.9844, into range, for 1.55× the time.

**Temporal stability — good result.** Three static frames at 8 samples are **bit-identical**: SSIM 1.000000, PSNR infinite on all three pairs. Eevee's TAA is deterministic here, so there is no Monte-Carlo flicker component. Caveat: a static-scene test proves determinism, not the absence of flicker under motion.

**Contact sheet:** `tools/blender-test/contact_sheet.png` — 5 regions × (8 samples | 64 samples). Confirms by eye what the metrics say: card/rings/background indistinguishable, bevel grainy, floor heavily stippled at 8.

**The substantive finding:** the biggest local performance lever is not sample count or resolution — it is **whether the floor reflects**. Matte floor at 8 spp: 28 min per 10 s. Glossy floor at 64 spp: 100 min. A 3.6× span decided by art direction, not by settings. That belongs in `BENCHMARK_SPEC_PREMIUM.md`.

**ADRs amended, statuses preserved as `proposed`.** ADR-0001: the "Eevee unmeasured" rejection reason is now measured; spine decision unaffected because it rests on determinism and cost, not Eevee speed. ADR-0002: two premises corrected — Eevee is measured, and the $0.108/h GPU figure was a spot outlier (verified $0.34–0.41/h).

**Not done**
- No motion rendered. CF-028 is the smallest test that produces it and is now the open approval request.
- QA-4/5/6/9/10 specified, not implemented.
- No hash manifest for the evidence PNGs, which stay gitignored.

**Scores** (`docs/reviews/V4_VALIDATION_2026-10-30.md`): engineering 4.5, hardware 4.5, documentation 4, tool discovery 4, architecture 3.5, visual 3, production readiness 1.5. **Visual did not improve** — the round found a defect rather than fixing one.

**What to improve**
- A3 is the highest-value open engineering item: the floor is both the worst region and the bottom third of frame (C8).
- The matte-vs-glossy floor decision must be made in the creative spec before any further render benchmarking, because it sets the entire local budget.

**Next:** CF-028 approval — 24 frames, 540×960, 8 samples, ~3 min, €0.

---

## 2026-10-30 · CF-028 executed · first motion

### BEFORE

**Prompt:** "approved" — CF-028 authorised.

**Scope as approved:** 24 frames, 540×960, 8 TAA samples, encoded with FFmpeg. Under 3 minutes, €0, no install.

**Plan**
1. Render 24 frames with the existing camera orbit (1.5°/frame, 34.5° total).
2. Encode with libx264, yuv420p, constant quality.
3. Verify the MP4 with ffprobe: frame count, duration, dimensions.
4. Compute frame-to-frame SSIM across the moving sequence — the flicker test the static scene could not provide.
5. Compare measured render time against the estimate from `SAMPLE_AND_TEMPORAL_QA.md` §5.

**Thinking**
- This is the first moving image the project has produced. Its purpose is not beauty; it is to answer whether an animated sequence exposes instability the static test hid.
- The estimate (~108 s) comes from `t ≈ 2.8 + 3.32 µs × px` at 8 samples. Shadow quality is left at its raised default, so the real number will be higher. That discrepancy is itself a result worth recording.
- 1 second is enough to see whether consecutive frames differ smoothly or stutter. It is not enough to judge pacing.

**Risks**
- The 1.5°/frame orbit may be too fast or too slow to read at 24 fps.
- 540×960 is a preview grade; grain visible at half resolution will differ from the 1080×1920 measurements.
- Encoding might fail on an odd dimension; 540×960 are both even, so yuv420p is safe.

**Success criteria**
- A valid MP4 exists, 24 frames, 1.0 s, 540×960.
- Measured render time recorded, compared to the 108 s estimate.
- Frame-to-frame SSIM recorded for all 23 adjacent pairs.

### AFTER

**Produced:** `tools/blender-test/cf028.mp4` — 540×960, 24 frames, 1.000 s @ 24 fps, h264, 136,429 bytes. The first moving image in the project.

**Measured cost**

| Metric | Value |
|---|---|
| Total wall clock | **74.6 s** |
| First frame | 4.07 s |
| Median frame | **2.42 s** |
| Setup | 1.65 s |
| **10 s at 540×960** | **≈ 9.7 min — fits the ≤15 min V4 budget** |

The §5 estimate was ~108 s; actual 74.6 s. The estimate was 31 % conservative.

**Temporal stability — pass.** All 23 adjacent-frame SSIM pairs between **0.9589 and 0.9718**, mean 0.9684, monotonic with a 0.013 spread. No outliers, no dropped or duplicated frames, **no flicker**.

**Defect F1 — exposure drift 32 %.** Per-frame YAVG falls monotonically 69.61 → 47.35 across 24 frames. The camera orbits out of a world-fixed key light. Not flicker; a one-directional fade. **The gate failed on frame 24 (`p99 = 0.6676 < 0.70`) and was correct to** — the frame genuinely lost its highlights. Root cause is scene construction: the lights do not follow the camera, so any orbit is a turntable with a fixed key. Fix is CF-030.

**Defect F2 — the gold chip renders black.** `metallic = 1.0` has no diffuse term; at frame 24 nothing bright is in the reflection cone, so the chip returns near-zero. Fix is CF-031 (environment source, or drop metallic to ~0.85).

**Gate semantics is now a known defect.** An absolute per-frame threshold flags a legitimately darker frame without distinguishing "broken image" from "shot drifted". QA-2 needs to be evaluated across the sequence, not on the last frame.

**What this changed**
- Half-resolution 10 s clips are now **measured viable locally at 9.7 min** — previously only estimated.
- Motion is confirmed deterministic and smooth; the earlier static-frame result holds under animation.
- Two real defects surfaced that no still could have shown: exposure drift and metals in vacuum.

**What to improve**
- CF-030 and CF-031 are both cheap and both block any believable orbit.
- The orbit's 1.5°/frame was chosen arbitrarily. Pacing has never been judged by a human.

**Next:** CF-030 (camera-relative lighting) and CF-031 (environment reflection) — both repository-local, both €0.

---

## 2026-10-30 · CF-030 / CF-031 · controlled lighting and material validation

### BEFORE

**Prompt (summary):** Implement two lighting candidates — **A** camera-relative studio rig, **B** fixed rig with environmental reflections — compare them on identical camera path, resolution, samples, colour management and output; measure exposure drift, highlight visibility, chip readability, continuity, time and memory; add sequence-level QA that separates intentional lighting change from accidental drift; deliver a contact sheet with chip/terminal/card crops; adversarially review and fix.

**Acceptance targets:** exposure within ±5 %, chip visible as metal throughout the move, no unintended temporal artefacts, no cost increase without demonstrated benefit.

**Plan**
1. Refactor `blender_scene_proof.py` to build either rig from `CF_RIG=A|B`, keeping every other setting identical.
2. Rig A: parent the three area lights to an empty and rotate it by the same angle as the camera, so the key never leaves the subject.
3. Rig B: keep the lights world-fixed; add a procedural vertical-gradient world so metals have something to reflect and the scene gains view-independent fill.
4. **Do not touch `metallic`.** Fix metals with reflection sources and roughness first, as instructed.
5. Render stills at orbit positions 0, 12, 24 for both rigs, then a bounded 24-frame run per rig.
6. Sequence QA: normalised drift, second-difference flicker index, per-frame luma. SSIM alone is explicitly rejected as sufficient.

**Thinking**
- The 32 % drift is not a renderer problem; the key light is a fixed point and the camera is a moving point. Two honest fixes exist — move the lights with the camera, or make the light less directional. A and B are those two answers.
- The black chip is a physics consequence: a metal with `metallic = 1.0` has no diffuse term and can only show what it reflects. Changing metallic to hide that would be the wrong fix and is explicitly ruled out.
- Sequence QA must not simply fail on any change. A deliberate lighting change is legitimate; an unnoticed one is not. The distinguishing rule must be stated in the QA, not applied by eye afterwards.

**Risks**
- Rig A may look static and lifeless if the lighting never changes with the camera — a known turntable trade-off.
- Rig B may not fully remove drift, because a fixed key still loses its angle.
- A gradient world raises render cost; the target says no cost increase without demonstrated benefit, so both must be timed.

**Success criteria**
- Both rigs rendered under identical settings, timings recorded.
- Drift measured per rig; at least one within ±5 %.
- Chip legible in every rendered frame of that rig.
- A sequence-QA rule written down that distinguishes intended from accidental change.

### AFTER

**Both candidates built behind one switch** (`CF_RIG=A|B`, plus `CF_STILL_ORBIT` for positioned stills). One `place_orbit()` drives stills and sequences so the camera path is identical by construction, not by convention.

**Results**

| | Rig A camera-relative | Rig B fixed + gradient world |
|---|---:|---:|
| Still deviation from orbit 0 | **2.8 %** | 34.1 % |
| `seq_max_deviation` (24 frames) | **3.55 %** | 33.50 % |
| `seq_flicker_index` | 0.00043 | 0.00093 |
| luma first → last | 0.2470 → 0.2393 | 0.2770 → 0.1842 |
| Last-frame gate | PASS | FAIL (p99 0.6724) |
| Per-frame render | 2.10 s | 2.09 s |

**Acceptance targets:** exposure ≤ ±5 % — **A passes at 3.55 %**; chip visible throughout — **both pass**; no unintended temporal artefacts — **both pass**; no cost increase without benefit — **neither costs more**, so cost does not decide.

**CF-030 and CF-031 resolved.** CF-031 in particular was solved by both rigs with `metallic` untouched at 1.0, as instructed.

**Why B failed — the useful finding.** Environment light adds a constant, not a proportional term. It made frame 1 brighter (0.2770 vs 0.2470), which looked like progress, while the key light still rotated away. Ambient raised the floor; it did not stop the fall. **Ambient cannot fix a directional problem.**

**Why A still drifts 3.55 %** — not the lights. Rotating a light about the Z axis through the origin leaves its distance to the target invariant, so the key's contribution is exactly constant. The residual is the fixed world and the view-dependent floor reflection. Three and a half per cent is the cost of holding the world still.

**QA rule replaced.** QA-8 previously read "SSIM within the motion bound". SSIM measures difference, and a shot can change smoothly while fading to black — which is exactly what CF-028 did. Replaced with two independent measures computed in the script: `seq_max_deviation` (departure from frame 1) and `seq_flicker_index` (mean absolute second difference of the luma series, normalised). `CF_INTENTIONAL_DRIFT=1` reclassifies drift as `INFO(intentional-drift)` so a scripted light move is distinguishable from an accident.

**Adversarial findings**

| ID | Finding | Status |
|---|---|---|
| G1 | Rig A makes the subject's lighting invariant with camera angle; a long turntable may read flat | **Open** — trade-off accepted for short hero shots |
| G2 | Stills rendered at 32 samples, sequences at 8, so quality is not directly comparable across them; only lighting is | Noted |
| G3 | The `gate=` field still reports the last frame on a sequence, which is not representative | **Open** — `seq_verdict` now carries the sequence answer, but the field name still misleads |
| G4 | Rig B's gradient world costs nothing (2.09 vs 2.10 s/frame), so "no cost increase without benefit" is satisfied vacuously for the losing option | Noted |

**Files:** `tools/blender_scene_proof.py`, `docs/benchmarks/SAMPLE_AND_TEMPORAL_QA.md` §9, `tasks/BACKLOG.md`.

**Artifacts:** `rig_compare.png`, `chip_crops.png`, `motion_strip.png`, `regions_compare.png`, `cf030_A.mp4`, `cf030_B.mp4`.

**Next:** creative approval of Rig A. Nothing else should be built until the look is accepted.

---

## 2026-10-30 · V4 cinematic scene + QA system correction

### BEFORE

**Prompt (summary):** Rig A is the technical lighting baseline, **not** the creative standard. CF-030/031 technically complete, visual acceptance pending. Build: a corrected QA system (clear gate naming, region-specific temporal QA, shot-type thresholds, documented expected-exposure curve); a genuinely cinematic composition; and a shot that **teaches** a contactless payment interaction including the authorization request leaving.

**Non-negotiables restated:** no installs, no paid services, no heavy benchmark, no commit/push/publish; do not raise resolution or duration merely to improve a score; stop for creative approval.

**Plan**
1. Extract QA into `tools/cf_qa.py`: rename `gate` → `frame_gate`, add `seq_verdict` as the sequence answer, add per-region temporal metrics, add shot-type threshold sets, add expected-curve validation.
2. Leave `blender_scene_proof.py` as the preserved Rig A baseline; build the cinematic scene in a new `tools/blender_scene_v4.py`.
3. Scene: remove the three floating torus rings. Replace with a card antenna coil that energises, a terminal indicator that confirms, and a discrete packet that departs — approach → couple → confirm → request.
4. Composition: reduce floor dominance, add a graded backdrop so the upper third carries meaning instead of emptiness, improve terminal proportions and card detail.
5. Camera: replace the constant 1.5°/frame orbit with an eased dolly-in.
6. Stills first, then one 24-frame sequence at 540×960 — same resolution and duration as CF-028, not more.

**Thinking**
- The rings were the worst defect. They were decorative, they read as literal technology, and they taught nothing. Removing them is a correctness fix, not a style choice.
- A payment explainer must show cause and effect. The chain is: field energises the card's coil → terminal confirms → request departs. Three states, each visible.
- "Request begins its journey" needs a departure, which needs a destination in frame. That is what the empty top third is for.
- QA must be able to say "this shot was supposed to dim, and it did" versus "this shot dimmed by accident". That requires an expected curve, not a fixed threshold.

**Risks**
- A backdrop and a travelling packet add cost. Target says no cost increase without demonstrated benefit — both must be measured.
- A 1-second shot may be too short for a three-beat story. If so, that is a finding, not a reason to lengthen without approval.

**Success criteria**
- No field named `gate` remains ambiguous; `frame_gate` and `seq_verdict` are distinct.
- Per-region drift and flicker reported for card, chip, terminal, background.
- The three-beat story is legible in stills alone.
- Cost measured against the Rig A baseline.

### AFTER

**Built:** `tools/cf_qa.py` (shared QA) and `tools/blender_scene_v4.py` (cinematic scene). `blender_scene_proof.py` untouched — the Rig A baseline is preserved.

**QA system — all five items done**
- `gate` split into `frame_gate` + `frame_gate_reason` and `seq_verdict`. No ambiguous field remains.
- Per-region temporal QA: `region_card_*`, `region_chip_*`, `region_terminal_*`.
- `SHOT_THRESHOLDS` for `product_still`, `product_motion`, `diagram`, selected by `CF_SHOT`.
- `CF_EXPECTED_CURVE` → `seq_expected_curve_error`; without a declared curve, drift >5 % fails rather than being waived.
- §2–§9 and every existing `.txt` report preserved unchanged.

**Scene — built, not accepted.** Coil replaced the torus rings. Eased dolly replaced the constant orbit. Matte floor, emissive backdrop, terminal head, screen, NFC indicator, departing packet.

**Measured**

| Item | Value |
|---|---|
| Stills 1080×1920, 24–32 spp | 18.4–43.3 s |
| Sequence 24 frames, 540×960, 8 spp | **2.73 s/frame** |
| 240 frames | **≈ 11.0 min** |
| `frame_gate` (final frame) | PASS — mean 0.2846, p99 0.9947 |
| `seq_max_deviation` | **10.95 %** |
| `seq_flicker_index` | 0.00292 |
| `seq_verdict` | **FAIL** |

**The QA worked and found a criterion problem, not an image problem.** A dolly-in from 0.53 m to 0.38 m must brighten ~10 % — that is the arithmetic of the move. And fixed region rects inflate as the subject grows: the card "deviates 86 %" because the box fills with card, not because the light changed. Both limits were inherited from the CF-028 *orbit*, where framing was constant. This is the concrete evidence item 1 needed: a `dolly` shot type requires scale-invariant exposure and object-tracking rects. Recorded as **CF-035**, open.

**Visual defects found on inspection**

| ID | Defect | Severity |
|---|---|---|
| V1 | Packet passes **through the card** — it starts inside the reader head and the Bezier arc crosses the card body around frames 12–14 | **High** |
| V2 | Packet **exits frame** at the end — the third beat is half legible | **High** |
| V3 | Hard horizontal backdrop seam across the upper third | Medium |
| V4 | Terminal reads as two stacked boxes, not a reader | Medium |
| V5 | Card has no number block or branding | Medium |

**Creative verdict: not accepted.** The scene has a story structure and an accurate coil, but the payoff beat is physically broken (V1) and then invisible (V2). That is the whole difference between "a card over a box" and "the request leaves".

**Cost:** 2.73 s/frame vs the Rig A baseline's 2.10 s (+30 %), from the backdrop emission and extra objects. The benefit is real but not yet earned, because the shot is not good enough to call it.

**Bugs fixed during the build** — worth recording because both were invisible until rendered:
- `on_card()` baked `card.matrix_world` once, so the chip, stripe and coil stayed where the card started while the card animated away from them. Fixed by parenting with an identity parent-inverse.
- The packet path ended 17.8° off the view axis against a 14.4° half-FOV — outside the frame by construction. Found by computing the angle rather than by re-rendering.

**Next:** CF-034 (packet trajectory), CF-035 (dolly QA), CF-036 (backdrop seam, terminal silhouette). None requires approval beyond a go-ahead; all are repository-local and €0.

---

## 2026-10-30 · Autonomous run · candidate B + end of bounded cycle

### BEFORE

**Prompt:** autonomous studio mode. Fix CF-034/035/036, establish premium art direction across up to two candidates, build a complete educational shot, score to 90/100. Bounded: max three creative revisions per candidate, max two candidates before reassessment, one render worker.

**Plan:** one new candidate (B) rather than a third revision of A — A had already absorbed four passes.

### AFTER

**Candidate B changes**
- World gradient replaced the backdrop plane. **Seam removed**, and metals gained a gradient to reflect with no added geometry.
- Terminal head re-proportioned, sloped, with the screen parented to it in local space so it cannot protrude.
- Card keeps coil, chip, stripe; terminal keeps an NFC indicator.
- Packet start moved behind the reader head; arc re-routed.
- Camera 65 mm, eased dolly.
- `cf_qa` extended: per-frame region rects, **scaled by projected radius** so coverage stays constant as the subject grows.

**Measured**

| Metric | Candidate A | Candidate B |
|---|---:|---:|
| Mean luminance | 0.2846 | 0.2624 |
| p99 | 0.9947 | 0.9983 |
| `frame_gate` | PASS | **PASS** |
| `seq_max_deviation` | 10.95 % | 10.44 % |
| `seq_flicker_index` | 0.00292 | 0.00293 |
| `region_card_deviation` | 86.0 % | **30.5 %** |
| `region_chip_deviation` | 79.7 % | **50.7 %** |
| `region_terminal_deviation` | 101.6 % | **17.9 %** |
| `region_card_flicker` | 0.04235 | **0.00575** |
| per-frame 540×960 @8 spp | 2.73 s | **2.40 s** |

**CF-035 is most of the way solved.** Tracking alone cut region flicker 5×; scaling the rect by projected radius cut deviation roughly in half again. What remains is not a measurement artefact: the subject really does brighten as the dolly closes (inverse square), and the coil and screen are scripted to brighten. Separating those two needs a declared expected curve — the mechanism exists (`CF_EXPECTED_CURVE`) and is unused.

**CF-034 partial.** The packet no longer intersects the card. At frame 24 it is still a dot at the frame edge and leaves. Second reduction needed.

**CF-036 partial.** Seam gone. Terminal still reads as stacked rounded boxes; the screen reads as a teal slab rather than a display.

**Bounded cycle exhausted.** Three creative revisions on A, one full rebuild as B. Remaining defects are art-direction defects, not defects another render pass would remove: the scene is grey-on-grey with no palette, no depth of field, and a subject that occupies a third of the frame.

**Score: 57/100** (see §11 of `SAMPLE_AND_TEMPORAL_QA.md` computation). Below the 90 bar. Stopping per the bounded-cycle rule rather than producing a third candidate without a creative direction from the user.

---

## 2026-10-30 · Cleanup audit + task-ID reconciliation

### BEFORE

**Prompt:** autonomous studio mode. Mandatory cleanup audit before further implementation; resolve the CF-030–CF-035 ID collisions; fix CF-034/035/036; deliver a 30–45 s educational Short.

**Plan:** do the mandatory, high-value, bounded work first — inventory, classification, ID mapping — then continue to scene fixes with whatever budget remains.

### AFTER

**Inventory:** 93 tracked files, 0 untracked, 7,661 ignored. `tools/blender/` 929 MB, `tools/blender-test/` 239 MB (217 PNGs = 249 MB, 5 MP4s = 630 KB, 49 QA reports). Total ≈1.17 GB.

**Key structural finding:** tracked content is small and clean; **all the mass is ignored and regenerable**. The repository is in the right shape — the only waste is 249 MB of intermediate frames with no retention policy.

**Classified A–F** in `docs/reviews/CLEANUP_AND_ID_RECONCILIATION.md`. Quarantine proposal: ~233 MB of Class D/E sequence frames. **Nothing deleted** — pre-existing files need authorization.

**ID collisions resolved.** CF-028–CF-036 collided with Phase 3 spine IDs. The 3D workstream moved to the 1xx band (CF-128–CF-136); the spine keeps its originals; no history deleted. Nine rows renumbered in `tasks/BACKLOG.md`, mapping documented, band rule written into the ID rule line.

**Not done this cycle:** CF-134/135/136 fixes, and the 30–45 s Short. No new renders were produced. The blocker is remaining working budget in this session, not a resource, permission, or dependency.

**Next:** resume at CF-134 — packet end point needs a second reduction so it stays in frame for its full travel.

---

## 2026-10-31 · Resume — doc correction, CF-134/135/136, Short assembly

### BEFORE

**Prompt:** resume ContentFactory autonomously. Correct stale documentation-only phase descriptions preserving historical approval boundaries; verify task-ID mapping and fix double counting in the cleanup manifest; finish CF-134 (packet visible and collision-free for full journey, camera-space geometry tests), CF-135 (tracked regions, dolly exposure criteria, documented intentional lighting changes, orbit regressions preserved), CF-136 (recognizable terminal, convincing materials, focal hierarchy, coherent art direction); produce premium storyboard + source-verified script; assemble the best Short achievable within limits.

**Plan:** (1) subagent compatibility probe against the current provider, read-only. (2) Documentation corrections: MASTER_PLAN status line, CLAUDE.md/AGENTS.md current-phase sections, BACKLOG stale ID refs, CLEANUP manifest double count. (3) Read `tools/blender_scene_v4.py`; add camera-space geometry assertions for the packet; implement the declared expected-exposure curve; rebuild terminal geometry and materials. (4) Stills before sequences. (5) Storyboard + script. (6) Assemble.

**Assumptions:** the V4 scene work already authorised under CF-021/CF-133 continues; no new install, no download, no cloud, no publishing. Local Eevee renders at 540x960 are within the already-approved resource envelope.

**Risks:** render time on Intel iGPU; art-direction quality is the open unknown, not mechanics; context budget.

**Success criteria:** geometry test fails on the old path and passes on the new one; region deviation under a declared curve passes or is honestly reported; terminal recognisable at 360 px; storyboard and script on disk with sourced claims; render or an explicit statement that it was not produced.

### AFTER

**Agents used (actual):** 1 read-only compatibility probe, 1 source-verification agent, 1 storyboard agent. **Not** used: concurrent render workers. Probe returned `DRIFT_MAX = 0.05`, the exact `sequence_qa` signature and 3 threshold keys — all correct, so runtime agents work on this backend. Probe cost 69.5 k subagent tokens; verification 156.7 k; storyboard 149.3 k.

**Documentation corrections.** `CLAUDE.md`, `AGENTS.md` and `MASTER_PLAN.md` header said "documentation only"; the project has been in V4 since 2026-10-30. Corrected without widening any approval — B0 stays unauthorised and the phase text now says so. ID mapping verified: nine rows one-to-one, no reuse. Two stale references fixed in the live backlog (`CF-133 → CF-134/135`, `CF-129 blocked by CF-028 → CF-128`). Cleanup manifest double count corrected in **`docs/reviews/CLEANUP_AND_ID_RECONCILIATION_V2.md`** — v1 is an audit and stays unedited per ADR-0006. Real cleanup is **68.4 MB**, not 233 MB.

**CF-134 — done.** Added `packet_geometry()`: NDC framing with a 6 % margin, OBB clearance, and a camera→packet ray cast. Current path PASSes (edge margin 0.140, clearance 3.19 mm). **Negative control**: the `a7d4a18` path FAILs the same gate — hidden behind the card at f14–15, 4.8 mm inside it at f16, right-edge breach at f23–24. The gate has been shown to fail. The occlusion check found a defect no framing test could see: the packet launched *behind the card's far edge*.

**CF-135 — done.** `curve_at()` predicts exposure from the actual light positions and inverse-square falloff; error is a normalised relative error, so the curve needs no fitted scale. `CURVE_MAX = 0.25` applies only when a curve is supplied — the 5 % orbit rule is untouched. 240-frame result: whole frame **5.18 %**, terminal **3.37 %**, chip **19.97 %**, card **21.01 %**, flicker **0.00006**, verdict PASS. The card residual is **not** the scripted emission: an emission-off control run gave 33.27 % against 33.39 %, a 0.12-point change. It is view-dependent specular, now labelled as such instead of excused.

**CF-136 — done.** Terminal rebuilt as body + tilted head + glossy bezel + dark display glass + amount line + approval tick + 12-key keypad + card slot + status LED. Two structural faults found by inspecting renders, not by reasoning: the card was held directly over the display (hiding it), and every material sat within 12 % of the others. Fixed with a forward tap point, a 23° camera elevation, and value/specular separation. Four render iterations; each defect above was named from an image before being fixed.

**Video produced.** `tools/blender-test/contactless_10s_captioned.mp4` — 540×960, 24 fps, 240 frames, 10.0 s, 729 KB, captions burned in from `render/captions/contactless_10s.srt`. Raw encode 683 KB. Render: median **1.54 s/frame**, 371 s of render, ~7 min wall clock. Selection PNGs 110.2 MiB.

**Script and storyboard.** `docs/creative/SCRIPT_CONTACTLESS.md` and `docs/creative/STORYBOARD_CONTACTLESS.md`, claims bound to `docs/research/contactless-claims/CLAIMS.md` (7 VERIFIED, 1 PARTIAL, 0 unverified). **No narration audio exists** — every line is a labelled placeholder and the film is built to work captioned. The PARTIAL claim (tokenisation) is deliberately unused.

**Not done.** The 40 s, six-beat cut is written but **not built**: it needs a return leg on the packet and a re-time to 960 frames, about 25 min of render. The 1080×1920 master has not been run (≈4× render time). No music, no voice.

**Risks noted.** Disk free is **49 GB**, below the 50 GB stop condition recorded in `APPROVAL_GATES.md` G6. Nothing here writes further large output without freeing space first.

**Next executable action:** `CF_FRAMES=960 CF_STORY_FRAMES=960 CF_PREVIEW_SAMPLES=8` after adding the packet return leg — or free disk first.

---

## 2026-10-31 (later) · Milestone: 40 s animatic + safe path to final

### BEFORE

**Prompt:** deliver a complete 40 s animatic, not a final render. Disk cleanup proposal, factual review of the six-beat script, scene split (Blender for spatial mechanism, lightweight graphics for the network), reuse of validated assets, validate comprehension/timing/readability/accuracy/continuity, adversarial review, update records. No heavy rendering while the disk gate is breached.

**Measured first:** disk free is **77 GB**, up from 49 GB at the previous checkpoint. The 50 GB stop threshold in `APPROVAL_GATES.md` G6 is therefore **not** currently breached. I did not free that space and am not claiming it; the earlier reading is kept in the record.

**Plan:** (1) duplicate-hash the render artefacts and write a cleanup proposal with no deletions; (2) review the script's hold/approval/settlement wording and correct overstatements; (3) build the 2D network scenes as SVG, rasterise with the installed Chrome, assemble a 40 s animatic from the existing 240 frames plus those stills; (4) spawn independent QA agents on the result; (5) fix what they find.

**Assumptions:** an animatic is a previsualisation, not final picture. Captions are burned in; there is still no audio of any kind. The 10 s 3D cut is reused at native speed, not padded.

**Risks:** 2D scenes drifting into slideshow pacing; no Pillow, so 2D rasterisation depends on Chrome headless; context budget.

**Success criteria:** a playable 40 s file with six visually distinct beats, timed captions, and a written statement of what is animatic and what is finished.

### AFTER

**Delivered.** `render/animatic/contactless_40s_animatic.mp4` — 960 frames, 40.000 s, 540×960, 24 fps, 12 caption cues burned in, **no audio stream** (verified: 0 audio streams). Built by `tools/build_animatic.py`, which asserts its own contract: every encode is checked against an expected packet count before it replaces its target, and the run fails unless the final probes as exactly 960 frames and 40.000 s.

**Scenes.** A 0–10 s rendered 3D (240 frames, reused, not re-rendered for the animatic). B–E are SVG diagrams rasterised by Chrome and assembled by ffmpeg, with a moving marker for the request and the response. Sources in `render/scenes/`.

**Disk.** 77 GB free at start, up from 49 GB at the previous checkpoint — I did not free it. **Zero content-identical duplicates** among 523 PNGs, so the waste is superseded sequences, not copies. Proposal: 80.0 MB across 168 frames, nothing deleted, blocked on authorisation. Recorded in `CLEANUP_AND_ID_RECONCILIATION_V2.md` §6.

**Factual review.** An independent read-only reviewer returned 1 BLOCKER, 7 SHOULD-FIX, 5 NITPICK. The blocker was real: the hold diagram described a *balance* being held and a *reduced credit limit*, both wrong for a credit card — an authorization reduces **available credit** and leaves the limit unchanged. All but one nitpick are fixed in the scene sources, the script and the board. "NO CONTACT" is kept, with the reason recorded.

**Technical review.** A second independent reviewer returned 1 BLOCKER, 5 SHOULD-FIX. The blocker: segment A's length was whatever frames existed on disk, so dropping in the planned 960-frame render would have produced a 70 s file with every caption after 10 s mistimed, exit code 0. Fixed with a pinned frame count plus a contract assertion at the end of the build.

**Reassessment found a new defect.** Correcting the card crop moved the camera's end pose, which raised the card-region curve error from 21.0 % to **26.3 %**, over the 25 % band. Whole-frame error is 6.81 %. Cause: `curve_at()` models light distance only and has no view-dependent specular term. **The gate was not widened.** Verdict recorded as FAIL, with two candidate fixes and neither applied.

**Measured costs.** 1080×1920 at 8 samples: 8.51 s/frame steady state (frame 1 costs 11.4 s for shader compilation); 1.82 MB per frame. 240 frames ≈ 34 min ≈ 437 MB. The full-resolution render was **not** run.

**Not done.** No audio of any kind. The 1080×1920 master. The packet return leg for a full-3D 40 s cut.

**Next executable action:** choose one of the two card-region fixes in `ANIMATIC_QA_2026-10-31.md` §4 — model the view term, or make the card diffuse — then re-render 240 frames and confirm the region error returns under 25 %.

---

## 2026-10-31 · Premium 3D production reset — research and architecture

### BEFORE

**Prompt.** A reset brief: stop polishing primitive Blender scenes; evaluate open-source Blender agent/pipeline projects; research commercially usable assets; propose a production architecture; produce a premium visual treatment and, if authorised, an 8–12 s benchmark; compare against the current baseline; update the roadmap and hygiene records. Ten candidate repositories named; Poly Haven, Blender Studio and several asset/generator sites named.

**Verified first.** Working tree is clean at `d274790`. Disk free is **77 GB**, so the 50 GB G6 stop condition is not breached. Blender-driven subagents were already verified compatible in the previous milestone (probe returned the exact `DRIFT_MAX = 0.05` and threshold keys), so no new probe is run.

**Plan.** (1) Log this entry. (2) Run three independent read-only research streams in parallel: candidate Blender tooling, asset libraries and licensing, and how the two named reference creators actually achieve their look. (3) Write the open-source evaluation, asset strategy, architecture recommendation and visual treatment as new documents under `docs/`. (4) State the exact authorisation each remaining step needs instead of claiming work that was not done. (5) Update `BACKLOG.md` with new task IDs and leave phase/gate state to `MASTER_PLAN.md`.

**Assumptions.** Research is read-only and needs no gate. No install, download, service start or commit happens in this entry. The brief's own §12 permits bounded previews with existing tools, but a benchmark that needs new assets or new software also needs a named approval, so the default is to identify the blocker precisely rather than improvise.

**Risks.** Documentation volume substituting for visible improvement — the brief warns about exactly this, so findings must be short and evidence-tagged. Web sources can be stale or wrong; every claim carries a confidence label. Context budget across four large documents.

**Success criteria.** Each of the ten candidates has a verified existence/licence/maintenance verdict or an explicit UNKNOWN. Asset sources carry licence and commercial-use facts, not just links. The architecture decision names what to keep, replace and defer. The treatment is shot-specific enough to build from. Every unperformed step states its exact authorisation blocker. No commit, no install, no claim of visual acceptance.

### AFTER

**Delivered as documents, not as a film.** Three read-only research streams ran in parallel (candidate tooling, asset licensing, reference-creator method). No install, no clone, no asset download, no commit. Working tree now has 8 new/modified documentation paths plus one opt-in code block.

**Tooling (deliverable A).** Ten candidates evaluated with licence, capability and security detail: `docs/research/open-source-projects/EVALUATION_2026-10-31.md`. Shortlist: `ifBars/blender-agent-studio` (MIT, active, Claude Code-native, saves `.blend`), `shefq/blendrelay-mcp` (MIT, typed tools), `ahujasid/mcp-for-blender` (MIT, most battle-tested). Rejected: no licence (`nishit47`), AGPL behind an MIT README (`RFingAdam`), abandoned or stale repos, and the official Blender lab MCP which its own vendor says runs LLM code with no guards. **Multi-shot timeline is unproven for all ten.** Every candidate builds scenes by executing model-written Python.

**Assets (deliverable B).** `docs/research/assets/ASSET_STRATEGY_2026-10-31.md`. The decisive finding: **no CC0 payment terminal, card reader or credit card exists** in Poly Haven (521 models scanned), Sketchfab's CC0 filter, Kenney or Poly Pizza. Poly Haven and ambientCG remain excellent for CC0 HDRIs and PBR. Sketchfab has CC BY 4.0 terminals (credit required); the highest-detail one is a branded PAX device and is rejected on brand grounds. **No verified CC0 rigged hand exists**; Blender Studio Humans are CC0 but unrigged, Pip/Rain are CC BY. Smallest useful acquisition set is < 30 MB of CC0, with hero props modelled in-house.

**Architecture (deliverable C).** `docs/architecture/decisions/ADR-0007-asset-driven-scene-pipeline.md` (proposed). Asset-driven scene assembly, `.blend` template + JSON shot spec, deterministic render path; agents may author, agents never render. V4 is frozen as the technical baseline.

**Treatment (deliverable D).** `docs/creative/PREMIUM_TREATMENT_V5.md`. Original 11 s, four-shot treatment whose argument is carried by a rack focus from card to terminal. Ten checkable craft rules; explicit asset slots; explicit blockers.

**Measured (deliverable G).** Added an opt-in `CF_LENS_PROBE` block to `tools/blender_scene_v4.py` (unset = baseline unchanged) and rendered five 1080×1920 stills at 32 samples, frame 150:

| Run | Seconds |
|---|---:|
| baseline | 14.83 |
| DOF f/2.8 + 180° blur | 21.46 |
| DOF f/5.6 + 180° blur | 21.91 |
| DOF f/5.6, no blur | 17.42 |
| DOF f/16, no blur | 13.01 |

**Finding that changes the plan:** at ~0.35 m with a 65 mm lens, f/2.8 and f/5.6 blur the *entire* set — the terminal screen, which is the film's payoff, becomes unreadable. Only f/16 restores baseline sharpness. Shallow depth of field is not available at tabletop scale unless the background is far away. Motion blur is the cost driver, not DOF. Recorded in `docs/benchmarks/LENS_PROBE_2026-10-31.md`; treatment rule C2 rewritten accordingly.

**Reference-creator evidence.** Zack D. Films: contractor portfolio names Blender + Cascadeur + BlenderKit + After Effects + EmberGen with templates and a Flamenco farm — asset reuse, not bespoke modelling. Branch Education: buys and disassembles hardware, scans and rebuilds it to photographic fidelity, 1,100+ hours per video. Both spend on lens, light and sound. Team-size and per-day figures from fan wikis were not relied on.

**Not done, and why.** No premium benchmark: it needs asset download approval (CF-140) and a `.blend` template (CF-142); neither exists. No agent-tool trial: needs an isolated environment and approval (CF-143). No audio. No V5 frame. Creative acceptance untouched.

**Next executable action:** approve or refuse CF-140 (≤ 30 MB CC0 HDRI + PBR download). On approval: build `assets/manifest.json` + validator (CF-141), then the template (CF-142).

**Follow-up — CF-140/CF-141 approved and closed, 2026-10-31 18:03.**

User approved the asset download named as the next action. Downloaded a 10-file CC0 set, **23.1 MB total**, into `assets/`, with sha256 recorded for every file: `brown_photostudio_02` 2K HDR (Poly Haven), `metal_plate` 2K diffuse/rough/normal/metal (Poly Haven), `Plastic013A` 1K JPG (ambientCG). No account, no attribution owed, no collection download.

`tools/check_assets.py` (CF-141) validates the manifest: PASS on the real set (`assets=10 total_mb=23.1`), and the negative control with `commercial_ok=false` exits 1 with two FAIL lines, so the gate can fail.

Asset import proven headless: `CF_ASSET_HDRI` swaps the procedural world for the HDR and rendered frame 150 at **26.81 s** (1080×1920, 32 spp) against a 14.83 s procedural baseline — **+81 %**, the most expensive change measured so far. Visually the change is subtle at strength 0.3: environment alone does not make primitive geometry look premium, which is what the treatment predicted.

`assets/` is currently untracked. Whether 23.1 MB of binaries belong in git or should be re-fetched from the manifest URLs is the user's call; nothing was committed.

---

## 2026-10-31 · Asset-first production transformation

### BEFORE

**Prompt.** Transform the project into an asset-first, template-driven studio: research ready-made assets, build a catalog and reusable Blender template, a shot-template library, two art-direction candidates, a six-minute production spec and, as far as resources allow, a six-minute prototype; measure cold and warm production; perform an authorized cleanup of generated artifacts; update roadmap, scorecard and evidence. No installs, no paid services, no commit.

**Verified first.** `assets/` holds 10 CC0 files / 23.1 MB with sha256 in `assets/manifest.json`; `tools/check_assets.py` PASSes and fails on a bad row. `tools/blender-test` holds **621 files / 411 MB**, all untracked. Disk free 77 GB. `assets/.gitignore` currently contains a bare `*`, which also hides `manifest.json`.

**Plan.** (1) Log this entry. (2) Spawn one read-only asset-hunt agent; do not repeat the prior licence sweep. (3) Extend the manifest into a catalog with the fields the brief names, and extend the validator (duplicates, missing textures, format, polygon count where recorded). (4) Build CF-142 as a real `.blend` template with collections, camera rig, light rig, HDRI world and render/compositing settings; verify headless. (5) Render one still per art direction and compare. (6) Write the shot-template specification, the six-minute production spec, the scorecard and the cleanup manifest. (7) Delete only generated, regenerable, untracked files that meet all ten conditions; record every path.

**Assumptions.** Downloads remain limited to the already-approved CC0 set; new assets are researched and catalogued, not fetched. The six-minute film cannot be produced in this session; the deliverable will be the specification plus an explicit limiting-capability statement.

**Risks.** Breadth over depth: twelve deliverables invite shallow work. Cleanup is destructive; a wrong call is unrecoverable. Template work can regress the frozen V4 baseline if it edits that file. Time and context.

**Success criteria.** Catalog validates. Template opens headless and renders a frame with recorded hash. Two stills exist with an honest comparison. Cleanup has a manifest and recovers space without touching evidence. Every unbuilt deliverable names its exact blocker. No commit.

### AFTER

**Agent participation (actual).** One read-only subagent ran for this brief: an asset hunt (59 tool uses, ~149 k tokens) that verified individual models and licence terms. No render worker ran in parallel. The earlier three research agents belong to the previous brief and are reported there. Nothing in this entry claims an agent did work it did not do.

**Delivered.**

- `assets/manifest.json` extended into a catalog (id, category, format, style, blender_compatible, reuse, dependencies), version 2, 10 rows.
- `tools/check_assets.py` extended: duplicate id, duplicate sha256, unsupported format, catalog fields. Real set PASSes (`assets=10 total_mb=23.1`); negative control exits 1 with four FAIL lines.
- `tools/build_template.py` → `templates/cf_studio_v1.blend` (CF-142, done). Collections CAMERAS/LIGHTS/SET/PROPS/RIGS, two tracking cameras (85 mm f/8, 35 mm f/5.6), HDRI world at 0.3, PBR counter/backdrop/trim, 3.0 m backdrop, AgX Medium High Contrast, 180° shutter.
- `docs/production/SHOT_LIBRARY.md` — ten templates specified, one built, with a five-point template contract.
- `docs/production/SIX_MINUTE_SPEC.md` — cold vs warm definitions, shot budget, arithmetic showing why 8,640 locally rendered frames cannot fit ten minutes.
- `docs/reviews/QUALITY_SCORECARD_2026-10-31.md` — **58/100**, weighted, with per-category evidence.
- `docs/reviews/cleanup_2026-10-31B/` — cleanup manifest and per-file hash inventory.
- Second-pass asset rows appended to `ASSET_STRATEGY_2026-10-31.md`.

**Measured.**

| Item | Value |
|---|---|
| Template frame, 540×960/16 spp | **5.33 s**, mean 0.212, p95 0.526 |
| Light-scale sweep on the template | 1.0 → mean 0.501/p95 0.909 (blown); 0.3 → 0.352; 0.1 → 0.212; 0.03 → 0.104 |
| Cleanup | 173 files, **≈ 81 MB** reclaimed; `tools/blender-test` 411 MB → 340 MB; disk free 77 GB → **81 GB** |

The template's light powers were set from that sweep, not guessed: 2.2 / 0.55 / 7.0 W at a 4:1 key:fill ratio.

**Cleanup discipline.** Only the six series whose generator tag is unambiguous were removed. `anim_*` was **not** removed: its `.txt` records settings but no generator command, so provenance is uncertain and the brief says leave it. Class B evidence (`v4final`, `proof_seq`, `c136noemit`) was retained. Reproduction was proven by regenerating `v4seq` (24/24 frames, same 26.2 % card deviation) before deletion.

**Not delivered, with the exact reason.**

1. **Two art-direction candidates** — not rendered. A second direction needs the same hero prop; with a primitive subject the comparison would measure lighting, not art direction.
2. **Premium benchmark** — not produced. No terminal geometry, no human, no licensed hand. The V4 baseline remains the only 3D film.
3. **Six-minute animatic or film** — not produced. Missing audio (CF-139), hero props, a cache, and a six-minute script. `SIX_MINUTE_SPEC.md` §5 states this in order.
4. **Cold/warm timing** — not measured, because neither run exists. `SIX_MINUTE_SPEC.md` gives the arithmetic, not a result.
5. **Shot templates 2–10** — specified, not built; building empty shells would satisfy a count and prove nothing.

**Repo state.** `assets/.gitignore` corrected: binaries ignored, `manifest.json` and the ignore file re-included, so the licence catalog is versioned. `git check-ignore` confirms both behaviours. Nothing committed; the user retains commit authority.

**Next executable action:** model the terminal (CF-150, 4–6 h). Everything else that matters waits on it.

---

## 2026-10-31 · Asset-first terminal milestone (CF-150…CF-155)

### BEFORE

**Prompt.** Replace in-house primitive modelling with acquisition and adaptation of a professional payment-terminal asset; integrate it into `templates/cf_studio_v1.blend` using Blender's native asset library; produce two art-direction stills, a before/after benchmark, three working shot templates, an audio/assembly attempt, measurements, a scorecard and cleanup — without installing, paying, publishing or committing.

**Verified first.** Git clean at `b27a1e5`. `templates/cf_studio_v1.blend` exists (97 KB). `assets/` holds 10 CC0 files / 23.1 MB, manifest v2, validator PASS. `tools/blender-test` 340 MB. Backlog marks CF-150 `ready` as an in-house model; **this brief changes CF-150's definition** from "model from scratch" to "acquire, evaluate, adapt", a scope change recorded here and in `BACKLOG.md`, not silently applied. ADR-0007 rule 1 already requires a licence row with `commercial_ok=true` for any asset entering `assets/`.

**Plan.** (1) Verify terminal candidates and licences from primary pages. (2) Download only CC0/no-account sources; request approval for anything gated. (3) Import the selected asset headless, inspect geometry, adapt scale/orientation/materials. (4) Extend the template with a linked asset collection. (5) Render two art directions and the before/after pair at matched settings. (6) Build three parameterised shot templates as JSON + a runner. (7) Implement a content-addressed still/frame cache (CF-151) and measure it. (8) Audio/assembly check with installed tools only. (9) Scorecard, cleanup manifest, backlog/roadmap updates. (10) No commit.

**Assumptions.** Poly Haven / Poly Pizza CC0 assets downloaded without an account fall under the existing approved CC0-acquisition pattern (CF-140); Sketchfab requires an account and is treated as gated. Blender 5.2.3 portable is the only renderer; one worker. Disk gate: >50 GB free.

**Risks.** Candidate may not exist as CC0, leaving the brief's core goal unmet — that outcome is reported, not papered over. Import of third-party `.glb`/`.blend` is executing third-party data in Blender; assets are treated as untrusted input, opened headless with no auto-run scripts. Time: many deliverables, one render worker.

**Success criteria.** A licence row per candidate with exact URL. One terminal asset imported and visible in a matched before/after pair. Measurements recorded. Three templates render headless from parameters. Cache hit/miss measured. Every failure names its blocker. Nothing committed.

### AFTER

**Agent participation (actual).** **No subagents ran this session.** The brief permitted up to three; the work was short enough to run sequentially, and claiming otherwise would be false. All tool calls were made by the lead agent.

**Delivered.**

1. **Asset comparison** — `docs/reviews/ASSET_EVALUATION_2026-10-31.md`, ten candidates with URL, author, licence, size, geometry, materials, textures, import, quality, cost, adaptation. Sketchfab rows are marked as not re-verified because download is account-gated.
2. **Selected terminal and licence record** — Innerscene "Counter Pay", CC0, 204,384 B, sha256 `fd49c9304bc1a9e617203c64b7188608faabbc0855902e5b135311b2f9aa93b6`, row `receipt-pos-terminal-cc0` in `assets/manifest.json`; validator PASS (`assets=11 total_mb=23.3`).
3. **Working integration** — `tools/build_terminal_master.py` → `assets/models/terminal_master.blend`; `tools/shot_render.py` links the collection and instantiates it per shot. Method and checks: `docs/production/ASSET_INTEGRATION_2026-10-31.md`.
4. **Two art directions** — `render/stills/artA_premium_realistic.png`, `artB_premium_stylized.png`; A selected, B retained with its rejection reason.
5. **Before/after** — `render/comparison/baseline_artA_artB.png` plus mobile preview and screen crops; `docs/benchmarks/V5_STILL_BENCHMARK_2026-10-31.md`.
6. **Three operational templates** — `shots/t01_product_macro.json`, `t02_object_interaction.json`, `t03_cutaway.json`, each rendered at 1080×1920/32 spp (13.09–13.94 s), exposure gate PASS.
7. **Audio and assembly** — `tools/assemble_proof.py` → `render/assembly/assembly_proof.mp4` (11.0 s, 264 frames, 540×960 h264, 0.20 MB, built in 4.58 s, captions burned and inspected). **No narration and no music**: no TTS engine (`pyttsx3`, `espeak` absent) and no licensed track. Audio sync is therefore untested, not measured.
8. **Measurements** — stills 13.1–15.9 s at 1080×1920/32 spp; baseline 27.58 s; cache hit 0.90 s (−94 %); cleanup 22.37 MB; `render/` 47 → 25 MB; disk 80 GB free.
9. **Scorecard** — `docs/reviews/QUALITY_SCORECARD_2026-10-31B.md`, **68/100**, +10 over the previous version, with the two heaviest categories still capped (quality 3/5, animation 2/5).
10. **Cleanup** — `docs/reviews/cleanup_2026-10-31C/README.md`, 47 files / 22.37 MB, class-D only.
11. **Backlog and roadmap** — CF-150/151/154 done, CF-148/155 in progress, CF-153 ready; MASTER_PLAN and README rows updated.
12. **Changed files** — 7 modified, 5 new documents/dirs, 4 new tools, `shots/`; nothing committed.

**Defects found and fixed during the work (worth recording).**

- The GLB ships all four materials at the 0.8 grey default; without adaptation the hero prop renders as a grey blob with a blown top panel.
- The cache key initially omitted the master asset, then omitted the renderer source. Both omissions served a stale frame after a real change. The key now covers spec, template, master, renderer and Blender version.
- `ffmpeg` on this host cannot take a Windows drive path in `drawtext` (fontconfig is absent); the assembly script stages a relative font copy instead.

**Not delivered, with the exact reason.**

1. **A moving sequence or animation** — not produced. The three templates are stills; choreography (card insert, focus pull) is keyframe work not attempted here.
2. **A licensed hand** — not acquired. Every rigged hand found is Sketchfab CC BY behind an account, which needs the user's approval (CF-149).
3. **The 86.6k-triangle Sketchfab fallback** — not downloaded; account-gated and ~17× the geometry for an unverified look.
4. **TTS and music** — not obtained; no engine installed and no licensed track. CF-139 stays blocked.
5. **Cold/warm six-minute measurement** — not run; a still cache hit exists, a production-length warm run does not.
6. **Compositor** (CF-155) — not built; JSON spec, template hash and three variants exist.

**Repo state.** Branch `main`, nothing committed. `assets/` binaries remain git-ignored; `manifest.json` is tracked and now carries eleven rows. The terminal GLB is ignored by `assets/.gitignore` as designed.

**Next executable action:** cut a 4-shot sequence from the three templates with real keyframes and measure it end to end; the hand remains the largest single quality lever after that.

---

## 2026-10-31 · V5 animated production milestone

### BEFORE

**Prompt.** Turn the still templates into one 12–15 s animated educational sequence: four directed shots, keyframed JSON, geometry checks, bounded 9:16 preview, FFmpeg assembly, narration research without installs, comparison against V4 at equal display size, incremental-cache proof, adversarial review, docs.

**Verified first.** Working tree holds the uncommitted asset-first milestone (7 modified, 4 new tools, `shots/`, 5 new docs). Git clean point remains `b27a1e5`; nothing will be committed. Template + terminal master render from cache in 0.9 s; 5,100-tri terminal; 80 GB free.

**Plan.** (1) Extend `tools/shot_render.py` with bounded channels (`camera_location`, `marker`, `terminal_rot_z`, `card_pos`, `screen_events`, `packet_pos`), smooth easing, per-frame rendering and a `--check` geometry mode. (2) Four shot specs: macro push-in, card approach, contactless tap with screen state change, authorisation diagram with a travelling packet. (3) Geometry gate before any sequence. (4) 540×960 preview, one worker. (5) FFmpeg assembly. (6) Cache-invalidation test by editing one spec. (7) TTS availability/licence research only. (8) V4 vs V5 comparison at 540×960. (9) Reviews. (10) Docs, scorecard, cleanup, BACKLOG/MASTER_PLAN.

**Assumptions.** Windows SAPI voices exist but their licence for monetised narration is unverified, so audio stays blocked unless a permitted option is found without install. Low-resolution preview plus stills is the acceptance unit; premium quality is not claimed from a preview.

**Risks.** 300+ frames at 540×960 could exceed 20 min; bounded to 12–15 s total at 24 fps. New diagram geometry could look amateurish — it is checked by stills before sequence rendering. Cache design is the second real test of content addressing.

**Success criteria.** Four shots pass the camera-space check; one assembled 12–15 s 9:16 MP4 exists with recorded frame count; editing one shot leaves the other three cached; V4/V5 comparison recorded; every unbuilt item names its blocker; nothing committed.

### BEFORE — resumed 2026-11-01

**Prompt.** Same milestone, resumed in a new session: the four shot specs were edited at 23:22 after the adversarial reviews, but nothing was rendered or assembled against them. Finish the milestone — re-render, assemble, verify, review, document.

**Verified first.** `shots/v5_s*.json` mtimes are 23:22; `render/sequences/*.json` pointers are 23:20 and `render/assembly/v5_sequence.mp4` is 23:16, so all four renders and the assembled cut predate the fixes. `tools/shot_render.py` (22:51) is older than the specs, so only the specs invalidate their own keys. Total footage 13.0 s (3.0+3.5+3.5+3.0), 312 frames at 24 fps (72+84+84+72), 0.9 s of crossfades, 12.1 s expected final. Disk 63 GB free, above the 50 GB gate. Blender 5.2.3 at `tools/blender/blender-5.2.3-windows-x64/blender.exe`.

**Plan.** (1) Re-run the camera-space gate on all four specs. (2) Render all four shots, one worker, 540×960/16 spp. (3) Re-assemble with FFmpeg. (4) Extract verification frames and inspect them by eye. (5) Rebuild the V4/V5 comparison at matched display size. (6) Run technical, creative and educational adversarial reviews against the new frames. (7) Fix only material defects, retest inside the same budget. (8) Update MASTER_PLAN, BACKLOG, QA evidence, cleanup manifest and this log.

**Assumptions.** Existing review findings from 2026-10-31 stay valid for what they targeted; they are re-verified against the new frames rather than re-derived from scratch. The narration research in `docs/production/NARRATION_OPTIONS_2026-10-31.md` stands as the answer to brief item 8 — no TTS engine is installed and nothing was downloaded.

**Risks.** All four keys miss at once, about 12–13 min of single-worker render. A fix may have introduced a new framing defect the gate cannot see (the gate checks geometry, not composition), which is why the still inspection comes before the sequence review.

**Success criteria.** One ~12.1 s 9:16 MP4 exists whose frames come from the fixed specs; frame count and clock measured, not assumed; review findings either fixed with a measured retest or recorded as blockers; documents updated; nothing committed.
