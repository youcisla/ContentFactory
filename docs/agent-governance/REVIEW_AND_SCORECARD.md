# Review and Scorecard — Governance Package

Subject: the operating policy, compatibility audit, and instruction patches for Claude Code × DeepSeek.
Scoring is of the **governance design**, not of a running system. Untested runtime behaviour cannot score 5/5.

---

## 1. Rubric

| Criterion | Weight |
|---|---:|
| Correctness and accuracy | 25 |
| Security and compliance | 20 |
| Claude Code / DeepSeek compatibility | 15 |
| Maintainability and simplicity | 15 |
| Cost and resource efficiency | 10 |
| Verification and reproducibility | 10 |
| Documentation clarity | 5 |

## 2. Scores

### Draft v1

| Criterion | Score | Weighted | Basis |
|---|---:|---:|---|
| Correctness | 4 | 20.0 | Facts sourced; some claims still vendor-only |
| Security | 3 | 12.0 | Token at rest not yet mitigated; deny rules absent |
| Compatibility | 3 | 9.0 | Matrix complete but runtime untested |
| Maintainability | 4 | 12.0 | Concise rules; small duplication risk with AGENTS.md |
| Cost | 3 | 6.0 | Effort conflict unresolved; MCP surface large |
| Verification | 4 | 8.0 | Test suite defined, not run |
| Documentation | 5 | 5.0 | Clear, sourced, dated |
| **Total** | | **72.0** | |

### Revised v2 (after adversary passes)

| Criterion | Score | Change |
|---|---:|---|
| Correctness | 4 | Added precise field-support table; removed generalisations |
| Security | 4 | Deny rules proposed; token migration documented |
| Compatibility | 3 | Stays 3 until T1–T2 run |
| Maintainability | 4 | Rules shortened; single source for provider facts |
| Cost | 4 | Effort conflict made explicit; MCP reduction named |
| Verification | 4 | Test suite has cost caps and approval gates |
| Documentation | 5 | — |
| **Total** | **84.0** | |

## 3. Adversarial review A — architecture, security, cost

| # | Challenge | Response |
|---|---|---|
| A1 | Two instruction files will drift | AGENTS.md holds cross-agent rules; CLAUDE.md holds Claude-specific provider facts and links to the audit. Duplication limited to the phase rule |
| A2 | Four governance documents is overengineering | Three documents; each answers a different question (what is true, what is allowed, how good is it) |
| A3 | Deny rules can be bypassed by writing a script | True. Deny rules are a guardrail, not a sandbox; the real control is no secrets in scope |
| A4 | Effort max on a 1M window is the dominant cost | Agreed; policy now defaults to lowest passing effort |
| A5 | Hooks that block reads cost more than they save | Recorded as risk C5; not disabled, because disabling a control is out of scope |
| A6 | Model label could mislead a future maintainer | Explicit rule: label is not billing evidence |

## 4. Adversarial review B — maintainer, security reviewer, solo budget

| # | Challenge | Response |
|---|---|---|
| B1 | 303 skills / 47 agents unmaintainable | Policy requires loading only what a task needs; surface reduction listed as a next action |
| B2 | Token in settings file will leak eventually | High-severity finding; migration steps and rotation guidance documented |
| B3 | Untested compatibility matrix gives false confidence | Every row carries a status; UNKNOWN is explicit; no row claims verification without local evidence |
| B4 | Test suite could itself cost money | Each test has an estimated cap and requires approval |
| B5 | Governance docs add reading burden | Kept short; the policy is ~11 sections, one screen each |

## 5. Hard blockers

| ID | Blocker | Effect |
|---|---|---|
| H1 | Auth token in plaintext settings | **Accepted risk** (user decision) — mitigation: ACL hardening, no agent reads, rotation on exposure. No longer blocks GO |
| H2 | Corporate authorisation | **Closed** — user declaration 2026-10-30 |
| H3 | No runtime compatibility test | Compatibility capped at 3; no 5/5 anywhere |

Hard blockers override the numeric score: **84/100 does not mean GO.**

## 6. What would raise the score

1. Token moved out of settings and rotated → Security 5.
2. T1–T2 executed with recorded token usage → Compatibility 4.
3. Effort precedence tested and pinned to one value → Cost 5.
4. MCP servers trimmed to the ones used in this repo → Cost 5.
5. Independent review of the policy by a second agent → Verification 5.

## 7. Revision log

| Version | Date | Change |
|---|---|---|
| v1 | 2026-10-30 | Initial matrix and policy draft, score 72 |
| v2 | 2026-10-30 | Adversary A and B applied, deny rules and effort policy added, score 84 |
| v3 | 2026-10-30 | Token relocation declined by user; recorded as accepted risk with ACL mitigation. Score unchanged |
| v4 | 2026-10-30 | Effort reconciled to `max` in both env and settings. No spend cap set by user; cost risk accepted. Score unchanged |
| v5 | 2026-10-30 | Corporate authorisation recorded as user declaration; H2 closed. H3 (no runtime test) remains |

## 8. Honest limitations

- No usage or billing data was available; all cost statements are structural, not measured.
- The compatibility matrix reflects vendor documentation on one date; providers change silently.
- The policy cannot enforce itself. It is enforced by permissions, review, and the user.
