# 01 — Reconciliation of v1 Contradictions

Purpose: find and settle every inconsistency between v1 reports before building v2 on top of them. Nothing here is cosmetic; each item names which file wins and why.

---

## R1 — 66/100 vs 69/100 (the item you flagged)

| File | Value | Context |
|---|---|---|
| `v1/00-executive-decision.md` | 66 | "Weighted score after redesign" row |
| `v1/05-scorecard.md` | **69.0** | Full S1 table, arithmetic shown |

**Resolution: 69.0 is correct.** Recomputing S1 from the published table — 14.0 + 12.0 + 12.0 + 10.5 + 6.0 + 8.0 + 4.0 + 2.5 — sums to 69.0. The 66 was a draft figure written into `00` before the `05` table was finalised, and never reconciled.

**Disposition:** v1 `00` line is wrong. v2 supersedes it. v1 `05` stands.

## R2 — Pessimistic sensitivity case is arithmetically wrong

`v1/05` §3 states pessimistic = **44.5**. Applying the stated inputs (dims 1,3 → 2; dims 2,8 → 2; others unchanged) yields:

8.0 + 8.0 + 6.0 + 10.5 + 6.0 + 8.0 + 4.0 + 2.0 = **52.5**

**Resolution: 52.5.** The 44.5 would require additional dimensions to drop, which the table does not state. Corrected band: **52.5 – 69.0 – 80.5**.

## R3 — Variable cost envelope differs between files

| File | 40 s Short | 8 min long |
|---|---:|---:|
| `v1/00` | $0.05–$3 | $0.5–$6 |
| `v1/04` §11 | $0.05–$0.75 | $0.25–$4.30 |

**Resolution:** `04` is the base case; `00` quoted a worst-case envelope that includes premium TTS pricing. Both are defensible but were presented as the same number. v2 `05` states base and worst case separately.

## R4 — Human review rate was applied to the wrong format

`v1/00` says "20–45 min per finished minute". `v1/04` implies 45–90 min per finished minute for a 40 s Short (0.5–1 h review on 0.67 min of video) and 22–45 min/min for the 8-minute long-form.

**Resolution:** the 20–45 figure applies to **long-form only**. Shorts carry a higher review cost per minute because fixed overhead (fact-check, metadata, thumbnail) is amortised over less runtime. v2 uses 30–60 min per Short.

## R5 — Python version: 3.14.8 vs 3.14.6

- Registry uninstall entry: `Python 3.14.8`.
- Interpreter at runtime: `Python 3.14.6` from `pythoncore-3.14-64`.

**Resolution: 3.14.6** — the runtime is what executes. The registry entry reflects a different installed package/version. Neither is suitable for the ecosystem; v2 still requires a pinned 3.12 environment.

## R6 — Node version: 26.12.1 vs 26.3.1

- Registry: `Node.js 26.3.1`.
- `node --version`: `v26.12.1` via `C:\nvm4w\nodejs\node.exe`.

**Resolution: v26.12.1** — nvm-windows owns the active runtime; the MSI entry is a leftover base install. Node version churn is a maintenance risk for any Node-based renderer.

## R7 — GPU memory: 2048 MB reported vs registry VRAM absent

`Win32_VideoController.AdapterRAM` reports 2048 MB, but the registry `HardwareInformation.qwMemorySize` query returned nothing.

**Resolution:** 2048 MB is a **shared-memory reporting artefact**, not dedicated VRAM. The machine has no dedicated VRAM. v2 never treats 2 GB as usable GPU memory.

## R8 — "Four candidates with 0–17 stars" vs the table

`v1/00` says four candidates have 0–17 stars. `v1/03` table shows: 0, 2, 3, 17 (and 12 for BlendRelay). Counting ≤17 gives **five**, not four.

**Resolution: five.** Wording error in `00`; the underlying table is correct.

## R9 — Blender licence labelled two ways

`v1/02` says `GPL-2.0-or-later`; `v1/03` says "site: GPL" while GitHub reports `NOASSERTION`.

**Resolution:** Blender is distributed under the GPL (the Foundation's own licence page). The precise "2.0 or later" qualifier is a convention not re-verified from the licence text in v1. v2 writes "GPL (version qualifier unverified)" and does not depend on the distinction.

## R10 — Score scale ambiguity between plan quality and system readiness

`v1/05` mixes two different 0–5 scales in adjacent sections (system dimensions vs plan-quality aspects), which invites misreading 4.6/5 plan quality as 92/100 system readiness.

**Resolution:** v2 separates them explicitly; plan quality is labelled subjective and excluded from any aggregate.

## Contradictions intentionally left standing

| Item | Why not "fixed" |
|---|---|
| `v1/01` says 31.5 GB usable vs 32 GB installed | Both true (firmware reserve); not a contradiction |
| `v1/03` star counts will drift | Point-in-time measurement; date is stated |
| `v1/04` calls render times "unmeasured" while giving ranges | Ranges are labelled estimates; that is the correct handling |

## Net effect on v2

Corrected v1 baseline: **S1 = 69.0**, sensitivity band **52.5–80.5**, shorts review **30–60 min**, cost base **$0.05–0.75**. None of these corrections changes the v1 verdict; they change the precision of its numbers. The v2 architecture comparison is scored fresh and does not inherit them.
