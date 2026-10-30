# ADR-0006 — Publication and redaction policy

- Status: proposed
- Date: 2026-10-30
- Deciders: user (sign-off pending), agent (proposal)
- Related: ADR-0005

## Context

This repository is **public**. The audit necessarily inspected a managed device and recorded facts about it. Some facts are technically necessary (hardware limits, disk, absence of a GPU); others identify an employer, a device, or a person and serve no technical purpose.

Git history is permanent. A secret or identifier committed once remains recoverable even after a later deletion.

## Decision

Only technical facts that are load-bearing for a decision may be published. Employer, domain, device model, serial-class identifiers, BIOS version, and personal paths are removed or generalized.

Specifically excluded:

- Employer or institution names, corporate domains, VPN/security-agent vendor names
- Device model, BIOS/firmware versions, serials, hostnames
- Absolute paths containing a username
- Raw audit evidence (`reports/evidence/`, already git-ignored)
- Credentials, tokens, OAuth client files, `.env`
- Screenshots of account consoles or billing pages

Permitted:

- CPU class, core count, RAM size, disk headroom
- Absence of a discrete GPU and its architectural consequence
- OS family and build number
- Benchmark results

## Enforcement

1. `.gitignore` blocks secrets, evidence, media, models, and local state.
2. `CLAUDE.md` and `AGENTS.md` require an explicit check before any commit.
3. Reports are reviewed for identifiers before publication.
4. Any accidental commit of sensitive material is handled by rotating the secret first, then cleaning history — not by a follow-up delete commit.

## Consequences

**Positive:** the repo can be shared for review without exposing an employer or a device fingerprint.

**Negative:** some evidence is less convenient to read; raw captures must be re-fetched.

**Harder:** future audits must separate "technically relevant" from "identifying" while writing, not afterwards.

## Review trigger

If the repository ever becomes private, the redaction burden decreases — but the policy remains, because history may later be made public again.
