---
minutes: 1.5
---

# OpenCode `/goal` runs across turns until an internal reviewer checks done.

<div class="frame fit"><span class="label">OpenCode PR #59437 · /goal execution architecture</span><div class="pic"><Figure id="diag-goal-loop" /></div></div>

::foot::
Source: `github.com/anomalyco/opencode/pull/59437` (merged two weeks ago)

<!--
过去大家用 OpenCode，它是“你说一句、它动一下就停了”，你得一直在旁边盯着催它。就在刚过去这一两周，OpenCode 正式合入了全新的 `/goal` 功能（PR #59437）！它的本质原理看这张图就全明白了：当你输入 `/goal <目标>`，整个长任务在同一个执行流里跑。每当模型干完一轮活准备停下来（Session `idle` 钩子触发）时，内置的 Reviewer 会读取完整的工具运行输出，判断目标到底达成了没有：没达成但有进展，就自动注入隐藏的 `continue` 指令重申目标继续干；连卡 3 轮没进展自动暂停防烧钱；只有测试全绿、真正达标，才亮起绿灯 `◎ goal met` 通知你！
-->

::read::
Merged in OpenCode PR `#59437`, `/goal <objective>` intercepts the session `idle` boundary and runs an internal reviewer over tool outputs—continuing automatically until the objective is verified `done` or pausing after 3 stalled rounds.
