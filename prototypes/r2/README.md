# R2 — Animated prototype

12-second, looped, 9:16 animation of the authorization flow. Pure HTML + inline SVG + CSS. No JavaScript animation, no external assets, no fonts downloaded, no packages.

## Run

Open `index.html` in Chrome or Edge. Nothing else is required. The stage auto-scales to the window.

## Timeline

| Time | Beat |
|---|---|
| 0.0–1.0 s | Kicker and title fade in |
| 1.2 s | Node 1 (Card) rises |
| 2.2 s | Node 2 (Terminal) |
| 3.2 s | Node 3 (Acquirer) |
| 4.2 s | Node 4 (Card network) |
| 5.2 s | Node 5 (Issuing bank) |
| 1.2–8.6 s | Cyan packet travels down the flow |
| 6.2 s | Footer note |
| 9.4–11.3 s | Takeaway overlay: "A hold is not a payment" |
| 12 s | Loop resets |

## Determinism notes

- All motion is CSS keyframes with fixed durations; no randomness, no timers.
- The stage geometry is fixed at 1080×1920; only display scaling changes.
- `prefers-reduced-motion` disables motion and shows the final composition.
- `?t=<seconds>` freezes every animation at that timestamp via the Web Animations API, so previews are reproducible.
- `?motion=full` opts out of the reduced-motion fallback; headless Chrome otherwise reports `reduce` and disables animation. Preview only.
- Reduced-motion users get the takeaway card as the final composition; it replaces the flow rather than overlapping it.

### Preview capture

Headless screenshots do not advance CSS animations by default: three captures at 2 s, 6 s and 10 s were byte-identical. The `?t=` parameter exists to make still capture deterministic. It is a preview aid, not a renderer.

## What this proves

- The visual language and narration beat can be expressed in the browser with zero dependencies.
- Sequencing and timing are expressible without a build step.

## What this does **not** prove

- That offline frame rendering is feasible. Browser playback is not a video renderer.
- That the timing survives conversion to 30 fps video. That requires frame capture, which needs an approved renderer.
- That the final look holds on a phone at 360 px: only a still-frame check was performed.
