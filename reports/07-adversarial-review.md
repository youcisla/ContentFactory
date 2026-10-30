# 07 — Adversarial Review

Second-pass critique written in the stance of a sceptical senior engineer whose job is to find why this plan fails. Findings are ordered by consequence, not by ease of fixing.

Method: every claim in the plan was treated as a hypothesis, then tested against measurement, primary-source documentation, or repository metadata. Claims that survived are noted in §4. Claims that did not are listed with the change made in `04`.

---

## 1. Findings

### F1 — The candidate repository list was not evidence-based (Critical)

Four of twelve listed projects have 0–17 stars, one has **no licence at all**, one has been stale for 16 months, and the plan omits the category leader (`ahujasid/mcp-for-blender`, 32,783 stars, MIT, pushed daily). A due-diligence list that misses the dominant option and includes unlicensed micro-projects was not produced from repository data.

**Change:** `03` replaces the list with verified metadata and an explicit disposition per project. `hotspoons/blender-agent` is rejected on legal grounds alone.

### F2 — The hardware premise was never tested (Critical)

The plan treats GPU as a "verify later" checkbox and then specifies Cycles-grade 3D output. Measurement shows a single Intel integrated adapter, and the Blender manual states oneAPI requires an **Arc / Xe HPG** card. Cycles is therefore CPU-only on this host.

**Change:** `00` and `01` make CPU-only rendering a stated boundary; `04 §2` routes rendering through CPU or cloud; `04 §13` defines a benchmark whose outcome decides the visual language.

### F3 — The device is corporately managed (Critical, external)

`PartOfDomain = True` on a corporate domain, non-admin shell. The plan's Phase 0 asked whether it was company-managed and then never used the answer. Every installation task in Phase A depends on a permission nobody has confirmed.

**Change:** Stage **A0** inserted ahead of all technical work; `06` makes it the single blocking question.

### F4 — "Automated, reproducible pipeline" contradicts "agent-driven Blender" (High)

An LLM choosing geometry per run cannot be reproducible. The plan's own completion criteria demand reproducible scores while its architecture section leaves room for exactly the opposite.

**Change:** `04 §1` separates the two roles explicitly: deterministic templates in production, MCP only as an authoring accelerator inside a VM. No agent in the publish path.

### F5 — The official Blender MCP is unsafe by the vendor's own admission (High)

The Blender Lab page states the server *"will execute LLM generated code in Blender without any guards in place"* and recommends a VM. Running that on a domain-joined laptop with institutional credentials is an escalation path, not a convenience.

**Change:** `04 §9` isolation table; `02` disposition "DEV SANDBOX ONLY"; `03 §2.2` quotes the warning verbatim.

### F6 — Free TTS is a commercial trap (High)

MoneyPrinterTurbo's free default is Edge TTS — an unofficial endpoint with no licence grant. The plan treats TTS as a solved cost line.

**Change:** `02` rejects it for monetised output; `04 §11` prices licensed TTS; `06 Q4` asks which provider.

### F7 — Licence language was wrong in the plan (Medium)

Remotion and n8n are described as open source. Neither is OSI-approved: Remotion is free only for individuals and ≤3-employee organisations; n8n is fair-code with a service-hosting prohibition.

**Change:** `03 §2.9–2.10` states the exact terms; `02` marks both "CONDITIONAL" / "DEFER"; a re-check trigger is added for the moment the entity changes.

### F8 — YouTube quota facts were stale (Medium)

The plan assumes 10,000 units/day with uploads costing 1,600 units. Current documentation gives `videos.insert` its **own bucket of 100 uploads/day**, separate from the shared 10,000 units.

**Change:** `04 §10` corrects the fact and reframes the real constraint as review capacity, not upload quota.

### F9 — Disk was never budgeted (High)

58.2 GB free, and no phase accounts for EXR frames, proxies, cached assets, or retained masters. A single 8-minute project can exceed 20 GB.

