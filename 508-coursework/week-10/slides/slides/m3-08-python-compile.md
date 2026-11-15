---
minutes: 1.5
---

# Stack four fast Python gates so syntax and type errors die in `0.15s`.

<div class="route">
<div class="step"><p class="what">1 · compileall</p><p class="how">syntax check</p></div>
<div class="arrow">→</div>
<div class="step"><p class="what">2 · ruff check</p><p class="how">undefined names</p></div>
<div class="arrow">→</div>
<div class="step"><p class="what">3 · mypy</p><p class="how">None &amp; dict types</p></div>
<div class="arrow">→</div>
<div class="step red"><p class="what">4 · pytest -q</p><p class="how">unit &amp; API rules</p></div>
</div>

<div class="term">
<div class="term-bar"><span>Terminal · install &amp; run all 4 gates in one command</span></div>
<pre>
<span class="blk">$ uv add --dev ruff mypy pytest fastapi httpx</span>
<span class="blk">$ python3 -m compileall -q src &amp;&amp; uv run ruff check . &amp;&amp; uv run mypy src &amp;&amp; uv run pytest -q</span>
<span class="ok">✓ All checks passed in 0.18s</span>
</pre>
</div>

<!--
如果你的后端或数据处理用的是 Python，它没有传统编译器怎么办？照着这页两行命令配好：一行 `uv add --dev ruff mypy pytest` 装齐工具，然后把 `compileall`、`ruff`、`mypy`、`pytest` 串成一条命令写进你的 `/goal` 里——拼写错、少写了引号、把 `None` 当字典用，0.18 秒内当场拦住！
-->

::read::
Install `ruff`, `mypy`, and `pytest` (`uv add --dev ruff mypy pytest`) and chain `compileall → ruff → mypy → pytest` as a single `0.18s` verification command inside OpenCode.
