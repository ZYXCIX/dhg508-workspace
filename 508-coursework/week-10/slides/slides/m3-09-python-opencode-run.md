---
minutes: 1
---

# Watch the Python check loop catch a wrong Bashan field name in 0.1 seconds.

<div class="term">
<div class="term-bar"><span>OpenCode · bashan-backend</span></div>
<pre>
<span class="blk">$ python3 -m compileall -q src/ &amp;&amp; ruff check src/ &amp;&amp; mypy --strict src/</span>
<span class="del">src/loader.py:24: error: TypedDict "ResearchMeta" has no key "evidence_tier" (did you mean "evidenceLevel"?) [typeddict-item]</span>
<span class="del">Found 1 error in 1 file (checked 7 source files in 0.11s)</span>
&nbsp;
<span class="tool">← Edit</span> src/loader.py  <span class="dim">evidence_tier → evidenceLevel</span>
<span class="blk">$ python3 -m compileall -q src/ &amp;&amp; ruff check src/ &amp;&amp; mypy --strict src/</span>
<span class="ok">All checks passed!</span>
<span class="ok">Success: no issues found in 7 source files (0.10s)</span>
</pre>
<div class="term-foot">Build · DeepSeek V4.1 Flash · 0.10s</div>
</div>

<!--
大家看终端里发生的事：小模型写代码最常见的毛病就是自己瞎猜字段名，把巴山轮 expert-1.json 里的驼峰命名 evidenceLevel 写成了下划线 evidence_tier。以前你要等到网页端玩家点上去报 500 错误才发现；现在 mypy 零点一秒直接指着第 24 行问它：“你是不是想写 evidenceLevel？”模型自己看一眼立刻改好，全绿通过。
-->

::read::
Running `compileall`, `ruff`, and `mypy` catches hallucinated field names like `evidence_tier` vs `evidenceLevel` in `0.11s`, letting a fast model self-correct immediately.
