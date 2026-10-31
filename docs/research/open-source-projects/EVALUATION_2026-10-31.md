# Blender tooling evaluation — 2026-10-31

Supersedes nothing. The 2026-10-30 assessment in [`README.md`](README.md) stays as the first pass; this file adds capability detail, three candidates the first pass missed, and a security read. No repository was cloned, installed, or executed.

Confidence tags: **VERIFIED** (repository contents or licence file read directly) · **DOCUMENTED** (README/docs read) · **INFERRED** · **UNKNOWN**.

---

## 1. Question

Does any public Blender project let an agent-driven workflow produce an editable `.blend` with real assets, animation, cameras, lighting and a multi-shot timeline, on Windows, with Blender 5.2 — and at what licence and security cost?

## 2. Candidates

| # | Project | Stars | Licence | Active | Writes `.blend` | Animation | Cameras | Lighting | Multi-shot | Executes LLM bpy | Win | Confidence |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | [ifBars/blender-agent-studio](https://github.com/ifBars/blender-agent-studio) | 98 | MIT | yes (2026-10-30) | yes | yes | yes | yes | unknown | yes (no generic Python tool) | yes | VERIFIED |
| 2 | [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | 32,898 | MIT | yes (2026-10-29) | yes | yes | yes | yes (HDRI) | unknown | yes, **by default** | yes | VERIFIED |
| 3 | [nishit47/Blender-Pre-vis-Pipeline](https://github.com/nishit47/Blender-Pre-vis-Pipeline---Screenplay-to-Animatic) | 0 | **none** | stale (2026-09-26) | yes | yes | yes | unknown | yes | yes | unknown | VERIFIED |
| 4 | [DvaitAI-tech/anim-studio](https://github.com/DvaitAI-tech/anim-studio) | 3 | MIT | stale (2026-06-30) | unknown | yes | yes | unknown | yes | yes | yes | DOCUMENTED |
| 5 | [Mnehmos/semantic-video-studio](https://github.com/Mnehmos/semantic-video-studio) | 0 | MIT | abandoned (one-day repo) | no evidence | yes | yes | yes | yes | yes | yes | VERIFIED |
| 6 | [danromik/smoothie](https://github.com/danromik/smoothie) | 2 | GPL-3.0 | stale (2026-04-15) | unknown | yes | unknown | unknown | unknown | yes, review-gated | yes | DOCUMENTED |
| 7 | [shefq/blendrelay-mcp](https://github.com/shefq/blendrelay-mcp) | 13 | MIT | yes (2026-10-29) | yes | yes | yes | yes | unknown | yes, AST blocklist | yes | DOCUMENTED |
| 8 | [carlosh7/blender-mcp](https://github.com/carlosh7/blender-mcp) | 17 | MIT | stale (2026-08-29) | yes | yes | yes | yes | unknown | yes, AST blocklist | yes | VERIFIED |
| 9 | [RFingAdam/mcp-blender](https://github.com/RFingAdam/mcp-blender) | 33 | **AGPL-3.0** | yes (2026-10-23) | yes | yes | yes | yes | unknown | unknown | yes | VERIFIED |
| 10 | [blender.org lab MCP](https://projects.blender.org/lab/blender_mcp) | 36 | GPL-3.0 | yes (v1.0.3, 2026-09-11) | via executed code | unknown | unknown | unknown | unknown | yes, **no guards** | unknown | VERIFIED |

**Multi-shot timeline is unproven for all ten.** No candidate documents a working sequencer/timeline workflow on Blender 5.2. Any plan that assumes one is an assumption, not a finding.

## 3. Security read — the deciding factor

Every candidate that can build a scene does it by running Python inside Blender. That is the product. The differences are only in how much code they let a model write and what stands between that code and the machine:

- **blender.org official MCP** — the project's own page states it runs LLM-generated code "without any guards" and recommends a VM. This is the clearest warning in the set and it comes from the vendor.
- **ahujasid/mcp-for-blender** — `execute_blender_code` is the default; a blocklist exists only behind `BLENDER_MCP_SAFE_MODE=1`. Anonymous telemetry (install ID, tool names, OS, Blender version) is on until opted out.
- **blendrelay / blender-mcp-ultra / mcp-blender** — AST blocklists (80-ish patterns), localhost binding, tokens, auto-undo. Better than nothing, and weaker than a sandbox: a blocklist is a denylist, and denylists fail open on anything not imagined.
- **blender-agent-studio** — ships an MCP with no generic arbitrary-Python tool; still runs generated scripts inside Blender, and Blender's Python is not sandboxed.
- **smoothie** — the only candidate with human review before execution as the default, at the cost of requiring a Claude subscription or API key.

Consequence for this repository: none of these qualifies for the publish path, and none should run on the corporate-managed host with network access. An agent tool that writes scene code is acceptable only in an isolated VM or container with no credentials and no network, and only after a named G6-style approval. That is a decision for the user, not something this evaluation can grant.

## 4. Licence read

- MIT — candidates 1, 2, 4, 5, 7, 8. Commercially usable; keep the copyright notice.
- **AGPL-3.0 — candidate 9.** Its README still claims MIT; the `LICENSE` file is AGPL-3.0-or-later (relicensed at v0.4.0). Read the file, not the bullet. AGPL is a network-copyleft obligation; avoid unless the user accepts it deliberately.
- GPL-3.0 — candidates 6 and 10. Fine to run as a local tool; obligations attach if redistributed.
- **No licence — candidate 3.** No licence means no rights. Rejected regardless of features.

## 5. Verdicts

**Shortlist**

1. **ifBars/blender-agent-studio** — the only candidate built for Claude Code, stating Blender 5.2 and a saveable `.blend` plus emitted Python, with no API key and no paid service. Risks: 98 stars, three months old, multi-shot unknown, and its no-generic-Python tool is a design choice rather than a sandbox.
2. **shefq/blendrelay-mcp** — typed tools covering animation, cameras, lighting and checkpoints on the open `.blend`, documented Claude Code wiring and Windows paths. Risks: three months old, 13 stars, and its docs are near-identical to candidates 8 and 9, so their "tool count" claims are one project's evidence repeated, not three independent proofs.
3. **ahujasid/mcp-for-blender** — the most battle-tested, MIT, Windows installer, asset libraries and render-based self-check. Risks: arbitrary Python by default, telemetry on by default, and a mandatory `uv` dependency.

**Rejected**

- `nishit47/…` — no licence.
- `RFingAdam/mcp-blender` — AGPL-3.0 against a README that says MIT; a licence trap is disqualifying on its own.
- `Mnehmos/semantic-video-studio` — one-day repository, no evidence it saves a `.blend`.
- `danromik/smoothie` — requires a paid inference path and is stale.
- `DvaitAI-tech/anim-studio` — stale, two conda environments that cannot co-install, and it pulls in the unsafe default from candidate 2.
- `carlosh7/blender-mcp` — stale since August, and its README disagrees with itself on tool count.
- `blender.org/lab` — official, but the vendor itself says the code path has no guards; it is a research preview, not a production tool.

## 6. What this changes

Nothing about the architecture. `MASTER_PLAN.md` §3 principle 1 already says the production render path is fixed code driven by JSON, not an agent. This evaluation supports that principle rather than weakening it:

- An agent tool can shorten **authoring** — building a `.blend`, trying a camera, checking a framing.
- It must not sit in the **render** path, because determinism, licensing and reproducibility are the things a code-generating tool makes worst.
- The measurable gain from these tools is unverified. No candidate has a published comparison showing it beats a hand-written `bpy` script on a real scene.

The recommendation is therefore: **evaluate one candidate (blender-agent-studio) in an isolated environment, if and only if the user authorises it** — see `BACKLOG.md` CF-143. Until then the deterministic scripts stay the only path.

## 7. Open questions

1. Blender 5.2 compatibility is the projects' own claim; none was tested here.
2. Multi-shot timeline support is unverified everywhere.
3. No candidate publishes a quality or time comparison against hand-written `bpy`.
4. Telemetry opt-out has not been verified beyond the README statement for candidate 2.
