---
minutes: 1.5
---

# Browser MCP turns invisible UI bugs into four machine-readable signals.

<div class="body">
<div class="browser">
<div class="browser-bar"><span class="url">http://localhost:3090/bow-deck · 3 bugs on screen</span></div>
<div class="browser-body">
<h3>James Talbot · Bow Deck (Sep 1985)</h3>
<p>[404 Broken Image: /people/tobin.jpg]</p>
<p>“Indirect levers—interest rates and reserve requirements—only work when commercial banks…” <b>[Text clipped at 92px! Button overlapping!]</b></p>
<p><span class="del">Console TypeError: Cannot read properties of null ('addEventListener')</span></p>
</div>
</div>
<div class="frame hot"><span class="label">What @playwright/mcp sees at once</span><div class="text">

1. **DOM geometry:** `scrollHeight (148) > clientHeight (92)` → clipped!
2. **Console errors:** `TypeError` at `bow-deck.js:42`
3. **Network log:** `404` on `/people/tobin.jpg`
4. **Screenshot:** vision check at `1280×720`

</div></div>
</div>

<!--
为什么一定要给 Agent 配上 Browser Feedback？左边是同学们平时最头疼的页面毛病：头像路径写错 404 裂了、对话框高度写死导致字被截断按钮重叠、点按钮没反应因为控制台报了空指针错。装上 `@playwright/mcp` 后，右边这四路信号同时喂进 Agent 的上下文里，不用你截图贴报错，它自己一轮全修好！下一页看具体怎么配。
-->

::read::
Connecting `@playwright/mcp` gives the agent simultaneous access to clipped DOM dimensions (`scrollHeight > clientHeight`), JavaScript console exceptions, `404` network requests, and `1280×720` screenshots.
