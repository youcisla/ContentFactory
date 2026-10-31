# Storyboard — What Actually Happens When You Tap a Card

Status: production board, 40 s, 9:16, 24 fps, 540×960 preview at 8 samples. Source scene: `tools/blender_scene_v4.py`. Art direction: `docs/creative/TREATMENT_TAP.md`. All narration is PLACEHOLDER; there is no recorded audio. Captions are edit-layer overlays; the terminal screen stays textless.

## 1. Logline

A single contactless tap, followed in one continuous macro shot, reveals that the reader powers the card and that the green approval light is a hold, not a payment.

## 2. One-sentence teaching claim

A contactless tap is a powered data exchange that obtains an authorization hold, not a transfer of money; settlement moves the money later.

## 3. Art direction

Palette, unchanged: Void `#05070D` (world and negative space), Graphite `#12161F` (terminal chassis and card body), Steel `#2A3340` (bevels and edges), Signal cyan `#22D3EE` (field and outbound request), Approval green `#34D399` (approval response), Warning amber `#F5B547` (chip and hold state), Paper `#E6EDF7` (captions only).

Look: premium fintech hardware photography. Matte black surfaces, one warm key, one cool rim, deep falloff, no decorative gradients. The V4 scene already supplies the set: world gradient, four area lights, beveled card, terminal, coil, chip, indicator, packet.

One deliberate addition: a **colour-location rule**. Approval green may appear only on the terminal — the NFC indicator and the screen — and on the returning packet. It never appears on the card. The card's only lit element is the amber chip. Why: the film's argument is that approval is a message at the terminal, not value moving to the card. The colour map makes that argument before the narration does. The rule costs nothing: it reuses `ind_mat`, `screen_mat`, and `pkt_mat`; only their emission colours are keyed.

No new hue, no new material, no new geometry. The terminal screen is treated as a state light, not a display: cyan idle, green approved. The V4 screen still reads as a slab (CF-136), so no diegetic text is put on it. Captions are edit-layer overlays in the system sans; no font files.

The treatment's "type appears twice only" rule was sized for the 10 s POC. This 40 s cut uses one caption per beat, six total, because the film must work silently. **This is the plan for the full 3D cut, which is not built.** The animatic that exists uses 12 cues, because 10 s of 3D carries three beats and the diagrams carry the rest — see §9 and §10. Where the two differ, `render/captions/contactless_40s.srt` is what has been burned in. All captions are Paper, one line, lower third; no background box.

The current `CardBody` material is a dark navy (0.016, 0.030, 0.082), not Graphite. Either grade it to Graphite or accept the navy as the card's coat; one line, no geometry. The board does not depend on the difference.

## 4. Shot table

The film is one continuous take. The six rows are beats, not cuts. The camera is the existing V4 dolly, re-timed to complete at 36 s and hold to 40 s. No row introduces a new camera move. The light rig translates with the camera, as it does now.

