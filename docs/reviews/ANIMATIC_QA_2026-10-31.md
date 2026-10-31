# Animatic QA — 2026-10-31

Two independent reviewers examined the 40 s animatic read-only, one for factual accuracy and one for pipeline correctness. Neither was shown the other's findings. This file records what they found and what was done about it. Dispositions are `FIXED`, `ACCEPTED` (with the reason) or `OPEN`.

**This is a review of an animatic, not of a finished film.** No audio exists. S4–S6 are diagrams.

---

## 1. Factual review

Verdict returned: **SCRIPT NEEDS FIXES — 1 BLOCKER.**

### BLOCKER

**B1 — the hold diagram was wrong for credit cards.** `hold.svg` said `YOUR AVAILABLE BALANCE`, `still yours — just not spendable`, and `a reduced credit limit`. A credit card has no balance being held, and an authorization does not reduce the credit limit — it reduces *available credit*. "Still yours" is false when the held amount is borrowing capacity, not funds.

`FIXED`. The diagram now reads `AVAILABLE TO SPEND`, `reserved, not yet charged`, and `On a credit card this reduces available credit, not money taken from an account.` The narration line became "On a credit card, available credit falls; on a debit card, the funds are held." The statement `the issuer reserved the amount` — which the reviewer identified as correct for both card types — was already in use and is unchanged.

### SHOULD-FIX

| # | Finding | Disposition |
|---|---|---|
| S1 | The claim map and production board still carried the pre-review lines, so the review's claim to have corrected them was itself false | `FIXED` — 3 claim-map lines and 7 board lines replaced |
| S2 | "FOUR PARTIES, ONE MESSAGE" miscounts. The four-party model is cardholder, merchant, acquirer, issuer; the network is the scheme, not a party, and the film's four omit the cardholder. "One message" also contradicted the REQUEST/RESPONSE pair on screen | `FIXED` — caption is now `FOUR STOPS, ONE REQUEST`, which describes the message path the diagram actually shows |
| S3 | "NOBODY IN THE SHOP DECIDES" is an absolute the source does not support: terminals can decline locally and can be configured for offline authorisation | `FIXED` — caption is now `THE TERMINAL ONLY ASKS`; narration "The terminal only asks. The issuer sends the answer." |
| S4 | Netting and batching are not in the claim sheet. `settlement.svg` drew six arrows converging on a `NET` hub and captioned it "batched and netted" | `FIXED` — the hub and the six arrows are gone. The scene is now two entities and one link labelled `settles later`, which is what claim 7 supports. The word "netted" is gone from script and picture |
| S5 | "Settlement is the answer arriving late" conflates the authorization response with interbank settlement, and "late" is a timing characterisation | `FIXED` — "Settlement moves the money later." |
| S6 | The board's six-caption plan contradicted the 12-cue SRT without saying which was authoritative | `FIXED` — the board now marks the six-caption plan as the unbuilt 3D cut and names the SRT as what is burned in |
| S7 | "your bank" used as a synonym for issuer, which is ambiguous for a card issued by a bank you do not deposit with | `FIXED` — caption `THE ROUTE TO THE ISSUER`; the settlement diagram says `your card issuer` |

### NITPICK

| # | Finding | Disposition |
|---|---|---|
| N1 | "the merchant's bank" for acquirer — an acquirer may be a non-bank processor | `FIXED` — `the merchant's provider` in all three diagrams |
| N2 | Board claimed terminal approval and the app's pending line are "the same event" | `FIXED` — "two views of the same authorization" |
| N3 | Board's S4 cause read as three direct recipients | `FIXED` — "the terminal sends the request to the acquirer, which routes it through the network to the issuer" |
| N4 | Green appeared on the issuer box and the settlement arrows, breaking the film's own rule that green marks approval at the terminal | `FIXED` — issuer box takes the cyan signal hue; settlement arrows are steel |
| N5 | "NO CONTACT" can be misread as no physical contact | `ACCEPTED` — "contactless" is the industry term and the next cue, `HOLD IT ABOUT 4 CM`, resolves it within 2 s. Changing it would cost the only line that names the product category |

### Clean categories

Numbers and units (4 cm, 13.56 MHz, ISO/IEC 14443), approval finality (nothing claims the payment is final or that money moved), settlement timing (no T+1, no "seconds", no "instant"), and the prohibited-language list — all clean in visible text.

