# Contactless card claims — verified sheet

Purpose: source-checked claims for a 30–45 second educational Short on contactless card payments.
Date: 2026-10-31.
Rule: a claim may be used in the script only if this sheet marks it **VERIFIED** or **PARTIAL**. A PARTIAL claim must use the precise wording in "Safe wording", not the broad version.

| # | Claim | Source | Verbatim quote (max 25 words) | Publisher | Date | Status |
|---|---|---|---|---|---|---|
| 1 | A contactless card has no battery; the reader's electromagnetic field powers the chip during a tap. | https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/DigitaleGesellschaft/NFC_Systeme_im_Praxiseinsatz.pdf?__blob=publicationFile&v=1 | "nicht über eine eigene Stromversorgung verfügt (sondern stattdessen über elektromagnetische Induktion ihre benötigte Energie aus dem EM Feld des Lesers bezieht)" | Bundesamt für Sicherheit in der Informationstechnik (BSI), Germany | 2020-10-01 | VERIFIED |
| 2 | Contactless payment uses NFC at 13.56 MHz under ISO/IEC 14443. | https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR03105/TR-03105_ISO-IECvsNFC.pdf?__blob=publicationFile&v=1 | "It defines contactless smart card technology (cards and reader devices) at 13.56 MHz." | BSI | Undated; accessed 2026-10-31 | VERIFIED |
| 3 | A tap normally works at a few centimetres: about 4 cm in practice, with an ISO proximity limit of about 10 cm depending on the reader. | https://usa.visa.com/content/dam/VCOM/global/partner-with-us/documents/vca-contactless-opinion-paper-global.pdf | "For the payment to work, the card or phone must be held within 4cm of the secure contactless reader." | Visa Consulting & Analytics | Undated; accessed 2026-10-31 | VERIFIED |
| 4 | An EMV contactless transaction generates a fresh one-time cryptogram for each tap, not a fixed secret. | https://www.emvco.com/emv-technologies/contactless/ | "A one-time use security code is generated for every transaction to safeguard against fraud." | EMVCo | Undated; accessed 2026-10-31 | VERIFIED |
| 5 | Network tokenisation replaces the card number with a token for mobile wallets and, for some schemes, contactless cards. | https://www.emvco.com/emv-technologies/payment-tokenisation/ | "removing the most valuable data to a fraudster, the primary account number (PAN), and replacing it with a unique alternative value, the EMV Payment Token." | EMVCo | Undated; accessed 2026-10-31 | PARTIAL |
| 6 | Authorisation is a message exchange: merchant terminal to acquirer to card network to issuer, and back. | https://www.bankofengland.co.uk/explainers/how-do-card-payments-work | "the company providing the card reader tells Visa about the payment. Visa then works with your bank and the company providing the card reader" | Bank of England | 2019-01-10 | VERIFIED |
| 7 | Authorisation does not move money; clearing and settlement happen later. | https://www.philadelphiafed.org/-/media/FRBP/Assets/Consumer-Finance/Discussion-Papers/D-2013-October-Clearing-Settlement.pdf | "Settlement is the final process in the series of steps that begins with authorization" | Federal Reserve Bank of Philadelphia | 2013-10 | VERIFIED |
| 8 | The pending/hold amount can differ from the final posted amount, for example at restaurants (tip added later) or fuel pumps (final amount unknown at tap time). | https://www.capitalone.com/help-center/credit-cards/card-pending-transactions/ | "These adjustments also explain why final transactions and pending amounts sometimes differ." | Capital One | Undated; accessed 2026-10-31 | VERIFIED |

## Notes

- Claim 1 quote translated: "does not have its own power supply (but instead draws the energy it needs from the reader's EM field by electromagnetic induction)".
- Claim 3: 4 cm is the practical tap distance; the ISO/IEC 14443 proximity range is up to about 10 cm (see claim 2 source). Readers and antennas vary.
- Claim 5 is PARTIAL: the token definition and mobile-wallet use are verified. The "some contactless cards" half was not verified; a normal plastic contactless card commonly presents the PAN stored on its chip. Do not use that half without a scheme-specific source.

## Safe wording

1. A contactless card has no battery: the reader's radio field powers its chip during the tap.
2. Tap-to-pay runs on NFC at 13.56 MHz, the ISO/IEC 14443 proximity standard.
3. You hold the card about four centimetres from the reader; the standard's proximity range goes up to about ten centimetres.
4. Every tap creates a new one-time cryptogram, so a copied code cannot be reused.
5. Tokenisation replaces the card number with a restricted token; mobile wallets use it, while tokenised plastic cards depend on the scheme and market.
6. The terminal passes the transaction to the acquirer, the network routes it to the issuer, and the answer travels back.
7. Authorisation is a check only; clearing and settlement move the money afterwards.
8. The amount on hold can differ from the final charge, for example when a tip or a fuel purchase is settled later.

## Do not say

1. "The tap moves the money instantly." Authorisation can be fast; settlement is later and the hold can change.
2. "The card sends your PIN over the air." The PIN is not transmitted by the contactless card.
3. "The card has a battery and broadcasts continuously." It is passive and only active in the reader's field.
4. "Contactless payments are anonymous or untraceable." Transaction data is sent; tokenisation limits exposure, not traceability.
5. "Approval means the payment is final." Clearing and settlement follow, and the posted amount can differ.
