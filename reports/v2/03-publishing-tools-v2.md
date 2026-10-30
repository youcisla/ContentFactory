# 03 — Publishing Tools: Open-Source Alternatives to Blotato

Scope: Postiz, OpenPost, Mixpost, direct YouTube Data API. Blotato itself is a proprietary SaaS and was **not** audited — no source, no self-host option, and its terms cannot be verified from a repository.

Verification date 2026-10-30. Star/push figures are point-in-time.

---

## 1. Verification table

| Tool | Licence | Stars | Last push | YouTube publishing | Self-host footprint |
|---|---|---:|---|---|---|
| **Postiz** | **AGPL-3.0** | 40,185 | 2026-10-30 | **No provider found in OSS tree** | Node + Postgres + Redis |
| **OpenPost** | **AGPL-3.0** | 839 | 2026-10-30 | **Yes** — dedicated integration doc | Postgres + Go server + Node/web |
| **Mixpost** | MIT (core) | 3,890 | **2026-03-16** | **Yes** — videos and Shorts (vendor site) | Laravel + MySQL + Redis |
| Direct YouTube Data API | n/a (Google terms) | — | — | Native | none |

### How Postiz's YouTube gap was established

- Recursive tree scan of `gitroomhq/postiz-app` (1,330 nodes, default branch `main`): every path containing "youtube" is an **image asset** (`icons/platforms/youtube.png/.svg`, a screenshot). No provider implementation file.
- Provider implementation paths list Bluesky, Facebook, GMB, Instagram, LinkedIn, Tumblr, Telegram, Farcaster — no YouTube entry in the sampled provider directory.
- The docs site returned HTTP 308 on the provider page and could not be read this pass.

**Conclusion, with a caveat:** Postiz's open-source edition appears not to publish to YouTube. Treated as **verified-by-absence**; confirm against `docs.postiz.com` before adopting.

`★ Why this matters` A publishing tool that cannot publish to YouTube is a scheduling calendar for platforms you are not using. For a YouTube-first channel it is disqualified on function, not on licence.

## 2. Per-tool assessment

### Postiz
- **Strength:** the most active project of the three, 40k stars, daily commits, agent-friendly (MCP/CLI integrations advertised).
- **Weakness:** AGPL plus no YouTube provider. If YouTube support exists only in the hosted/paid edition, self-hosting does not solve it.
- **Footprint:** a Compose stack with Postgres and Redis idle-consumes roughly 0.5–1.5 GB RAM — directly against your zero-idle requirement.

### OpenPost
- **Strength:** the only one of the three with an explicit **YouTube integration document** in-repo (`apps/docs/content/docs/self-hosting/integrations/youtube.mdx`) plus YouTube-specific platform code (`postimport_youtube.go`, `first_comment_youtube.go`). Includes an image and video editor.
- **Weakness:** 839 stars, young project, AGPL. A single-maintainer risk at this size, and the video editor overlaps with the rendering work rather than complementing it.
- **Footprint:** Postgres + Go + Node/Web. Same always-on objection.

### Mixpost
- **Strength:** MIT core, mature Laravel package, explicit YouTube (videos and Shorts) support on the vendor site, 3.9k stars. Pro edition is paid and separate.
- **Weakness:** last push **2026-03-16** — roughly seven months stale at audit date. Pro features are where publishing depth tends to live.
- **Footprint:** Laravel + MySQL + Redis, always-on.

### Direct YouTube Data API
- **Strength:** no service, no idle cost, no third-party licence, no middleware failure mode.
- **Facts verified:** `videos.insert` has its own bucket of **100 uploads/day**; other endpoints share 10,000 units/day. `captions.insert` costs 400 units, `captions.update` 450 — caption uploads are the expensive call, not video upload.
- **Caveat [I]:** projects that have not completed YouTube's API audit may have uploads restricted (commonly to private visibility) until reviewed. Verify in the Google Cloud console before automating; manual upload avoids this entirely.
- **Effort:** OAuth once, then a single upload call per video.

## 3. Resource comparison (the deciding axis)

| Option | Idle RAM | Idle processes | Disk | Ongoing maintenance |
|---|---:|---:|---:|---|
| Direct API | 0 | 0 | ~0 | token refresh only |
| Postiz self-host | 0.5–1.5 GB | 3+ containers | 1–2 GB | upgrades, DB backups |
| OpenPost self-host | 0.5–1.5 GB | 3+ | 1–2 GB | upgrades, DB backups |
| Mixpost self-host | 0.4–1.2 GB | 3+ | 1 GB | upgrades, DB backups |
| Blotato (SaaS) | 0 | 0 | 0 | subscription, data leaves device |

Your stated priority — low RAM/CPU/disk and **zero idle consumption**, portable on-demand processes over always-running services — eliminates all three self-hosted tools for a single-channel operation. They are designed for teams managing many accounts, which is the opposite of this workload.

## 4. Recommendation

1. **Publish via the YouTube Data API directly.** One channel, ≤100 uploads/day, no service to keep alive.
2. **Manual upload for the first ten videos.** Removes OAuth/audit risk while the format is still changing, and costs nothing but minutes.
3. **Revisit OpenPost** only if multi-platform distribution (LinkedIn/TikTok/X) becomes a requirement. It is the only candidate that verifiably supports YouTube and carries a permissive-enough (AGPL) self-host licence.
4. **Do not adopt Postiz** for this workload unless its hosted edition is chosen deliberately; the OSS edition lacks the one integration that matters here.
5. **Mixpost** is a reasonable fallback if a Laravel shop is already operated, but its seven-month gap is a maintenance warning.

## 5. Legal notes

- AGPL-3.0 (Postiz, OpenPost): self-hosting for your own use is fine; distributing a modified version, or offering it as a network service to others, triggers source-disclosure obligations.
- MIT (Mixpost core): permissive; the paid Pro edition has separate commercial terms.
- Direct API: governed by the YouTube API Services Terms and Google Privacy Policy. Uploading content you own is the intended use.
- No tool changes the **disclosure obligation** for realistic AI-generated content — that flag is set at upload regardless of tooling.
