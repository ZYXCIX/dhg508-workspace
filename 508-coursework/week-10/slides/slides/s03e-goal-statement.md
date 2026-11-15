---
minutes: 1.5
---

# Write a concrete `/goal` statement anchored to a plan and machine checks.

<div class="body">
<div class="term">
<div class="term-bar"><span>OpenCode · bashan</span></div>
<pre>
<span class="you">/goal Implement Bow Deck dialogue per @docs/plan.md.</span>
<span class="you">Verify every claim against @data/bashan-evidence.csv,</span>
<span class="you">pass pytest -q, and verify 0 console errors in Playwright.</span>
&nbsp;
<span class="blk">◎ Goal: Implement Bow Deck dialogue per @docs/plan.md…</span>
<span class="tool">→ Read</span>   docs/plan.md · data/bashan-evidence.csv
<span class="tool">← Edit</span>   src/dialogue_rules.py · game/people/expert-1.json
<span class="blk">$ pytest -q &amp;&amp; npx playwright test</span>
<span class="ok">◎ goal met · 6 passed, 0 browser errors</span>
</pre>
<div class="term-foot" data-input="/goal pause   |   /goal resume   |   /goal clear">◎ goal met · Build · DeepSeek V4.1 Flash · high</div>
</div>
<div class="frame hot"><span class="label">What backs a good /goal</span><div class="text">

1. **A written file (`@docs/plan.md`)**, never a vague wish
2. **Evidence bounds (`@data/…`)** it must not cross
3. **Executable gates (`pytest`, `Playwright`)** the reviewer can verify

</div></div>
</div>

<!--
那怎么写出一句真正好用的 `/goal` statement（目标声明）？千万不能写 `/goal 把我的游戏做好看一点`——这种没有锚点的口号跑十轮一定彻底跑偏，而且 Reviewer 也不知道什么时候算完！一句合格的 `/goal` 必须带三样支撑：第一，指向你提前对齐好的计划文件 `@docs/plan.md`；第二，指向不可逾越的史料表 `@data/bashan-evidence.csv`；第三，写明机器可验的通关标准（比如 `pytest -q` 全过、Playwright 零报错）。底下状态栏会实时显示 `◎ goal`，随时可以用 `/goal pause`、`resume`、`clear` 控制。
-->

::read::
An effective `/goal` statement binds three things: a written specification (`@docs/plan.md`), explicit source constraints (`@data/bashan-evidence.csv`), and executable test commands (`pytest`, `Playwright`) that prove completion.
