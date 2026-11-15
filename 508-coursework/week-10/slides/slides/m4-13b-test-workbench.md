---
minutes: 1.5
preload: false
fit: false
---

# Interactive workbench: inject Unit, Integration, and E2E bugs into *Bashan*.

<LazyDemo
  src="./demos/bashan-test-workbench.html"
  badge="INTERACTIVE TEST RUNNER · CLICK TO INJECT REAL BUGS"
  title="Watch Which Test Layer Catches Each Bug in Bashan (1985)"
  summary="Toggle between a unit off-by-one bug (trust above 60), a historical integration bug (Kornai's soft budget constraint leaking into James Tobin), and a broken DOM button listener to see exact pass/fail diffs."
  height={555}
/>

<!--
光看代码不如亲手把程序搞坏一次！点开这个交互工作台，上面有四个按钮：点第二个“注入单元测试 Bug”，把 >= 改成 >，玩家卡在60信任度死活解锁不了，单元测试 0.02 秒直接标红；点第三个“注入集成测试 Bug”，把科尔奈的软预算约束混进托宾的 Prompt，语法和按钮全正常，只有集成测试精准报警；点第四个“注入 E2E Bug”，后端全绿，但前端按钮绑空了，Playwright 当场抓获。
-->

::read::
Use this interactive *Bashan* workbench to inject an off-by-one rule bug, a cross-economist historical contamination bug, and a broken DOM event handler, observing which layer of the test suite catches each failure.
