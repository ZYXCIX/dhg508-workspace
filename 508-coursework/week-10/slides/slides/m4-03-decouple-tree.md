---
minutes: 1
---

# Separate data and pure logic from the UI so all three test levels stay easy.

<div class="body">
<div class="tree"><span class="label">bashan/</span><pre>
├─ data/bashan-evidence.csv  <span class="dim">claims &amp; pages</span>
├─ game/people/expert-1.json <span class="dim">Talbot's card</span>
├─ src/dialogue_rules.py     <span class="hl">pure logic (0.05s)</span>
├─ src/server.py             <span class="hl">API route</span>
└─ tests/
   ├─ test_unit.py           <span class="hl">01 · unit</span>
   ├─ test_integration.py    <span class="hl">02 · integration</span>
   └─ e2e_bow_deck.spec.ts   <span class="hl">03 · browser E2E</span>
</pre></div>
<div class="frame hot"><span class="label">Golden rule</span><div class="text">

- **never** bury dialogue trees and year cutoffs inside a 2,000-line `index.html` script
- keep rules in `src/` and historical facts in `.json` / `.csv`

</div></div>
</div>

<!--
要写出好测的项目，前提是目录结构不能糊成一团。大家看巴山轮的目录树：如果你把所有对话词、年份判断全塞在 index.html 一个两千行的 script 标签里，那就没法做单元测试了。把历史证据放在 CSV、人物设定放在 JSON、判断规则抽成独立的 dialogue_rules.py 或 state.js，三层测试自然就清晰了。
-->

::read::
Keeping historical evidence in CSV/JSON files and dialogue rules in standalone modules—separate from HTML/Canvas rendering—makes unit, integration, and E2E tests clean and fast.
