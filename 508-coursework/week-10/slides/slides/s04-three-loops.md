---
minutes: 1
---

# Two feedback loops keep `/goal` on track: Ideation first, Verification second.

<div class="frame fit"><span class="label">Ideation before code · Verification during /goal</span><div class="pic"><Figure id="diag-two-loops" /></div></div>

<!--
现在把整张地图拼起来看，逻辑就无比顺畅了：要让 Agent 长时间跑 `/goal` 不跑偏，你需要前后两套 Feedback Loop。左边第一套叫 **Ideation Loop（构思探索闭环）**，发生在写一行代码之前——通过言语互述、Mermaid 流程图、Excalidraw 画板和 HTML 架构示意图，确保你和 Agent 想的是同一件事，从而产出靠谱的 `plan.md`。右边第二套叫 **Verification Loop（执行验证闭环）**，发生在跑 `/goal` 的过程里——Agent 互查史料、编译器与浏览器自动看画面、三层自动化测试把关。
-->

::read::
Preventing goal drift requires two complementary loops: an **Ideation Loop** before coding (to align intent and produce `docs/plan.md`) and a **Verification Loop** during `/goal` execution (to catch historical, visual, and code regressions).
