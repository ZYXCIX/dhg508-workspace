---
minutes: 1.5
---

# This week's steps (before Wed 18 Nov): deploy, test, and share.

<div class="grid" style="--n:3">
<div class="frame hot"><span class="label">01 · Deploy on Cloudflare</span><div class="text">

- ship your current build to **Cloudflare Pages** (`*.pages.dev`, plus Worker if using an API)
- verify the public link opens cleanly on another device

</div></div>
<div class="frame hot"><span class="label">02 · Set up &amp; try testing</span><div class="text">

- recall last week's preview (**evidence check + Browser MCP + API/drift audit**)
- install `Vitest` / `pytest` + `Playwright` and run your **first automated tests**

</div></div>
<div class="frame"><span class="label">03 · Share link with 2 friends</span><div class="text">

- send your live Cloudflare URL to **at least two friends** outside your team and collect their raw bug/UX notes

</div></div>
</div>

<!--
现在把**这周**和**下周**的任务彻底分清楚！先看**这周立刻要做的三件事**：第一，照着刚才那三步把你的项目真正 Deploy 到 Cloudflare Pages 上，拿到公开网址；第二，结合上周预告过的三项检查（史料页码程序核验、Browser MCP 自动试玩、角色偏移检查），把 `Vitest`/`pytest` 和 `Playwright` 装进仓库，跑通第一批自动化测试；第三，把线上链接发给至少两位朋友试玩，收集真实反馈，为下周全面展示做准备！
-->

::read::
This week: (1) deploy your project to a live Cloudflare Pages URL, (2) install `Vitest`/`pytest` + `Playwright` and get your initial data, logic, and browser tests running, and (3) share the live URL with two friends to gather feedback.