## 2. Technical review

Verdict returned: **PIPELINE NEEDS FIXES — 1 BLOCKER.**

### BLOCKER

**Segment A's frame count was whatever existed on disk, and the 960-frame contract was never asserted.** `segment_3d` had no `-frames:v`, and `main()` only printed the probe. The repository plans a 960-frame render of the same scene into the same `v4final_f*` prefix; dropping it in would have produced a 70 s file with every caption after 10 s mistimed — exit code 0.

`FIXED`. `SEG_A_FRAMES = 240` pins the read, every encode is verified by packet count before it replaces its target, and `main()` refuses to succeed unless the final probes as exactly 960 frames and 40.000 s.

### SHOULD-FIX

| # | Finding | Disposition |
|---|---|---|
| T1 | Chrome was trusted on exit code alone; on Windows it can hand off to a running instance and exit 0 without writing, and the previous raster would be reused silently | `FIXED` — the old raster is deleted before capture, a throwaway `--user-data-dir` is used, and the result is verified by PNG IHDR dimensions |
| T2 | A crash during the final encode left a truncated file where a good deliverable had been | `FIXED` — every encode writes `.tmp` and `os.replace`s on success |
| T3 | Chrome was probed only after segment A had already been encoded | `FIXED` — checked before any encode |
| T4 | SRT timings and segment durations had no shared source and no validation | `FIXED` — `check_captions` parses the SRT and refuses any cue that crosses a segment boundary. Verified: 12 cues, 0 problems |
| T5 | Stale QA captures in the delivery folder showed a build that no longer existed | `FIXED` — deleted; regenerated from the shipped file |

### NITPICK

`run()` now names the failing step. Chrome candidates include `LOCALAPPDATA`. Every subprocess has a timeout. The output constant is `OUT_VIDEO`, not `FINAL` — the file is an animatic and its own name should say so.

`make_dot()` still writes into `render/scenes/`. `ACCEPTED`: the dots are build inputs, are regenerated every run, and are named by colour so two segments sharing a colour share one asset, which is correct.

`-loglevel error` is kept. `ACCEPTED`: failures still surface through the exit code, the named step and the stderr tail; the quieter default keeps a successful build readable.

## 3. What the reviewers could not establish

- Determinism was **inferred**, not hash-proven: the reviewer did not run a second build. PNG chunks carry no `tIME`, and the MP4 tags carry no `creation_time`, so a repeat build on the same host should be byte-identical — but Chrome version, the system font set and the ffmpeg build are all unpinned, so that holds only on this machine.
- Neither reviewer decoded the shipped MP4's pixels end to end. Visual checks were made on extracted frames.

## 4. Reassessment after the fixes

Rebuilt after every `FIXED` item above. The rebuild itself found a new defect, which is recorded here rather than smoothed over.

| Run | Card-region curve error | Band | Whole frame | Flicker | Verdict |
|---|---:|---:|---:|---:|---|
| Before the reframe | 21.0 % | 25 % | 5.18 % | 0.00006 | PASS |
| After the reframe | **26.3 %** | 25 % | 6.81 % | not re-read | **FAIL on `region 'card'`** |

**Cause.** Correcting the end framing (the card was being cut by the left edge for the last ~10 frames) moved the camera's end pose, which changes how the key light's specular sweeps across the card face. `curve_at()` models light-to-subject distance only; it has no view-dependent term, so a view-dependent reflection shows up as model error.

**This is not a visible defect.** The whole-frame curve is within 6.8 %, the flicker index is low, and nothing fades or flickers. The card brightens gradually as the camera moves, which is physically correct. What failed is the *model's* coverage of that brightening, not the picture.

**Not fixed by widening `CURVE_MAX`.** Doing so would make the gate pass by definition, which is the one thing a gate must not do. The band stays at 0.25.

**Open. Two candidate fixes, neither applied:**

1. **Make the model honest.** Add a view-dependent term to `curve_at()` — project the key light's reflection vector against the camera and weight it. Correct, and more work than the animatic milestone justifies.
2. **Make the card more diffuse.** Raise `CardBody` roughness and drop its `spec`, so the measurement's Lambertian assumption holds. Cheaper, but it flattens the card's sheen, which is part of the premium look the scene is trying to earn.

Until one is chosen, the 10 s 3D segment has a known, quantified, non-visual QA failure and must be described that way — not as a pass.
