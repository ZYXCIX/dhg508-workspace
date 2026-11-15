---
minutes: 1.5
---

# Browser feedback setup: two commands + one `opencode.json` block.

<div class="body">
<div class="term">
<div class="term-bar"><span>Step 1 · Install Chromium once</span></div>
<pre>
<span class="blk">$ npx playwright install chromium</span>
<span class="ok">✓ Chromium downloaded for headless &amp; MCP runs</span>
&nbsp;
<span class="you">› Start my local dev server in the background, open it</span>
<span class="you">  with playwright MCP, click through the main flow,</span>
<span class="you">  and fix any console, 404, or layout overflow errors.</span>
</pre>
<div class="term-foot">Build · DeepSeek V4.1 Flash · high</div>
</div>
<div class="json" data-src="Step 2 · opencode.json (project root)"><pre>
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "playwright": {
      "type": "local",
      "command": [
        "npx", "-y",
        <span class="hl">"@playwright/mcp@latest"</span>,
        "--headless"
      ],
      "enabled": true
    }
  }
}
</pre></div>
</div>

<!--
请大家把这一页拍下来或者直接复制走——这就是 Browser Feedback 完整、零死角的 Setup 步骤：第一步，在项目终端跑一次 `npx playwright install chromium` 把浏览器内核装好；第二步，在项目根目录建一个 `opencode.json`，把右边这段 `@playwright/mcp@latest` 粘进去。重启 OpenCode 后，直接发左边底下那句提示词，浏览器就能全自动跑起来了！
-->

::read::
To set up automatic browser feedback: run `npx playwright install chromium` once, add `@playwright/mcp@latest` to `opencode.json`, and instruct OpenCode to open your local server and fix all console, `404`, and overflow errors.
