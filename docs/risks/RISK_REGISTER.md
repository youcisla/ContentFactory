# Risk Register

Owner: user. Reviewed: 2026-10-30. Next review: after B0, or when any trigger fires.
Probability and impact are qualitative until a benchmark exists.

| ID | Risk | P | Impact | Mitigation | Trigger to act | Status |
|---|---|---|---|---|---|---|
| R1 | Corporate policy forbids installs or personal commercial use on this device | Medium | **Fatal** | Resolved by user declaration (G0); personal device or cloud-only fallback remains available | Policy reversal | **Closed — user declaration 2026-10-30** |
| R2 | Local render too slow to iterate | **Confirmed for 3D** | High | B0 still unmeasured (vector path). For Eevee, `BLENDER_EEVEE_CORRECTION.md` gives the curve; fallback is cloud GPU or fewer shadow rays | 10 s test > 10 min | Open — vector path unmeasured; 3D path measured and fails |
| R3 | Disk exhaustion during production | Medium | High | Disk guard (refuse <15 GB, abort <8 GB); per-episode purge; external SSD | Free space <15 GB | Open |
| R4 | Factual error ships | Medium | High | G1 claims gate enforced at schema level; correction policy (Q8) | Any post-publish correction | Open |
| R5 | Agent-generated code damages files | Low | High | No MCP on host; isolated VM only; no credentials in scope | Any request to run MCP locally | Open |
| R6 | TTS rights challenge | Low | High | Licensed engines only; Edge TTS banned for published output | Any monetisation review | Open |
| R7 | Asset licence contamination | Medium | High | `commercial_ok` field; licence evidence hash; per-asset check | Asset with unknown licence | Open |
| R8 | Visual quality below audience threshold | High | Medium | R1 style approval before build; retention feedback after R7 | Retention < 40 % | Open |
| R9 | Schema drift breaks re-render | Medium | Medium | Strict validation; pinned versions; template versioning | Validation error on a known-good episode | Open |
| R10 | Human review caps output | High | Medium | Templates and checklists; accept ~2 long-form/month until proven otherwise | >60 min review per finished minute | Open |
| R11 | YouTube API restricts unaudited uploads | Medium | Medium | Manual upload for first 10; verify audit status | API upload returns restricted state | Open |
| R12 | Cloud GPU price or reliability shifts | Medium | Low | Measured $0.11–0.27/h; 2× sensitivity case; hero shots optional | Price > $0.50/h or repeated interruptions | Open |
| R13 | Publication leaks identifiers or secrets | Low | High | ADR-0006; `.gitignore`; review before commit | Any sensitive string found in a diff | Open |
| R14 | Single-maintainer dependency abandoned | Medium | Medium | Prefer projects with releases <90 days; pin versions; exit path per component | No release/commit for 6 months | Open |
| R15 | Eevee too slow on the iGPU for animation | **Confirmed** | **High** | Local Eevee for stills and look-dev only; remote or managed GPU for animation | Measured at 1080×1920: 6.67 s/frame at 8 TAA samples, 29.14 s at 64, 77.41 s at 64 with raised shadow sampling. 240 frames = **27 min to 5.2 h** against a ≤15 min budget | **Triggered** — remote promoted. GPU backend confirmed hardware (Intel OpenGL 4.6), so no driver fix will recover this |
| R16 | Corporate policy blocks Blender installation | Medium | **High** | Portable ZIP in a project folder; written approval first; remote fallback | Approval refused | Open |
| R17 | Asset licence contamination from aggregator sites | Medium | Medium | CC0 sources only for environment; model hero props; record licence per asset | Any asset without provenance | Open |
| R18 | Disk pressure from Blender + assets + frames | High | Medium | Disk guard; purge frames after encode; external SSD option | Free space <15 GB | Open |

## Risk ownership

- **User** owns R1, R4, R6, R7 (policy, facts, rights).
- **Implementation** owns R2, R3, R5, R9, R11, R12.
- **Both** own R8, R10, R13, R14.

## Scoring note

No numeric risk score is assigned. A probability × impact product would imply precision this audit does not have — there is no benchmark, no pilot, and no policy answer. Qualitative bands with explicit triggers are more honest and more actionable.

## Review cadence

1. After B0 — update R2, R3.
2. After the first pilot — update R4, R8, R10.
3. After 10 published videos — update R6, R11, R12.
4. Any time a trigger fires — update the row, not the narrative.
