# Script — "What Actually Happens When You Tap a Card"

Format: 9:16, 24 fps. Board: `docs/creative/STORYBOARD_CONTACTLESS.md`. Claims: `docs/research/contactless-claims/CLAIMS.md`.
Status: **script locked for the 10 s scene; the 40 s cut is written but not rendered.**

## Audio status — read this before reviewing

**There is no narration audio. Every narration line below is a PLACEHOLDER for a voice track that has not been recorded.** No TTS model has been installed, no download has been approved, and no recording exists. The video is built to work **silently**: each beat carries a caption that states the claim the image cannot show. If the captions are removed, the film still teaches the mechanism but loses the two facts a viewer cannot infer — that the card has no battery, and that approval is not payment.

Do not describe this film as narrated. It is captioned.

## Claim map

Every narration line traces to a claim marked VERIFIED in the claim sheet. No line uses a PARTIAL claim, so no line needs the hedge wording.

| Beat | Line | Claim | Status |
|---|---|---|---|
| S1 | "This card has no battery. The reader's field powers it." | 1 — passive card powered by induction | VERIFIED |
| S2 | "The field induces a current in this coil. The chip wakes up." | 1, 2 — induction; 13.56 MHz ISO/IEC 14443 | VERIFIED |
| S3 | "The card adds a one-time code. The request is unique to this tap." | 4 — one-time cryptogram per transaction | VERIFIED |
| S4 | "The request goes to the merchant's bank, the card network, then your bank." | 6 — terminal → acquirer → network → issuer | VERIFIED |
| S5 | "Approved means your bank set the money aside. It has not moved." | 7 — settlement follows authorisation; 8 — hold can differ | VERIFIED |
| S6 | "Later, the banks settle up. The tap only asked permission." | 7 — clearing and settlement | VERIFIED |

Claim 3 (tap distance around 4 cm) is used as a caption in S1, not a narration line — it is a fact about handling, not about mechanism.
Claim 5 (tokenisation) is **not used**. It is the only PARTIAL claim and the precise version would need a scheme-specific source. Omitting it costs nothing; overstating it would.

## Beats

Timings are for the 40 s cut. The rendered scene currently covers S1–S3 compressed into 10 s; see `docs/creative/STORYBOARD_CONTACTLESS.md` §8.

| # | Time | Caption (max 6 words) | Narration (PLACEHOLDER, max 18 words) |
|---|---|---|---|
| S1 | 0.0–4.0 | NO BATTERY. NO CONTACT. | This card has no battery. The reader's field powers it. |
| S1b | 1.5–4.0 | HOLD IT ABOUT 4 CM | — |
| S2 | 4.0–10.0 | THE READER POWERS THE CARD | The field induces a current in this coil. The chip wakes up. |
| S3 | 10.0–17.0 | A ONE-TIME CODE | The card adds a one-time code. The request is unique to this tap. |
| S4 | 17.0–24.0 | THE DECISION IS OFF-SCREEN | The request goes to the merchant's bank, the card network, then your bank. |
| S5 | 24.0–32.0 | APPROVED IS NOT PAID | Approved means your bank set the money aside. It has not moved. |
| S6 | 32.0–40.0 | SETTLEMENT MOVES MONEY LATER | Later, the banks settle up. The tap only asked permission. |

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
- The rendered scene is a single continuous take. The 40 s cut requires re-timing to 960 frames plus a return leg on the packet, which is written but not built.
- Captions exist as timing data ready for burn-in; they are not baked into the current render.
