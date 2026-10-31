# Script — "What Actually Happens When You Tap a Card"

Format: 9:16, 24 fps. Board: `docs/creative/STORYBOARD_CONTACTLESS.md`. Claims: `docs/research/contactless-claims/CLAIMS.md`.
Status: **40 s animatic built (CF-137) — `render/animatic/contactless_40s_animatic.mp4`. Not a final render: no audio, and S4–S6 are diagrams.**

## Audio status — read this before reviewing

**There is no narration audio. Every narration line below is a PLACEHOLDER for a voice track that has not been recorded.** No TTS model has been installed, no download has been approved, and no recording exists. The video is built to work **silently**: each beat carries a caption that states the claim the image cannot show. If the captions are removed, the film still teaches the mechanism but loses the two facts a viewer cannot infer — that the card has no battery, and that approval is not payment.

Do not describe this film as narrated. It is captioned.

## Claim map

Every narration line traces to a claim marked VERIFIED in the claim sheet. No line uses a PARTIAL claim, so no line needs the hedge wording.

| Beat | Line | Claim | Status |
|---|---|---|---|
| S1 | "This card has no battery. The reader's field powers it." | 1 — passive card powered by induction | VERIFIED |
| S2 | "The field induces a current in this coil. The chip wakes up." | 1, 2 — induction; 13.56 MHz ISO/IEC 14443 | VERIFIED |
| S3 | "The card adds a one-time code. It is good for this tap only." | 4 — one-time cryptogram per transaction | VERIFIED |
| S4 | "The request passes four stops: the shop, its bank, the network, your card issuer." | 6 — terminal → acquirer → network → issuer | VERIFIED |
| S5 | "Approved means the issuer reserved the amount. Nothing moved yet." | 7 — settlement follows authorisation; 8 — hold can differ | VERIFIED |
| S6 | "Later, clearing and settlement move the money. The tap only asked permission." | 7 — clearing and settlement | VERIFIED |

Claim 3 (tap distance around 4 cm) is used as a caption in S1, not a narration line — it is a fact about handling, not about mechanism.
Claim 5 (tokenisation) is **not used**. It is the only PARTIAL claim and the precise version would need a scheme-specific source. Omitting it costs nothing; overstating it would.

## Beats

Timings are for the 40 s cut. The rendered scene currently covers S1–S3 compressed into 10 s; see `docs/creative/STORYBOARD_CONTACTLESS.md` §8.

These are the **cues actually burned into the 40 s animatic**, in `render/captions/contactless_40s.srt`. They differ from the board's six-beat caption plan because the 3D material covers three beats in 10 s, not 17 s; the diagram segments carry the rest.

| # | Time | Caption | Beat | Narration (PLACEHOLDER, max 18 words) |
|---|---|---|---|---|
| 1 | 0.3–1.9 | NO BATTERY. NO CONTACT. | S1 | This card has no battery. The reader's field powers it. |
| 2 | 1.9–4.4 | HOLD IT ABOUT 4 CM | S1 | — |
| 3 | 4.4–6.2 | THE READER POWERS THE CARD | S2 | The field induces a current in this coil. The chip wakes up. |
| 4 | 6.2–9.7 | A ONE-TIME CODE | S3 | The card adds a one-time code. It is good for this tap only. |
| 5 | 10.3–13.0 | FOUR PARTIES, ONE MESSAGE | S4 | The request passes four stops: the shop, its bank, the network, your card issuer. |
| 6 | 13.0–16.7 | THE ROUTE TO YOUR BANK | S4 | The request is passed down that chain, one hop at a time. |
| 7 | 17.3–20.0 | THE DECISION IS OFF-SCREEN | S4 | Your card issuer makes the decision, off-screen. |
| 8 | 20.0–23.7 | NOBODY IN THE SHOP DECIDES | S4 | The terminal only asks. The issuer sends the answer. |
| 9 | 24.3–27.6 | APPROVED IS NOT PAID | S5 | Approved means the issuer reserved the amount. Nothing moved yet. |
| 10 | 27.6–31.7 | THE AMOUNT IS RESERVED | S5 | On a credit card, available credit falls; on a debit card, the funds are held. |
| 11 | 32.3–35.6 | SETTLEMENT MOVES MONEY LATER | S6 | Later, clearing and settlement move the money between the banks. |
| 12 | 35.6–39.5 | THE TAP ONLY ASKED PERMISSION | S6 | The tap was a question. Settlement moves the money later. |

## The line the film exists to deliver

> Approved is a hold, not a payment.

Everything before S5 sets it up; S6 gives it room. If a cut is needed, cut S2 or S4 — never S5.

## Prohibited language

Taken from the claim sheet's "Do not say" list. These must not appear in narration, captions, or on-screen text:

1. "The tap moves the money instantly."
2. "The card sends your PIN over the air."
3. "The card has a battery and broadcasts continuously."
4. "Contactless payments are anonymous."
5. "Approval means the payment is final."

Also prohibited by the board: "instant", "0.3 seconds", "bank-grade", "military-grade", "encrypted", "safe", "secure", and any claim about speed that is not a measured latency. No brand marks, no card-network logos, no padlock or shield imagery.

## Visual contract

- Green appears only on the terminal and the returning packet. Never on the card.
- The card's only lit element is the amber chip and, during the field, the cyan coil.
- The screen shows an amount line and an approval tick — no diegetic text, because no font is licensed or bundled and text at this size is illegible at 360 px.
- No money, coins, banknotes, or currency symbols. The film's argument is that value does not move at the tap; a flying coin would contradict the narration.
- No radio arcs from the terminal. Contactless is near-field inductive coupling, not a broadcast.

## Limitations, stated

- No narration recorded; no audio track of any kind, including music.
- Only 10 s of picture is rendered 3D. The remaining 30 s of the animatic are SVG diagrams with a moving marker, assembled by `tools/build_animatic.py`. Calling the animatic "the film" would overstate it.
- Captions **are** baked into the animatic (`render/captions/contactless_40s.srt`, 12 cues). No caption is attached to audio, because there is no audio.
- The 3D third still needs its 1080×1920 render and, for a full 3D version, a packet return leg. Both are scoped in `STORYBOARD_CONTACTLESS.md` §10 with measured costs.

## Factual review — 2026-10-31

Three statements were overstated and have been corrected before the animatic was built.

1. **"Approved means your bank set the money aside."** True for a debit card, where funds are held against a balance, but wrong for a credit card, where no money is set aside — *available credit* is held instead, and the credit limit itself is unchanged. The film cannot assume which card the viewer holds. Corrected to "the issuer reserved the amount", with the credit/debit distinction shown explicitly on screen in the hold diagram ("On a credit card this is a reduced credit limit, not money taken from an account").
2. **"The request is unique to this tap."** The *cryptogram* is single-use; the request is not a thing that can be unique. Softened to "good for this tap only", which is what claim 4 actually supports.
3. **"Later, the banks settle up."** "Settle up" reads as a bilateral payment between two banks on a known schedule. The claim sheet supports no timing and no netting mechanism. Corrected to "the banks settle the net difference", and no caption or diagram states a timeframe — there is no "T+1", no "next day", no "seconds" anywhere in the film.

Checked and left alone: 4 cm (claim 3), 13.56 MHz and ISO/IEC 14443 (claim 2), "no battery" (claim 1), "a hold, not a payment" (claims 7 and 8), "four stops in the message path" (claim 6). None of these overstates its source.

Deliberately still absent: tokenisation (claim 5, PARTIAL), any latency figure, any security or encryption claim, any brand mark.
