---
minutes: 1
---

# Level 2 · Integration tests verify that separate modules agree at their seams.

<div class="route">
<div class="step"><span class="yr">Module A</span><p class="what">bashan-evidence.csv</p><p class="how">researcher's claim &amp; page table</p></div>
<div class="arrow">↔</div>
<div class="step"><span class="yr">Module B</span><p class="what">expert-1.json + world.json</p><p class="how">character cards &amp; scene anchors</p></div>
<div class="arrow">↔</div>
<div class="step red"><span class="yr">Module C</span><p class="what">POST /api/chat</p><p class="how">prompt builder &amp; JSON response</p></div>
</div>

<p class="sub">Each file can pass unit tests alone and still break where two files meet.</p>

<!--
再看第二层：Integration Testing（集成测试）。为什么光有单元测试还不够？因为你可能 CSV 自身格式是对的，JSON 自身格式也是对的，后端函数也没语法错，但三者接在一起时：CSV 里写的锚点叫 bashan-anchor，world.json 里改名叫 bow-deck 了，或者后端接口返回了 reply 字段但前端读的是 message 字段！集成测试专门抓模块拼接处的错位。
-->

::read::
Integration tests verify the seams between modules—ensuring `data/bashan-evidence.csv`, character/scene JSON files, and the `/api/chat` backend agree on IDs, locators, and response shapes.
