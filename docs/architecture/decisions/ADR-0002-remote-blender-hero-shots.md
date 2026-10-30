# ADR-0002 — Remote Blender for hero shots only

- Status: proposed
- Date: 2026-10-30
- Deciders: user (sign-off pending), agent (proposal)
- Related: ADR-0001, `reports/v2/02`, `reports/v2/04`

## Context

Blender's Cycles backend supports CUDA/OptiX (NVIDIA), HIP (AMD RDNA1+), and oneAPI (Intel Arc / Xe HPG). The measured host has a single **integrated Intel adapter**, which is not an Arc part, so Cycles cannot run on its GPU. EEVEE would run on the iGPU but is unmeasured, RAM-heavy, and slow to iterate.

Live marketplace pricing measured on 2026-10-30: **RTX 4090D $0.108/h**, **RTX 5090 $0.269/h**. An 8-minute render occupying 1–3 GPU-hours therefore costs roughly **$0.11–0.81**.

Local Blender remains possible on CPU, but a full episode re-render on 12 cores is an evening, not a coffee break.

## Decision

Blender is used **only for short 3D hero shots** (3–8 seconds, at most two per episode), rendered on a **rented GPU**. The local machine orchestrates: prepares the scene, uploads, polls, downloads frames/video, and composites. No full episode is rendered in Blender.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Local Cycles CPU | Too slow to iterate; blocks the day |
| Local EEVEE on iGPU | Unmeasured; RAM spikes 2–8 GB against ~8.7 GB free; driver risk |
| Full-episode Blender (remote) | Makes a vendor the core of every video; cost and outage risk on the critical path |
| three.js in-browser 3D | Headless WebGL determinism and weight; more engineering for less quality |

## Consequences

**Positive:** near-top visual quality where it matters; local pipeline stays light; cost per shot under $1.

**Negative:** an external dependency exists, but only for optional shots; upload/download must be scripted; reproducibility requires a pinned image and scene version.

**Harder:** interruption handling. Marketplace hosts can vanish mid-render, so jobs must be idempotent and retryable.

## Guardrails

1. Pin the Blender version and scene template; record both in `render_job.json`.
2. Destroy the instance after each job; no persistent subscription.
3. Never upload credentials, only scene assets.
4. If two runs differ, the shot is not reproducible — fix before publishing.
5. Hero shots are optional: an episode must be publishable without them.

## Evidence

- `reports/v2/04-tts-assets-render-v2.md` §4 — measured GPU prices
- `reports/01-machine-inventory.md` §3 — no supported Cycles GPU
- `reports/v2/02-architecture-comparison-v2.md` — architecture D scoring
