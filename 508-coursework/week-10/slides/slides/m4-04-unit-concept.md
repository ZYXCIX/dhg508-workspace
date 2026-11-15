---
minutes: 1
---

# Level 1 · Unit tests check single rules and records with zero external dependencies.

<div class="rows">
<div class="row"><span class="label">No network</span><p class="plain">Never calls OpenRouter or starts an HTTP server; runs offline in under 0.1 seconds</p></div>
<div class="row"><span class="label">Pure input → output</span><p class="plain">Calls one function such as <code>violates_1985_cutoff(prompt)</code> and asserts the exact boolean return</p></div>
<div class="row hot"><span class="label">Historical guardrails</span><p class="plain">Checks every character JSON for <code>据 / 推断 / 设</code> tags and a boundary section</p></div>
</div>

<!--
我们先看第一层：Unit Testing（单元测试）。它的特点是不联网、不调大模型 API、不开网页，单纯给一个函数喂输入、看输出。在数字人文和历史游戏里，单元测试最适合干两件事：第一，测年代防穿越过滤器（比如问 1989 或 1992 南巡，必须拦截）；第二，测每个人物 JSON 的史料字段格式合不合格。
-->

::read::
Unit tests run offline in under `0.1s` with no servers or API calls, checking pure functions such as anachronism filters and character schema rules.
