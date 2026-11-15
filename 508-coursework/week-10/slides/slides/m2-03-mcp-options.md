---
minutes: 1
class: compact
---

# Three widely used ways to coordinate specialist coding agents.

| Option | How it works | Best when |
|---|---|---|
| **OpenCode Subagents** (`.opencode/agents/*.md`) | Built-in `@researcher` / `@reviewer` roles invoked inside OpenCode (`0` plugins) | One student delegating read-only source checks |
| **`Dicklesworthstone/mcp_agent_mail_rust`** (`2.5k★`) | Local Git + SQLite MCP mail (`send_message`, `fetch_inbox`, advisory file leases) | Two independent terminals working asynchronously |
| **`bcurts/agentchattr`** (`1.6k★`) | Local Web UI (`:8300`) + MCP room; `@mention` auto-wakes peer terminals | Live group chat across Claude Code, Codex &amp; OpenCode |

<!--
我专门为大家核查了目前开源社区最主流、维护最活跃的三种多 Agent 协同方案：第一种根本不用装任何第三方插件——直接用 OpenCode 自带的 `.opencode/agents/researcher.md` 子代理，在对话框里 `@researcher` 就能让它只读查史料；第二种是目前 GitHub 上最火的多 Agent 异步协调 MCP **MCP Agent Mail**（2500+ 星，Rust 重写版），提供收发信箱和文件防冲突锁；第三种是 **agentchattr**（1600+ 星），自带本地 8300 端口网页群聊，你在里面 `@` 哪个终端，它就会自动唤醒那个终端干活！
-->

::read::
Choose from three active, battle-tested setups: built-in OpenCode subagents (`.opencode/agents/researcher.md`), **MCP Agent Mail** (`Dicklesworthstone/mcp_agent_mail_rust`, `2.5k★`) for asynchronous inboxes and file leases, or **agentchattr** (`bcurts/agentchattr`, `1.6k★`) for live `@mention` wakeups.
