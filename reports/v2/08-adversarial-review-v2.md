# 08 — Adversarial Review v2

Stance: find the reason this recommendation fails before you spend a week building it. Findings are ordered by how much they would hurt.

---

## 1. Findings

### A1 — The highest-scoring architecture is the one with the worst failure mode (High)

D scores 83.5, but every video would depend on a rented machine, a network upload, and a vendor's price. A good score is an average; a single point of failure is absolute.

**Change made:** `02` §6 recommends A as the spine and D for ≤10 % of runtime, not D outright. Composite ≈86.

### A2 — "2.5D is enough" is a creative bet, not an engineering fact (High)

The recommendation assumes diagrams and typography carry educational value better than 3D spectacle. That is true for *concepts* (interchange, authorisation flow) and false for *spatial* topics (how a chip's antenna works, how data centres are laid out).

**Unresolved by design.** The topic mix decides. If more than ~30 % of episodes need spatial explanation, the weighting should shift toward D-as-primary.
**Evidence that would settle it:** 10 proposed episode titles, classified spatial vs conceptual.

### A3 — Motion Canvas is not a safe spine (Medium)

Its latest release is **v3.17.2, published 2024-12-14**, despite repository activity. Two years without a release on a Node 26 runtime is a compatibility risk.

**Change made:** Motion Canvas is optional authoring only; the spine is a stdlib Python SVG generator + resvg, which has no framework lifecycle.

### A4 — Kokoro is stale (Medium)

Last push 2025-08-06 — ~14 months. Apache-2.0 weights remain usable forever, but bugs will not be fixed.

**Change made:** Kokoro demoted to fallback; Chatterbox-Turbo (active, MIT) is primary.

### A5 — Chatterbox's CPU claim is a vendor claim (Medium)

"3× faster than realtime on 8 CPU cores" was read from the README. This laptop has 12 cores (2 of them low-power). Real throughput could be half that.

**Mitigation:** R5 gate is a listen test plus a measured realtime factor; fallback chain defined (Kokoro → paid API).

### A6 — Vast.ai prices are live, therefore unstable (Medium)

$0.108/h today does not bind tomorrow, and marketplace hosts are interruptible. Budgeting at the measured number without a margin is naive.

**Mitigation:** `05` uses $0.11–0.27/h and a 2× sensitivity case; R8 requires idempotent jobs, so an interrupted render is retryable.

### A7 — YouTube API may restrict unaudited projects (Medium)

New Google Cloud projects often upload via API into a restricted/private state until audited. If true here, "automated publishing" is not available on day one.

**Mitigation:** manual upload for the first ten videos; verify audit status in the console before writing the uploader. Marked [I], not verified.

### A8 — Pexels/Pixabay licences were not read (Medium)

Both returned HTTP 403 to the audit fetch. Their terms are widely commercial-friendly but not verified in this pass.

**Mitigation:** treat stock footage as optional; prefer CC0 (Poly Haven, Kenney) and authored graphics, where the licence is unambiguous.

### A9 — Piper's licence changed from MIT to GPL-3.0 (Medium)

The archived `rhasspy/piper` was MIT; the maintained successor `OHF-Voice/piper1-gpl` is **GPL-3.0**. Anyone copying the old assumption would be wrong.

**Mitigation:** `04` records it; Piper is not the default. Local use is unaffected; distributing a derivative is not.

### A10 — The obvious publishing choice would have failed silently (Medium)

Postiz is the most popular self-hosted scheduling tool, and its OSS tree contains **no YouTube provider**. Adopting it would have produced a working app that cannot publish the only platform that matters here.

**Change made:** `03` rejects Postiz for this workload; direct API recommended.

### A11 — B (Manim + Eevee) cannot sustain a library on this disk (Medium)

15–40 GB per long-form episode against 58.2 GB free means one episode in flight, then cleanup. That is a production ceiling disguised as a render choice.

**Change made:** efficiency score 2.5; B demoted to secondary.

### A12 — Human review is the true bottleneck and nothing here reduces it (High)

At 3–6 hours per long-form, output is capped at ~2 long-form videos per month regardless of architecture. Every architecture scores similarly because compute is not the constraint.

**Mitigation:** none in this plan. Templates and checklists reduce per-video review over time, but the first 10 videos will be slow. Planning for higher throughput is self-deception.

### A13 — "Zero idle" eliminates every self-hosted publisher (Low)

Postiz, OpenPost, and Mixpost all require Postgres/MySQL and Redis running continuously. That directly contradicts the stated preference.

**Change made:** direct API recommended; self-hosted publishers deferred.

### A14 — Determinism claim depends on pinning the rasteriser (Low)

Even with identical SVG, text shaping and anti-aliasing can differ across resvg versions or font availability. "Byte-identical re-render" is only true if the binary, fonts, and version are pinned.

**Mitigation:** R3 acceptance requires pinning resvg version and bundling fonts; hash comparison is the test.

---

## 2. Weak assumptions ranked

| # | Assumption | Confidence | If wrong |
|---|---|---|---|
| 1 | Vector/diagram style is sufficient for the topics | Medium | Move to D-primary |
| 2 | Render ≤ 3 min for 10 s at 1080×1920 | Unknown | B0 answers it |
| 3 | Chatterbox CPU speed acceptable | Medium-low | Kokoro, then paid TTS |
| 4 | Cloud GPU is reliable enough for scheduled production | Medium | Keep 3D one-off, manual |
| 5 | YouTube API can upload without audit friction | Medium | Manual upload |
| 6 | Review takes 3–6 h per long-form | Low | Budget blows up |
| 7 | Disk stays above 15 GB with cleanup discipline | Medium | External SSD required |
| 8 | CC0 asset quality is sufficient without stock footage | Medium | Licence review for stock |

## 3. What evidence would change the recommendation

| Evidence | New recommendation |
|---|---|
| B0 fails (>10 min or >3 GB RAM) | Move to D-primary or C, accept cloud dependency |
| B0 passes but you reject the visual style | Try B (Manim) before D; 3D becomes required |
| Chatterbox measures < 1× realtime | Kokoro, then Azure/ElevenLabs |
| Policy forbids installs | Cloud-only pipeline; local device is text editing only |
| >30 % of planned episodes are spatial | D-primary with A for text/diagrams |
| YouTube API audit blocks uploads | Manual upload permanently; publisher tooling unnecessary |
| Disk drops below 15 GB before R4 | External SSD or cloud storage is a prerequisite |
| Review consistently exceeds 6 h/long-form | Reduce episode length to 4–5 min, or accept 1 video/month |

## 4. Plan-quality assessment (subjective)

| Aspect | v1 | v2 | Basis |
|---|---:|---:|---|
| Scope and deliverables | 5 | 5 | Complete, versioned |
| Safety and reversibility | 4 | 5 | B0 envelope explicit |
| Hardware grounding | 2 | 5 | Measured, unchanged facts |
| Dependency and licence verification | 2 | 5 | Live API + licence files |
| Architecture comparison | 2 | 5 | Four options, same artefact, same rubric |
| Cost realism | 3 | 5 | Measured GPU price replaces guess |
| Resource modelling | 2 | 4 | Estimated, labelled |
| Adversarial honesty | 3 | 5 | Failure modes named, not smoothed |
| Actionability | 3 | 5 | One benchmark, one decision |
| Verification completeness | 2 | 4 | Pexels/Pixabay and YouTube audit open |
| **Average** | **2.8** | **4.8** | Editorial judgment only |

v2 is graded higher because it is better evidenced, not because the system is closer to working. No frame has been rendered.

## 5. Residual uncertainty

1. B0 performance — unknown until run.
2. Corporate policy — external.
3. TTS realtime factor on this CPU.
4. YouTube API audit behaviour for a new project.
5. Pexels/Pixabay terms.
6. Whether the visual style is acceptable to the audience.
7. Review time per finished minute in practice.

## 6. Bottom line

The recommendation survives adversarial review **conditionally**: it is the lowest-risk path that still produces published video, and its one load-bearing assumption is cheap to test. It would not survive if 3D is non-negotiable or if the corporate device is off-limits — both are decisions for you, not findings for me.
