---
minutes: 1.5
---

# Worked example · Turning a friend's Bashan playtest into code and a test.

<div class="route">
<div class="step"><span class="yr">01 · Friend's feedback</span><p class="what">"Double-clicking Send fired two overlapping replies from Talbot"</p><p class="how">recorded in `docs/user-feedback.md`</p></div>
<div class="arrow">→</div>
<div class="step"><span class="yr">02 · Code integration</span><p class="what">Disable Send button while `inFlight === true`</p><p class="how">patched in `src/chat-ui.ts`</p></div>
<div class="arrow">→</div>
<div class="step red"><span class="yr">03 · New E2E test</span><p class="what">`dblclick('#chat-send')` asserts `apiCalls === 1`</p><p class="how">saved forever in `tests/e2e_bow_deck.spec.ts`</p></div>
</div>

<p class="sub">Every real human bug report becomes one permanent automated assertion.</p>

<!--
我用巴山轮给大家举一个完整的示范，什么叫“把朋友的反馈落到 test 里”：比如我把巴山轮线上链接发给朋友玩，朋友反馈说：“船头网络慢一点的时候，我连点两下发送键，Talbot 同时回了我两段重叠的话。”第一步，记进 user-feedback.md；第二步，在前端代码里加上请求未返回时禁用发送按钮；第三步，在 Playwright E2E 测试里专门加一条测试：模拟快速双击发送按钮，断言后端 API 只收到 1 次请求！从此这个 bug 永远不可能再犯。下周大家就照这个标准交作业！
-->

::read::
When a playtester reports a concrete issue—such as double-clicking Send triggering duplicate NPC replies—you record the feedback, ship the UI fix, and add a permanent Playwright test asserting `apiCalls === 1` on rapid clicks.
