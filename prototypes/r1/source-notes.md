# R1 Source Notes — claims and simplifications

Scope: three static frames. No narration. Claims are deliberately conservative.

## Claims used on screen

| Claim | Basis | Confidence |
|---|---|---|
| A contactless tap sends payment data to a terminal | EMV contactless standard behaviour | High |
| The terminal builds an authorization request | Standard acquirer processing | High |
| The acquirer is the merchant's bank and routes the request | Standard four-party model | High |
| A card network connects acquirer and issuer | Four-party model | High |
| The issuer checks balance/credit and fraud rules | Standard issuer behaviour | High |
| Authorization is separate from settlement | Clearing and settlement are distinct phases | High |
| Settlement commonly occurs around T+1 | Region-dependent; varies by network and scheme | Medium — hedged on screen |
| A hold can be reversed | Voids, reversals, and expiries exist | High |

## Deliberate omissions

- Tokenization and the role of the token service provider.
- 3-D Secure / strong customer authentication.
- Stand-in processing when the issuer is unreachable.
- Interchange economics and scheme fees (named only as "interchange is paid").
- Regional instant-settlement schemes.

These are long-form material, not Short material.

## Language and legal care

- No bank, network, or card brand is named or depicted. No logos, no trade dress.
- "1.3 seconds" is illustrative, not a measured statistic for any specific transaction. It is presented as a narrative device; the long-form script must either measure it or hedge it.
- "T+1" is hedged on screen with "timing varies by network and region".
- No claim about fees, interest, or consumer protection is made.

## Asset and licence status

- All geometry is authored SVG. No external fonts, images, icons, or downloaded assets.
- No third-party licence obligations attach to these files beyond the repository's own licence.
- Palette and type are defined inline; nothing is fetched at render time.

## Open questions before publishing

1. Is the illustrative "1.3 seconds" acceptable, or should it be replaced with a measured/hedged value?
2. Should the long-form version name the four-party model explicitly?
3. Which region's settlement timing is the default audience assumption?
