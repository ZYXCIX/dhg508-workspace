---
minutes: 1.5
---

# Testing setup from scratch: install `Vitest` / `pytest` + `Playwright` in 60 seconds.

<div class="body">
<div class="term">
<div class="term-bar"><span>Web / JS Game (Vitest + Playwright)</span></div>
<pre>
<span class="blk">$ npm init -y</span>
<span class="blk">$ npm i -D vitest @playwright/test</span>
<span class="blk">$ npx playwright install chromium</span>
&nbsp;
<span class="dim"># Run unit + integration tests (0.2s):</span>
<span class="blk">$ npx vitest run</span>
<span class="dim"># Run headless browser E2E tests (2s):</span>
<span class="blk">$ npx playwright test</span>
</pre>
<div class="term-foot">package.json: "test": "vitest run &amp;&amp; playwright test"</div>
</div>
<div class="term">
<div class="term-bar"><span>Python Backend + Web (pytest + Playwright)</span></div>
<pre>
<span class="blk">$ uv init &amp;&amp; uv add --dev pytest httpx</span>
<span class="blk">$ npm i -D @playwright/test</span>
<span class="blk">$ npx playwright install chromium</span>
&nbsp;
<span class="dim"># Run Python unit + FastAPI tests:</span>
<span class="blk">$ uv run pytest -q</span>
<span class="dim"># Run headless browser E2E tests:</span>
<span class="blk">$ npx playwright test</span>
</pre>
<div class="term-foot">Unity / Godot: test JSON with pytest + export WebGL</div>
</div>
</div>

<!--
很多同学问：“老师，我的项目现在只有一个文件夹和 HTML/Python，到底怎么从零把 Testing 装起来？”这页左右两栏给你写得明明白白：左边是纯前端或网页游戏，三行命令装好 `vitest` 和 `@playwright/test`；右边是 Python 后端加网页，装好 `pytest`、`httpx` 和 `@playwright/test`。如果你用 Unity 或 Godot，人物 JSON 数据照样用 `pytest` 秒测，导出 WebGL 后用 `npx playwright test` 自动测浏览器运行！装好后直接让 OpenCode 写测试文件就行。
-->

::read::
Initialize automated testing in one minute: install `vitest` (or `pytest` + `httpx`) for unit and integration checks alongside `@playwright/test` (`npx playwright install chromium`) for headless browser verification.