**Change:** disk guard in `04 §6` (refuse <15 GB, abort <8 GB); `06 Q3` asks for an external-storage decision.

### F10 — Unknowns were being scored optimistically (High)

The plan says "an unknown is not a five" but its self-assessment awarded a revised average of 4.8 before any machine or repository evidence existed. Independent scoring of v1.1 is **2.8**, matching the plan's own *draft* figure.

**Change:** `05 §5` records both numbers and labels them subjective; `05 §3` shows the 44.5–80.5 sensitivity band.

### F11 — The fact-checking gate had no enforcement mechanism (High)

The plan asserts human approval of claims, but nothing in a JSON-to-Blender pipeline stops an unverified claim from being narrated. A gate that is a convention is not a gate.

**Change:** `04 §3` makes `claims.json.verified_by_human` a **schema-level precondition**: the renderer refuses scenes referencing unverified claims.

### F12 — Vertical-format specifics were absent (Medium)

The plan correctly forbids auto-cropping but says nothing about safe areas, minimum type size, or composition for 9:16 — the details that decide whether a Short is legible on a phone.

**Change:** `04 §4` adds per-ratio camera fit, safe-area percentages, and minimum text sizes.

### F13 — Benchmark stop conditions referenced telemetry that does not exist (Medium)

The plan asks for "temperature telemetry if already installed". Nothing is installed to provide it, and the audit could not install one.

**Change:** `04 §13` uses measurable substitutes available without new software: wall clock, peak working set, free-disk delta, hard timeout. Thermal risk is handled by time-based stops.

### F14 — Rollback was named but not designed (Medium)

"Rollback" appears as a word in the task table, with no definition of what is restored or how.

**Change:** `04 §15` defines five concrete properties: everything is a file, portable Blender, pinned versions, no destructive automation, manual publish gate.

### F15 — Python ecosystem mismatch (Medium)

Only Python 3.14.6 exists. Several media/ML packages lag that version, and the plan assumes a working Python environment without specifying one.

**Change:** `01 §6` and `04 §14 Stage A` specify a pinned 3.12 environment managed by `uv`, leaving the system interpreter untouched.

### F16 — Cost model omitted the dominant cost (Medium)

The plan's cost section names API credits and ignores human review minutes. At €25/h, review is 95 %+ of marginal cost.

**Change:** `04 §11` separates variable cost from labour and shows labour dominating. `05` adds "cost per approved minute" as the governing metric.

---

## 2. What the plan got right

Worth stating so the revision does not over-correct:

- The **read-only boundary** was the correct instinct and prevented real damage.
- **Separate storyboards for 9:16 and 16:9** — the single most important content decision, already correct.
- **Hard blockers override numeric scores** — the right governance rule; this review relies on it.
- **Distinguishing documented compatibility from measured performance** — exactly why `05` refuses to award points for unrun benchmarks.
- **Requiring explicit approval for benchmarks** — appropriate, and honoured here.

## 3. Residual uncertainty after this review

| Item | Why it remains open |
|---|---|
| Real Cycles CPU throughput | Requires an authorised benchmark |
| EEVEE-on-iGPU viability in background mode | Requires execution |
| Docker daemon health | Starting it is a state change |
| Corporate policy | External to the machine |
| Blender Lab MCP licence | Repository identified, licence file not fetched |
| Actual TTS price | Vendor page is JavaScript-rendered; figure is list-price estimate |
| YouTube account-specific state | Needs the user's channel access |

## 4. Verdict impact

The adversarial pass moved the score **down** (54 from a self-assessed 4.8/5 plan) and moved the plan quality **up** (2.8 → 4.6 subjective), which is the correct direction: an honest plan scores its system lower than its author believed and rates its own completeness higher than its author's first draft.

The recommendation did not change from the first pass — deterministic spine, cloud or CPU render, resolve the host question first — but the reasoning is now anchored to measurements rather than plausible assumptions.
