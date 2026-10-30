# Claude Code × DeepSeek — Compatibility Audit

As of: **2026-10-30**. Method: read-only local inspection plus vendor documentation. No paid or state-changing test executed.
Status labels: **VERIFIED** (observed locally) · **DOCUMENTED** (vendor docs) · **DOCUMENTED-UNTESTED** (docs claim, no local test) · **UNSUPPORTED** · **UNKNOWN**.

---

## 1. Local environment (VERIFIED)

| Item | Value |
|---|---|
| Claude Code | 2.1.308, `~/.local/bin/claude.exe` |
| Entry point | `claude-vscode` |
| OS | Windows 11, build 26300 |
| Shell | PowerShell 5.1 |
| Node | 26.12.1 |
| SDK version | 0.3.312 |
| Git | clean, branch `main` |

## 2. Provider configuration (VERIFIED)

| Variable | Value |
|---|---|
| `ANTHROPIC_BASE_URL` | `https://api.deepseek.com/anthropic` |
| `ANTHROPIC_MODEL` | `deepseek-flash[1m]` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | `deepseek-flash` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | `deepseek-flash[1m]` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | `deepseek-flash[1m]` |
| `CLAUDE_CODE_SUBAGENT_MODEL` | `deepseek-flash` |
| `CLAUDE_CODE_EFFORT_LEVEL` | `max` |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | `786432` |
| `ANTHROPIC_AUTH_TOKEN` | set (masked; **stored in plaintext in `~/.claude/settings.json`**) |

Settings file (`~/.claude/settings.json`): `model: "opus[1m]"`, `permissions.defaultMode: "default"`, `effortLevel: "xhigh"`, hooks on SessionStart / PreToolUse ×3 / PostToolUse ×2 / UserPromptSubmit / Stop.
No project `.claude/`, no `.mcp.json`, no managed settings file.

This configuration matches DeepSeek's official Claude Code guide exactly [DOCUMENTED].

## 3. Surface area

| Surface | Count | Cost implication |
|---|---:|---|
| Skills | 303 | Large system-prompt footprint |
| Agents | 47 | Definitions loaded on demand; discovery cost |
| Plugins | 12 | Hook/tool surface |
| MCP servers configured | 20+ | Tool schemas occupy context every request |
| Hook scripts | 15 files | Latency and failure modes |

## 4. Compatibility matrix

| Area | Status | Evidence | Notes |
|---|---|---|---|
| Tool calls and tool results | **VERIFIED** | Continuous use this session; DeepSeek docs mark `tools` Fully Supported | `tool_choice: any` treated as `auto`; `tool_choice: {type:"tool"}` returns 400 in thinking mode |
| Thinking / effort | **DOCUMENTED-UNTESTED** | DeepSeek: `thinking` enabled/disabled supported, `adaptive` treated as enabled, `budget_tokens` ignored, `output_config` supports effort only | Both sources set to `max` since 2026-10-30; precedence no longer matters. Cost effect still unmeasured |
| Context limits / compaction | **DOCUMENTED-UNTESTED** | 786,432 window configured | No measurement of compaction behaviour or fidelity |
| Model mapping / billing | **DOCUMENTED / billing UNKNOWN** | `claude-opus*` → `deepseek-v4-pro` at Pro price; `claude-sonnet*`/`claude-haiku*` → `deepseek-flash` | Current opus override keeps traffic on flash; removing it silently changes tier |
| Streaming / retries | **DOCUMENTED** | `stream` Fully Supported | Retry behaviour is client-side, not provider-documented |
| JSON / schema validation | **DOCUMENTED-UNTESTED** | `input_schema` Fully Supported | DeepSeek has a separate JSON Output guide |
| Subagents / worktrees | **DOCUMENTED-UNTESTED** | Claude Code feature; subagent model pinned to `deepseek-flash` | Isolation semantics unchanged by provider |
| Hooks / permissions | **VERIFIED** | Hooks fired repeatedly this session; `defaultMode: default` | Hook failures surface as tool errors, not model-visible reasons |
| MCP integration | **VERIFIED (client-side)** | 20+ servers connected | `mcp_servers` request field is ignored by DeepSeek — MCP is executed by the client |
| Web search / charges | **UNKNOWN** | No documented billing path for provider-side search | Do not invoke paid search without approval |
| Checkpoints / handoffs | **DOCUMENTED-UNTESTED** | `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true` | Session handoff format unverified |
| Prompt injection | **UNSUPPORTED by provider** | No provider-level guarantee | Must be controlled by process and permissions |

## 5. DeepSeek API field support (DOCUMENTED, 2026-10-30)

