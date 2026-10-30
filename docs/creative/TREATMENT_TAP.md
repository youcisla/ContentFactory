# Creative Treatment — "The Tap"

Status: pre-production for the 10-second cinematic proof of concept.
Format: 1080×1920, 9:16, 12 fps capture, H.264 delivery.
Topic: what happens when a contactless card is tapped.

---

## 1. Concept

One tap. A pulse of light leaves the card, enters the terminal, and races into a dark network of institutions. It returns as an approval. The film ends on the distinction most explainers miss: **the money did not move**.

The camera is a character: it starts as a macro observer, becomes a traveller following the packet, then pulls back to reveal the whole machine.

## 2. Art direction

| Token | Value | Use |
|---|---|---|
| Void | `#05070D` | Background, negative space |
| Graphite | `#12161F` | Card body, terminal chassis |
| Steel | `#2A3340` | Metal edges, terminal bezel |
| Signal cyan | `#22D3EE` | Data in flight |
| Approval green | `#34D399` | Authorization response |
| Warning amber | `#F5B547` | Card chip, "hold" state |
| Paper | `#E6EDF7` | Titles only |

Language: premium fintech hardware photography — matte black surfaces, one warm rim light, one cold key, deep falloff, no decorative gradients. Type appears twice only; the mechanism carries the story.

## 3. Shot list

| # | Time | Shot | Camera | Action | Text |
|---|---|---|---|---|---|
| S1 | 0.0–1.6 | Macro card edge in darkness | Low, slow push | Rim light reveals silhouette; chip catches amber | `THE TAP` |
| S2 | 1.6–3.4 | Card approaches terminal | Slight orbit | Card tilts toward terminal face; NFC rings bloom | — |
| S3 | 3.4–5.2 | Contact | Camera dips under the card | Packet launches into the terminal; rings collapse | — |
| S4 | 5.2–7.2 | Into the network | Camera follows packet, rises | Terminal recedes; five institution nodes emerge in depth | — |
| S5 | 7.2–8.6 | Decision | Slow lateral drift | Issuer node pulses amber, then green; return pulse travels back | — |
| S6 | 8.6–10.0 | Pull-back reveal | Crane up and back | Terminal reads APPROVED; topology visible | `A HOLD IS NOT A PAYMENT` |

## 4. Lighting and camera

- Key: cool directional from upper left (0.6, 1.0, 0.5), intensity ~1.0.
- Fill: warm from lower right, ~0.25.
- Rim: fresnel term ~0.15, separating black objects from a black background.
- Contact shadow: soft radial darkening under card and terminal — not ray-traced. Stated as a limitation.
- Camera: perspective, 40° vertical FOV, eased keyframes, one continuous move, no cuts.
- Depth cueing: distance fog toward `#05070D` plus scale falloff of network nodes.

## 5. Asset list and provenance

| Asset | Source | Licence |
|---|---|---|
| Card, chip, terminal, rings, nodes, packet | Procedural geometry generated in-scene | Original |
| Type | System stack (`Segoe UI`, Inter, Arial) | System |
| Terminal screen | 2D canvas drawn at runtime | Original |
| Audio | None in this POC | — |

No external images, fonts, models, HDRIs, or brand marks. No card-network logos.

## 6. Animation plan

- All state is a pure function of `t` seconds; no randomness, no timers, no accumulated physics.
- Easing: smoothstep for camera, cubic ease-out for the packet.
- Rings: three torus meshes, phase-shifted, additive, life 0.9 s.
- Packet: emissive sphere with additive halo; path card → terminal → issuer → return.
- Terminal screen: canvas texture, `READY` → `APPROVED` at decision time.
- Determinism: `?t=` renders exactly one frame, so any frame is reproducible.

## 7. Tool selection rationale

| Candidate | Status | Verdict |
|---|---|---|
| Blender Eevee | **Not installed** | Unavailable; strongest look if installed |
| Three.js / R3F | Not installed; download blocked | Unavailable |
| Hyperframes | Skills instructional; no local CLI binary | Unavailable for rendering |
| Remotion | Not installed; needs Chromium download | Unavailable |
| Manim | Not installed | Unavailable |
| Rust/wgpu/Bevy | Toolchain present; crates not downloadable | Unavailable |
| **Custom WebGL + Chrome + FFmpeg** | Present and authorised | **Selected** |

Real perspective, normals, specular response, fresnel rim, fog, moving camera. Cannot produce ray-traced shadows, true depth of field, or motion blur — stated up front.

## 8. Long-form outline (8–10 min)

1. Cold open: the 1.3-second promise, then "what actually happened?"
2. Four-party model: cardholder, merchant/acquirer, network, issuer.
3. Contactless specifics: NFC, tokenization, cryptograms, token service provider.
4. The authorization message: fields, stand-in processing, latency budgets.
5. Fraud scoring: rules vs models, false declines, cost of friction.
6. Approval vs hold: what the balance screen shows.
7. Clearing and settlement: batching, netting, interchange, T+1 and instant schemes.
8. Failure modes: declines, timeouts, double holds, chargebacks.
9. Practical takeaways: pending vs posted, why holds linger.
10. Close: a chain of promises, not a transfer of money.

## 9. Resource budget (estimated)

| Item | Estimate |
|---|---|
| Frames | 120 at 12 fps, 10 s |
| Capture | ~1.5–2.5 s per frame → 3–5 min |
| Peak RAM | < 1.5 GB |
| Disk | 25–40 MB PNG + ~4 MB MP4 |
| GPU | Software (SwiftShader) |
| Cost | €0 |

## 10. Acceptance criteria

1. Recognisable 3D depth and perspective in every shot.
2. Camera motion motivates each transition; no cut hides missing animation.
3. Consistent lighting; black objects separated by rim light.
4. Mechanism readable at 360 px without relying on text.
5. Any frame reproducible from `?t=`.
6. Limitations documented: no ray-traced shadows, no DOF, no motion blur, no audio.
7. Weighted score ≥ 80 for POC review. 90 is the production-candidate target; a 10-second software-rendered POC is not expected to reach it.

## 11. Gates

- **V0** treatment approved (this document).
- **V1** stills at t = 0.5, 3.0, 6.0, 9.0 inspected at native and 360 px.
- **V2** 10-second MP4 inspected; score recorded.
- **V3** user creative acceptance — required before pipeline work.
