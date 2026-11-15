---
minutes: 1.5
---

# Browser MCP catches a missing Bashan JSON path and fixes it in one turn.

<div class="term">
<div class="term-bar"><span>OpenCode · bashan</span></div>
<pre>
<span class="you">› Open http://localhost:3090 in Playwright MCP, click Talbot, and check console.</span>
&nbsp;
<span class="tool">● browser_navigate</span>  http://localhost:3090
<span class="tool">● browser_click</span>     ref="npc-talbot"
<span class="tool">● browser_console</span>   <span class="del">404 /people/expert-1.json (missing /game/)</span>
<span class="tool">← Edit</span> src/loader.js  <span class="add">fetch('./game/people/expert-1.json')</span>
<span class="tool">● browser_snapshot</span>  <span class="ok">0 errors · dialogue box 620×184px</span>
<span class="ok">✓ Bow-deck dialogue loads Talbot's card cleanly</span>
</pre>
<div class="term-foot">Build · DeepSeek V4.1 Flash · high</div>
</div>

<!--
看这段巴山轮的真实例子：以前你点开船头的 Talbot 没反应，你可能得猜半天是模型坏了还是点击事件坏了。现在让 OpenCode 自己用 Playwright 打开点一下，它一读 browser_console 立刻看到：404 /people/expert-1.json，少了一层 /game/ 目录！它当场改掉 loader.js，刷新再测，0 报错、对话框不超框，十秒钟闭环修完。
-->

::read::
When OpenCode opens the Bashan bow-deck scene via Playwright MCP, it immediately spots a `404` path error on `expert-1.json` in the browser console, patches `src/loader.js`, and verifies zero errors on reload.
