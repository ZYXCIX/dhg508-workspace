---
minutes: 1
---

# Set up OpenCode subagents or `mcp-agent-mail` in one config file.

<div class="body">
<div class="file"><div class="file-bar">.opencode/agents/researcher.md (zero-install subagent)</div><pre>
<span class="dim">---</span>
description: Verify claims strictly against materials/ &amp; refs.bib
mode: subagent
permission:
  edit: deny
<span class="dim">---</span>
Answer historical source questions with exact page numbers.
Never edit game code.
</pre></div>
<div class="json" data-src="opencode.json · or connect two terminals via MCP Agent Mail"><pre>
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "agent_mail": {
      "type": "remote",
      "url": <span class="hl">"http://127.0.0.1:8765/mcp/"</span>,
      "enabled": true
    }
  }
}
// Terminal: mcp-agent-mail serve (auto-configured by am)
</pre></div>
</div>

<!--
具体怎么配？给你们两个最干净的真实配置：左边是零安装的 OpenCode 原生方案——在项目里建一个 `.opencode/agents/researcher.md`，设成 `edit: deny`（禁止改代码，只准读史料），写代码时随时 `@researcher` 提问；如果你开了两个独立终端想让它们互发邮件、互相锁文件防覆盖，就用右边的 `mcp-agent-mail`，一行命令启动本地 `8765` 端口，两个窗口都连上就能异步收发信件了！
-->

::read::
For single-window delegation, drop a read-only subagent Markdown file in `.opencode/agents/researcher.md` and invoke `@researcher`; for multi-terminal coordination, point `opencode.json` at a local `mcp-agent-mail` server (`http://127.0.0.1:8765/mcp/`).
