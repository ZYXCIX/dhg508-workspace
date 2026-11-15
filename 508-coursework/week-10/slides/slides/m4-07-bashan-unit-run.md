---
minutes: 1
---

# Unit tests fail with exact pinpointing when an agent drops a citation.

<div class="term">
<div class="term-bar"><span>OpenCode · bashan</span></div>
<pre>
<span class="blk">$ pytest tests/test_unit.py -q</span>
<span class="del">F..                                                                 [100%]</span>
<span class="del">E   AssertionError: economist-1.json position[2] has empty research.ref</span>
<span class="dim">1 failed, 2 passed in 0.08s</span>
&nbsp;
<span class="tool">→ Read</span> materials/annotations/secondary-weber-gewirtz.md
<span class="tool">← Edit</span> game/people/economist-1.json  <span class="add">"ref": "Weber 2021, p. 195; 项怀诚自述 P6, P11"</span>
<span class="blk">$ pytest tests/test_unit.py -q</span>
<span class="ok">...                                                                 [100%]</span>
<span class="ok">3 passed in 0.07s</span>
</pre>
<div class="term-foot">Build · DeepSeek V4.1 Flash · 0.07s</div>
</div>

<!--
看跑起来的效果：Agent 给中方官员加了一条新观点，但偷懒漏写了 research.ref 出处。pytest 零点零八秒直接标红：economist-1.json 第 2 条立场的 ref 为空！Agent 马上回去查 Weber 2021 第 195 页和项怀诚自述的笔记，把页码补齐，再跑一遍 0.07 秒全绿。
-->

::read::
When an edit leaves `research.ref` blank on a new character position, `pytest` catches it in `0.08s` and forces the agent to restore the exact source locator from the research notes.
