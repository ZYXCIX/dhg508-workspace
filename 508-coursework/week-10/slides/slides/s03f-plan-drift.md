---
minutes: 1.5
---

# Planning prevents goal drifting: lock `docs/plan.md` before launching `/goal`.

<div class="body">
<div class="file"><div class="file-bar">bashan/docs/plan.md</div><pre>
# Bow Deck Plan (Approved)
1. Scope: James Talbot on bashan-anchor only
2. Non-goals: NO Kornai quotes; NO post-Sep 1985 facts
3. Steps:
   - [x] Extract dialogue rules to src/dialogue_rules.py
   - [ ] Wire game/people/expert-1.json to /api/chat
   - [ ] Pass pytest + Playwright smoke check
</pre></div>
<div class="frame hot"><span class="label">Why goals drift without a plan</span><div class="text">

- **Context compaction:** after 20 turns, chat details compress away—`docs/plan.md` on disk never forgets
- **Plan mode first (`Tab`):** agree on steps &amp; non-goals *before* starting `/goal`
- **Checkboxes as state:** the agent ticks `[x]` as each stage passes

</div></div>
</div>

<!--
这里我要特别强调 Planning（规划）和 `/goal` 的关系：Planning 就是 `/goal` 底下最核心的第一步！为什么长任务跑着跑着就会发生 Goal Drifting（目标偏移——比如让你修船头对话，它跑去把餐厅整个重写了，或者把托宾改成了讲价格双轨制）？因为跑了二十轮之后，对话上下文会自动压缩（Compaction），口头聊过的细节就丢了！解决办法：在 OpenCode 里先按 `Tab` 切到 Plan 模式，把范围、红线（Non-goals）和分步清单写进硬盘上的 `docs/plan.md`；你点头确认后，再启动 `/goal` 让它照着勾选完成。下面整堂课讲的 Feedback Loops，就是帮你在写计划时对齐、在跑 `/goal` 时护航！
-->

::read::
Use OpenCode's **Plan** mode (`Tab`) to agree on scope, non-goals, and step checkboxes in `docs/plan.md` before running `/goal`, preventing context compaction from causing goal drift.
