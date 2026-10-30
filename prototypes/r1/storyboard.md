# R1 Storyboard — Contactless card authorization

Format: 1080 × 1920 (9:16) · 3 static frames · shared palette and type scale.
Topic: what happens between a card tap and an approval.

## Frame sequence

| # | File | Beat | On-screen text | Visual |
|---|---|---|---|---|
| 1 | `frame-01-hook.svg` | Hook | "Your card was approved in 1.3 seconds." / "Here is what actually happened." | Card with NFC waves |
| 2 | `frame-02-process.svg` | Process | "Five systems, one tap." + five labelled nodes | Vertical flow with arrows |
| 3 | `frame-03-takeaway.svg` | Takeaway | "Authorization is not settlement." + two panels | Side-by-side contrast |

## Frame 1 — Hook

- Kicker: `MONEY · HOW IT WORKS`
- Headline: three lines, 108 px, accent on the number.
- Minimum reading time: 2.5 s.
- Purpose: promise a concrete reveal, not a topic label.

## Frame 2 — Process

Five nodes, in order:

1. **Card** — sends payment data over NFC
2. **Terminal** — builds the authorization request
3. **Acquirer** — the merchant's bank; routes the request
4. **Card network** — connects acquirer to issuer
5. **Issuing bank** — checks balance and fraud rules

Footer: "Approval or decline returns along the same path."

Deliberate simplifications: no tokenization, no 3-D Secure, no stand-in processing, no scheme fees. Those belong in the long-form version.

## Frame 3 — Takeaway

| Authorization | Settlement |
|---|---|
| Seconds | T+1 (varies) |
| Funds held | Funds move |
| No money moves yet | Batch clearing |
| Can be reversed | Interchange paid |

Closing line: "A hold reserves money. Settlement moves it."
Fine print: "Educational simplification. Timing varies by network and region."

## Design system

| Token | Value | Use |
|---|---|---|
| Background | `#0B1020` | All frames |
| Surface | `#121A2B` | Cards and panels |
| Border | `#22304A` | 3 px strokes |
| Text | `#E6EDF7` | Headlines and body |
| Muted | `#9FB0C7` | Secondary text |
| Accent | `#4C8DFF` | Primary emphasis |
| Cyan | `#22D3EE` | Flow and response |
| Amber | `#F5B547` | Decision point and hold |

Type: system stack only — `'Segoe UI', 'Inter', Arial, sans-serif`.
Scale: 108 / 92 / 68 / 62 / 44 / 42 / 40 / 36 / 32 / 30 / 26 px.
Safe area: 96 px side margins; top 230 px; bottom 346 px.

## Mobile check

At 360 px display width the frame scales by 1/3. Smallest body text is 30 px → 10 px effective, which is below comfortable reading. Two mitigations apply:

- Body-size text (30 px) is used only for secondary descriptors that also appear in narration.
- Primary claims are never below 40 px (≈13 px effective).

This is a known limitation of a 1080-wide canvas with dense diagrams; R2 must not add more small text.
