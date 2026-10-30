# ADR-0003 — Direct YouTube API for publishing

- Status: proposed
- Date: 2026-10-30
- Deciders: user (sign-off pending), agent (proposal)
- Related: `reports/v2/03`

## Context

Three self-hosted alternatives to Blotato were evaluated:

| Tool | Licence | YouTube support | Idle footprint |
|---|---|---|---|
| Postiz | AGPL-3.0 | **No provider found in OSS tree** | 0.5–1.5 GB |
| OpenPost | AGPL-3.0 | Yes (integration doc + code) | 0.5–1.5 GB |
| Mixpost | MIT core | Yes (per vendor site) | 0.4–1.2 GB |
| Direct YouTube API | Google terms | Native | 0 |

The channel publishes to YouTube only. The stated operating preference is zero idle consumption and portable on-demand processes.

Verified quota facts: `videos.insert` has its own bucket of **100 uploads/day**; other endpoints share 10,000 units/day. `captions.insert` costs 400 units — caption uploads are the expensive call.

## Decision

Publish through the **YouTube Data API v3 directly**, from a small script. Perform the first ten uploads **manually** to avoid OAuth and API-audit risk while the format is still changing.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Postiz | Cannot publish to YouTube in the open-source edition; always-on stack |
| OpenPost | Viable but young (839 stars); always-on; only justified by multi-platform need |
| Mixpost | Stale (last push ~7 months); Pro features paid; always-on Laravel stack |
| Blotato (SaaS) | Closed, subscription, data leaves the device; not auditable |

## Consequences

**Positive:** no service, no idle RAM, no third-party licence, one fewer failure mode. Upload volume is not a constraint — review capacity is.

**Negative:** platform-specific code; any future multi-platform need requires a new tool.

**Harder:** OAuth token handling must be done carefully. Tokens are secrets and never enter the repository.

## Conditions

1. Manual upload for the first ten videos.
2. Verify the project's API audit status before automating — unaudited projects may have uploads restricted.
3. Set the AI-disclosure flag at upload when content is realistic synthetic media.
4. Credentials live outside the repo; `.gitignore` already blocks common token filenames.

## Evidence

- `reports/v2/03-publishing-tools-v2.md`
- `reports/evidence/youtube-quota.html` (ignored raw capture; quota facts above)
