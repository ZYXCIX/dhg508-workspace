---
minutes: 1.5
---

# Set up `mcp-excalidraw-server` in two lines to catch misunderstandings in 10s.

<div class="body">
<div class="json" data-src="opencode.json · yctimlin/mcp_excalidraw"><pre>
{
  "mcp": {
    "excalidraw": {
      "type": "local",
      "command": [
        "npx", "-y",
        <span class="hl">"mcp-excalidraw-server"</span>
      ],
      "enabled": true
    }
  }
}
// Local canvas: npx -y mcp-excalidraw-server start (:3000)
// Or official MCP App: https://mcp.excalidraw.com (5.6k★)
</pre></div>
<div class="frame hot fit"><span class="label">Round 29 · Misunderstanding caught in 10s</span><div class="pic"><Figure id="vmocc-round24" /></div></div>
</div>

<!--
怎么在你们电脑上把这个 Excalidraw 闭环配起来？非常清楚：左边就是完整的 `opencode.json` 配置——只需要装 `mcp-excalidraw-server`，或者在终端跑一行 `npx -y mcp-excalidraw-server start` 打开本地 3000 端口画板。你看右边我们在第 29 轮抓到的真实事故：Agent 本来误解了我的意思想重画整条走廊，它在画布上一画出来，我十秒钟就喊停作废（画布上还留着它写的“第二十九轮是我误解了——作废，留作对照”），省掉了四小时白做 3D 模型的冤枉功！下一页我现场画给大家看。
-->

::read::
Add `mcp-excalidraw-server` to `opencode.json` and run `npx -y mcp-excalidraw-server start` so both you and your agent share `http://localhost:3000`, catching spatial misunderstandings before 3D or UI coding starts.