| Shot | Time | Duration | Camera move | What is on screen | What physically happens (the cause) | What the viewer learns (the effect) | On-screen text (max 6 words) | Narration (max 18 words) |
|---|---|---|---|---|---|---|---|---|
| S1 | 0.0–4.0 | 4.0 s | Existing dolly, start framing; no new move | Card edge and amber chip above the terminal; the card descends into the reader's field; no contact | The reader emits an oscillating magnetic field; the card has no battery, so the field couples to its coil | A tap is not a button press; the reader powers the card | "NO BATTERY. NO CONTACT." (4) | PLACEHOLDER — "This card has no battery. The reader's field powers it." (10) |
| S2 | 4.0–10.0 | 6.0 s | Existing dolly, slow push; no new move | Four coil bars light from the card's edge inward; the chip wakes; the terminal screen rises from idle cyan | The 13.56 MHz field induces an alternating current in the coil; the chip rectifies it and powers up | The card is alive only while it is in the field; remove it and it sleeps | "THE READER POWERS THE CARD" (5) | PLACEHOLDER — "The field induces a current in this coil. The chip wakes up." (12) |
| S3 | 10.0–17.0 | 7.0 s | Existing dolly, mid-push; no new move | NFC indicator lights; a cyan packet forms at the reader head and lifts | Card and reader exchange data; the card returns a one-time cryptogram for this transaction; the terminal builds the request | The code is single-use and tied to this tap | "A ONE-TIME CODE" (3) | PLACEHOLDER — "The card adds a one-time code. It is good for this tap only." (13) |
| S4 | 17.0–24.0 | 7.0 s | Existing dolly, push toward the terminal face; no new move | The packet arcs up and holds near the top edge; the terminal and card hold still | The terminal sends the request to the acquirer, which routes it through the network to the issuer | The decision happens off-screen, outside the room | "THE DECISION IS OFF-SCREEN" (4) | PLACEHOLDER — "The request goes to the merchant's bank, the card network, then your bank." (13) |
| S5 | 24.0–32.0 | 8.0 s | Existing dolly, near-end framing; no new move | The packet returns green along the same arc and docks at the terminal; the indicator and screen turn green; the card is unchanged; the chip stays amber | The issuer approves and returns an authorization response; it places a hold on the amount | Approved is a hold, not a payment; the amount is held, not transferred | "APPROVED IS NOT PAID" (4) | PLACEHOLDER — "Approved means the issuer reserved the amount. Nothing moved yet." (12) |
| S6 | 32.0–40.0 | 8.0 s | Existing dolly completes at 36 s, then holds; no new move | Terminal stays green; card and chip unchanged; the packet has shrunk to a point; the camera settles | Later, clearing and settlement move funds between banks; the merchant's payment is settled then | Authorization, clearing, and settlement are three steps; the tap only did the first | "SETTLEMENT MOVES MONEY LATER" (4) | PLACEHOLDER — "Later, clearing and settlement move the money. The tap only asked permission." (10) |

Caption timing: S1 0.5 s, S2 5.0 s, S3 11.0 s, S4 18.0 s, S5 27.5 s, S6 33.0 s. S5's caption lands on the green light, not at the shot start.

Narration timing: each line starts about 0.5 s into its shot. S5 starts at 25.0 s so "It has not moved" lands at about 28.5 s, on the reversal.

## 5. Beat map

0.0–1.5 s — **Hook.** The card is already in frame, chip amber, no contact. The caption "NO BATTERY. NO CONTACT." asks the question. The viewer's first thought: if it has no battery, how does it work?

1.5–12.0 s — **Mechanism.** The field induces current; the coil lights; the chip wakes; the card adds a one-time code. By 12 s the viewer can explain the tap in one sentence: the reader powers the card, and the card sends a single-use code.

12.0–28.0 s — **Request and decision.** The packet leaves, holds at the top edge, returns green. The tension is "will it approve?" The relief is the green light. At 28 s the reversal lands: the green light is a hold, not a payment. The feeling turns from relief to re-evaluation.

28.0–40.0 s — **Close.** The terminal stays green; the card does not change; the packet is gone. "SETTLEMENT MOVES MONEY LATER" and "The tap only asked permission" close the loop. The last four seconds are still, so the distinction has room to stick.

The four required marks: hook 1.5 s, mechanism 12 s, reversal 28 s, close 40 s.

## 6. The reversal

**The reversal: people read "approved" as "paid," but a contactless tap only obtains an authorization hold, and the money does not move until clearing and settlement.**

This is a real misconception, not a strawman. "Approved" on the terminal and "pending" in a banking app are two views of the same authorization: the issuer has placed a hold. The posted balance changes later, after clearing and settlement. The film scopes the claim to card payments; it does not claim every payment scheme is slow, and it does not put a time on settlement.

The visual proof is the colour-location rule: green appears on the terminal, never on the card; the returning packet stops at the terminal and does not travel to the card.

## 7. What we will NOT show

- **Floating NFC torus rings.** They read as the technology and teach nothing; the coil is the real coupling element. V4 already deleted them.
- **A coin, banknote, or money symbol flying from card to terminal.** It teaches the exact falsehood the film corrects: money does not move at the tap.
- **Wi-Fi-style arcs radiating from the terminal.** Contactless is near-field inductive coupling, not a radio broadcast; the arcs teach the wrong physics.
- **A full card number on screen with a "your number stays safe" caption.** A physical contactless card may transmit its PAN; the film cannot make that claim without lying about a specific card. The one-time cryptogram is the accurate common element.
- **A padlock, shield, or "bank-grade security" stamp; any card-network or bank brand mark.** A security badge is a claim, not a cause; a brand mark is identity and licensing, not mechanism. The film stays on the mechanism.

