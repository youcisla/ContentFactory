# R1 / R2 Review and Scorecard

Date: 2026-10-30. Subject: static SVG visual language (R1) and 12-second animated prototype (R2).
Self-review, not independent validation.

---

## 1. What was built

| Item | Path | Status |
|---|---|---|
| Hook frame | `prototypes/r1/frame-01-hook.svg` | Verified structurally + visually |
| Process frame | `prototypes/r1/frame-02-process.svg` | Verified structurally + visually |
| Takeaway frame | `prototypes/r1/frame-03-takeaway.svg` | Verified structurally + visually |
| Storyboard | `prototypes/r1/storyboard.md` | — |
| Source notes | `prototypes/r1/source-notes.md` | — |
| Validator | `prototypes/r1/validate_r1.py` | PASS (exit 0) |
| Animated prototype | `prototypes/r2/index.html` | Verified structurally + 4 states captured |
| R2 validator | `prototypes/r2/validate_r2.py` | PASS (exit 0) |
| Previews | `prototypes/r1/previews/`, `prototypes/r2/previews/` | PNG, Chrome headless |

## 2. Tests actually executed

| Test | Result |
|---|---|
| R1 XML parse, viewBox, safe area, palette, font stack, min font size | **PASS** (3 frames, 40 text elements) |
| R1 visual render (Chrome headless, 1080×1920) | **PASS** after one fix |
| R2 structure (duration, 5 nodes, numbering, reduced-motion, external refs) | **PASS** |
| R2 state capture at 2 s / 6 s / 9.8 s | **PASS**, distinct hashes |
| R2 reduced-motion composition | **PASS** |
| Rust build or benchmark | **NOT RUN** — no download authorised |

## 3. Defects found and fixed during review

| # | Defect | Evidence | Fix |
|---|---|---|---|
| D1 | Text with colour-only classes fell back to serif | Preview 1 rendered "1.3 seconds." in serif | Global `text{font-family:…}` in all three SVGs |
| D2 | Takeaway panels had ~200 px dead space | Preview 3 | Panel height 560 → 470, closing text moved up |
| D3 | Headless screenshots froze at t=0; three "different" captures were byte-identical | SHA-256 equal | Added `?t=` Web Animations seek, then found animations were disabled entirely |
| D4 | Reduced-motion layout placed the takeaway in normal flow, overlapping the title | `reduced` capture | Takeaway becomes the final composition; no overlap |
| D5 | Packet dot travelled through node text | `motion-6` capture | Added a left rail; dot moved to x=60 |
| D6 | Takeaway scrim was translucent; flow text ghosted through | `motion-9.8` capture | Solid background |

D3–D6 are the reason visual capture exists: none was detectable from source review alone.

## 4. Scores

Separated deliberately: design completeness, verified functionality, production readiness.

### Weighted score (design + prototype)

| Criterion | Weight | Score | Weighted | Basis |
|---|---:|---:|---:|---|
| Educational accuracy | 20 | 4.5 | 18.0 | Claims conservative; "1.3 s" flagged as illustrative |
| Visual quality | 20 | 4.0 | 16.0 | Strong hierarchy, consistent system; diagrammatic, not cinematic |
| Resource efficiency | 20 | 4.5 | 18.0 | No installs; <3 MB of authored assets; Chrome only |
| Cost efficiency | 15 | 5.0 | 15.0 | Zero variable cost |
| Automation | 10 | 3.5 | 7.0 | No renderer or pipeline yet; manual composition |
| Maintainability | 10 | 4.0 | 8.0 | Single-file artifacts, validators; no build step |
| Compliance | 5 | 4.5 | 4.5 | No external assets or brands; disclosure not yet relevant |
| **Total** | | | **86.5** | Promising |

### Verified functionality: 4/5

All executed tests pass. Missing: a frame-by-frame render and encode test, which is blocked.

### Production readiness: 2/5

No rasteriser binary, no encoder loop, no audio, no captions, no QA gates implemented.

## 5. Adversarial pass A — engineering

| # | Finding | Response |
|---|---|---|
| A1 | Browser playback is not rendering | Stated explicitly in R2 README; no claim of video feasibility |
| A2 | 12 s loop with CSS timing will not survive conversion to 30 fps without a frame-accurate seek | Accepted; `?t=` gives frame-accurate stills, not an encoder |
| A3 | Validators check structure, not pixels | True; pixel checks were manual via rendered PNGs |
| A4 | Reduced-motion path was broken and only found by accident | Added explicit capture and a fix; now part of the test set |
| A5 | Two languages are already in play (Python validators, HTML/CSS) | Justified: validation only, no runtime dependency |
| A6 | Rail dot is decorative, not data-bearing | Correct; it indicates flow order only |

## 6. Adversarial pass B — educational and business

| # | Finding | Response |
|---|---|---|
| B1 | "Approved in 1.3 seconds" is a hook, not a fact | Flagged in source notes; must be replaced or hedged before publishing |
| B2 | Five-node flow omits tokenization and 3-D Secure | Deliberate for a 40 s short; long-form must include them |
| B3 | Dense descriptors at 29–30 px are small on a phone | Documented in storyboard; primary claims stay ≥40 px |
| B4 | Visual language is competent but not distinctive | True. Differentiation must come from diagrams and pacing, not decoration |
| B5 | No narration written, so timing is unvalidated against speech | Accepted; R5 will fit narration to the beat map |
| B6 | Reuse potential is high for the card/flow pattern, low for bespoke topic art | Each new topic needs 1–2 new templates; that is the intended cost |

## 7. Remaining limitations

1. No pixel-diff regression test.
2. No measured render throughput.
3. No export path to video.
4. Font rendering depends on the host's installed Segoe UI; cross-machine determinism unverified.
5. The 1.3-second figure is illustrative.

## 8. Gate status

| Gate | State |
|---|---|
| G1 claims | Not started — no narration yet |
| G2 script | Not started |
| G3 storyboard | **Prototype only** — human approval of the visual language is the next decision |
| G4 render QA | Not applicable at prototype stage |
| G5 publish | Not applicable |

## 9. Next tasks

1. Human approval or rejection of the visual language (blocks R3/R4).
2. Approve the `resvg` download so B0 can run.
3. Only then build the frame generator and encoder loop.