| Field | Status |
|---|---|
| `model` | Use DeepSeek model name; `claude-*` names are mapped |
| `max_tokens` | Supported but **not a strict limit** — for Claude Code main-agent requests in thinking mode the effective value can exceed the request |
| `thinking` | `enabled` / `disabled`; `adaptive` → enabled; `budget_tokens` ignored |
| `output_config` | Only `effort` supported |
| `cache_control` | **Ignored** |
| `anthropic-beta` | Ignored (except file-source requirement) |
| `mcp_servers` | Ignored |
| `container`, `service_tier` | Ignored |
| `temperature` | 0.0–2.0, fixed at 1.0 in thinking mode |
| `top_p` | Model-dependent; flash lower bound 0.95 in thinking mode |
| `top_k` | Ignored |
| `metadata` | Only `user_id` |
| `stop_sequences` | Fully supported |
| `stream`, `system` | Fully supported |

## 6. Billing analysis

| Fact | Status |
|---|---|
| Claude Code model label is not billing evidence | **CONFIRMED** — label is an alias resolved locally |
| `claude-opus*` maps to `deepseek-v4-pro`, billed at Pro price | **DOCUMENTED** |
| Current config avoids that path via explicit opus override | **VERIFIED** (env) |
| Per-request token usage for this session | **UNKNOWN** — requires provider usage endpoint or dashboard |
| Whether `effort=max` changes cost on flash | **UNKNOWN** — effort is accepted; effect on output tokens unmeasured |
| Prompt caching behaviour | **UNKNOWN** — `cache_control` ignored; DeepSeek may cache automatically |

**Rule derived:** never infer spend from the Claude Code model name. Read the provider dashboard or usage API.

## 7. Risks found

| ID | Risk | Severity | Status |
|---|---|---|---|
| C1 | Auth token stored in plaintext settings file | **High** | **Accepted risk** — user requires in-place token. File is outside the repo and not cloud-synced; an inherited read ACE for a local sandbox group should be denied; agents must not read it |
| C2 | Removing/changing opus override silently routes to Pro billing | **High** | Mitigated by current config; no guard |
| C3 | Effort `max` × 1M context × 300+ skills = unbounded per-request cost | Medium | **Accepted** — user set no spend cap; monitor via provider dashboard |
| C4 | `max_tokens` not enforced as a ceiling | Medium | Open |
| C5 | Hooks block legitimate read-only commands, causing retries | Medium | Observed ~20 times this session |
| C6 | MCP/skill surface inflates every request | Medium | Open |
| C7 | Web search billing path undocumented | Medium | Open |
| C8 | Prompt injection has no provider mitigation | High | Process-only control |

## 8. Unresolved questions

1. ~~Which effort setting wins?~~ **Resolved 2026-10-30:** both set to `max`.
2. Does `effort` measurably change token consumption on `deepseek-flash`?
3. Does Claude Code send `output_config.effort` to this endpoint, or drop it?
4. Is automatic context caching active when `cache_control` is ignored?
5. Is web search available at all on a non-Anthropic endpoint, and at what price?
6. Does a project-level `model` value override env without breaking startup?
7. Are subagent calls billed at the same rate as main-agent calls on this endpoint?

## 9. Minimal safe test suite (proposed — NOT authorised)

| ID | Test | Measures | Est. cost | Approval |
|---|---|---|---|---|
| T1 | Single tool call, read one file | Tool loop integrity | < $0.01 | needed |
| T2 | Same short prompt at effort `low` and `max` | Output tokens, latency | < $0.05 | needed |
| T3 | Request with small `max_tokens` in thinking mode | Whether the ceiling holds | < $0.05 | needed |
| T4 | Spawn one subagent on a trivial task | Subagent model + billing | < $0.05 | needed |
| T5 | Trigger one hook with a benign command | Hook latency and failure mode | $0 | needed |
| T6 | Call one MCP tool once | MCP round-trip | $0 | needed |
| T7 | Long session past 50 % context | Compaction fidelity | < $0.50 | needed |
| T8 | One web search query | Availability + charge | UNKNOWN | **explicit approval** |

None of these may run without the approval recorded in `docs/operations/APPROVAL_GATES.md`.

## 10. Sources

| Source | Retrieved | Use |
|---|---|---|
| https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/ | 2026-10-30 | Official Claude Code setup |
| https://api-docs.deepseek.com/guides/anthropic_api/ | 2026-10-30 | Field support, model mapping |
| https://api-docs.deepseek.com/quick_start/pricing/ | 2026-10-30 | Price structure (account billing not visible) |
| https://code.claude.com/docs/en/settings | 2026-10-30 | Settings precedence, permissions |
| https://code.claude.com/docs/en/model-config | 2026-10-30 | Effort levels, model aliases |

## 11. Prioritised next actions

1. Keep the token in place by user decision; deny inherited read access for the local sandbox group, and rotate on exposure.
2. Add project deny rules for secret files and pushes.
3. Resolve the effort conflict; pick one source of truth.
4. Run T1–T2 only, to establish a cost baseline.
5. Reduce MCP/skill surface for this repository.
6. Record actual spend from the provider dashboard before any further optimisation.