## 8. Buildable check

The board is built on the CF-133 scene as it stands: one card, one terminal, one coil, one indicator, one packet, one continuous dolly. It does not assume the CF-136 terminal/screen fix or the CF-135 exposure fix; it works around both. CF-134's packet exit is fixed by the apex reduction below.

| Shot | Existing objects in `tools/blender_scene_v4.py` | New geometry |
|---|---|---|
| S1 | `Card`, `Chip`, `TermBase`, `TermHead`, `camera`, `Key`, `Fill`, `Rim`, `Back`, world gradient | None |
| S2 | `CoilTop`, `CoilBottom`, `CoilLeft`, `CoilRight` (`coil_mat`), `Chip`, `Screen` | None |
| S3 | `Indicator` (`ind_mat`), `Screen`, `Packet` | None |
| S4 | `Packet` | None |
| S5 | `Packet`, `Indicator`, `Screen`, `Card`, `Chip` | None |
| S6 | `TermBase`, `TermHead`, `Screen`, `Indicator`, `Card`, `Chip`, `Packet` | None |

**No NEW GEOMETRY anywhere.** The board is a re-time and re-key of the existing scene, not a rebuild.

Required script work, not new assets: re-time `story()` to 960 frames; add a return leg to the packet Bezier; hold the packet at the apex for 2 s; reduce the apex to z ≈ 0.155 so the packet stays inside the top edge (fixes CF-134); key emission colour from Signal cyan to Approval green on `pkt_mat`, `screen_mat`, and `ind_mat`; ease the camera to complete at 36 s and hold to 40 s.

Camera: `cam.data.lens` is 65 mm; the comment above it says 55 mm. The board assumes 65 mm as built. If the apex still clips at 540×960, set the lens to 55 mm — a one-line parameter change, not a new camera move. A new camera move (a pull-back or orbit) is CUT: it would move the light rig and re-open the exposure QA (CF-135). The one existing dolly is re-timed, not replaced.

Screen: the V4 screen reads as a teal slab, not a display (CF-136). The board uses it as a state light and puts no diegetic text on it. If the film must be a single Blender render with text, each caption is NEW GEOMETRY (a text object with the built-in font) — six new objects and a new build cost; not assumed here.

Lighting: the V4 rig is a warm key (5.2), cool fill (0.55), cool rim (3.0), and back light (1.2), with a dark-to-cool world gradient. The treatment's lighting text specifies a cool key and a warm fill; the board follows the scene to avoid a relight. If strict treatment compliance is required, swap the Key and Fill colours — a one-line change that re-opens exposure QA.

Budget: 960 frames at 24 fps, 540×960, 8 samples, about 2.4 s per frame, about 38 minutes. If that is too long, the only trimmable beat is the final hold (2 s, 48 frames); do not shorten the mechanism shots. A 38 s cut keeps the same six beats. A 1080×1920 final is a separate budget, roughly four times the render time.

### CUT

- **Five-node network reveal (18 s).** Needs five new node objects and a new camera pull-back; it would imply the network is physically visible. The issuer stays off-screen; the packet apex carries the request.
- **Pull-back reveal at 36 s.** Needs a new camera move; the light rig moves with the camera, so it would re-open the exposure QA (CF-135). The close holds on the existing end framing.

## Rejected

- **Generic slideshow pacing.** No two-second cuts; six beats in one continuous take, 4–8 s each. The camera and the packet carry the transitions.
- **Arbitrary camera orbits.** The camera only pushes on the existing dolly; no orbit, no crane, no new move. The move is motivated by the approach to the reader.
- **Glow with no cause.** Coil emission is tied to the field ramp; indicator green is tied to the returning packet; packet emission is tied to departure and return. The screen is a state light. No ambient glow, no decorative bloom.
- **Text that repeats what the image already shows.** Captions state the claim the image cannot show: no battery, one-time code, off-screen decision, approved is not paid, settlement later. No "CARD TAPS TERMINAL."
- **Marketing claims about speed or security.** No "instant," "0.3 seconds," "secure," "encrypted," "bank-grade," "safe." The one-time code is a mechanism, not a guarantee. The film says "approved," not "instant approval."

## 9. Reconciliation — 2026-10-31, after CF-134/135/136 landed

