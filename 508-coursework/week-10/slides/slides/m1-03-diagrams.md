---
minutes: 1
---

# Ideation 2 · Have the agent draw a Mermaid state diagram to check logic branches.

<div class="body">
<div class="frame fit wide"><span class="label">Rendered Mermaid flowchart · docs/bow-flow.md</span><div class="pic"><Figure id="diag-mermaid-bow" /></div></div>
<div class="frame hot"><span class="label">What Mermaid catches</span><div class="text">

- **Dead-end states:** every refusal loops back cleanly to `Player Question`
- **Gate rules:** `Trust ≥ 60` required before unlocking `TOBIN-02`
- **Limit:** shows logic arrows, **not** room scale or floor plans

</div></div>
</div>

<!--
第二招：当你的对话或网页有分支逻辑时，光靠文字看不出死胡同，让 Agent 在 Markdown 里写一段 `mermaid` 代码画成右边这样的状态流程图！大家看这张真实的巴山轮船头流程图：玩家提问后先判断年份——如果是 1985 年 9 月之后的事，走右边红框拦截并虚线回到提问框，绝不会卡死；如果是当时的宏观调控问题，引用托宾第 152、157 页讲话，并且信任度达到 60 才解锁笔记本词条。逻辑一目了然！但如果要讨论展厅多大、桌子怎么摆，Mermaid 就画不出来了——这就轮到第三招 Excalidraw。
-->

::read::
Ask the agent for a `mermaid` state flowchart in Markdown to inspect dialogue branches, historical cutoff loops, and unlock conditions visually before implementation.