The board was written against the pre-fix scene and works around three defects. All three are now closed, so the assumptions in §8 are superseded by measurements. Recorded here rather than rewritten, because the board's structure and claim mapping still hold and rewriting it would hide what was actually constrained at the time.

| Board assumption | Now |
|---|---|
| Packet apex must be reduced to z ≈ 0.155 to stay in frame (CF-134) | Apex is **0.150**, set by the geometry gate, not by eye. Gate PASSes with 0.140 NDC edge margin and 3.19 mm clearance |
| Screen reads as a slab; treat it as a state light only (CF-136) | Screen **is a display**: dark glass, cyan amount line, green approval tick. The "state light" treatment still stands — the tick is the only state change, and no diegetic text is used |
| Warm key 5.2 / cool rim 3.0 | Key is now **11.0 W over a 0.22 m source** (softened to stop a mirror blowout); Rim is **1.0**. The rig's colour roles are unchanged |
| `CardBody` is navy, not Graphite | Navy is kept deliberately and deepened to (0.010, 0.018, 0.050). Graphite was never going to work: card and housing in the same value is what made the frame grey-on-grey |
| `cam.data.lens` comment says 55 mm, code says 65 mm | Comment corrected to 65 mm. 65 mm is what every render used |
| Camera elevation unspecified | 23°, raised from 17°, because a card 10 mm above the panel projects across it below ~20° |
| Six caps in 40 s, ~38 min render | **Not rendered.** The 10 s, three-beat cut is what exists: 240 frames, 371 s. The 40 s cut needs a return leg and a re-time to 960 frames, written in §8 but not built |

**What this does not change:** the reversal, the colour-location rule, the six-beat structure, the caption set, and every claim in the script map. The rendered 10 s cut covers the board's S1–S3 compressed; S4–S6 remain unbuilt.

## 10. Final production plan

### What the animatic is

`render/animatic/contactless_40s_animatic.mp4` is a **previsualisation**: 960 frames, 40.000 s, 540×960, 24 fps, captions burned in, **no audio of any kind**. Frame 1–240 is finished 3D. Frames 241–960 are SVG diagrams with a moving marker and a slow push-in. It is the right length, the right order, and the right claims. It is not final picture and it must not be published as such.

### Measured render cost

One 1080×1920 frame at 8 samples costs **8.51 s** (median of frames 2–4; frame 1 costs 11.4 s because it compiles shaders). The same scene at 540×960 costs 1.54 s. Output is 1.82 MB per 1080p PNG.

| Target | Frames | Basis | Time | PNG disk |
|---|---:|---|---:|---:|
| 10 s of 3D at 540×960 (what exists) | 240 | 1.54 s measured | 6 min | 116 MB |
| 10 s of 3D at 1080×1920 | 240 | 8.51 s measured | **34 min** (range 28–40) | 437 MB |
| 40 s entirely in 3D at 1080×1920 | 960 | 8.51 s measured | **136 min** | 1.75 GB |

Disk is **not** the constraint: 77 GB free against 1.75 GB worst case. The constraint is that the network beats have no photographable geometry, so making them 3D buys cost and no accuracy.

### Priority order

1. **Decide the 3D/2D split.** Recommendation: keep 2D for S4–S6. A card network is not a place; a diagram is the honest representation, and it is minutes of work rather than two hours of render. Revisit only if the 2D/3D cut reads badly to a viewer who has not seen the board.
2. **Build the missing mechanism.** The 40 s cut needs the packet's return leg and a re-time to 960 frames. That is the only thing standing between the current 10 s shot and a complete 3D S1–S3 at final quality.
3. **Render S1–S3 at 1080×1920.** 240 frames, 34 minutes, 437 MB. Verified geometry gate first (`CF_GEOMETRY_ONLY=1`), then stills, then the sequence — the same order that caught the packet exit, the occlusion, and the card crop.
4. **Audio is blocked.** There is no narration, no music, no ambience. Producing any of it needs either a recording or an approved TTS/model download, which the approval gate has not granted. Until then the film ships captioned, and this must be stated wherever it is shown.
5. **Captions are ready.** `render/captions/contactless_40s.srt`, 12 cues, already burned in by `tools/build_animatic.py`.

### Gates still closed

- **V3/V4 creative acceptance** — the user's, not the script's.
- **G1 claims** — the claim sheet is verified but the gate record does not exist.
- **G5 publication** — not requested and not closeable by an agent.
