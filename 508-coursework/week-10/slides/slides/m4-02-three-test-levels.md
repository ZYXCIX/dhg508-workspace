---
minutes: 1.5
---

# Where Unit, Integration, and End-to-End tests sit inside *Bashan*.

<div class="frame fit"><span class="label">Three automated test layers guarding Bashan</span><div class="pic"><Figure id="diag-test-pyramid" /></div></div>

<!--
进入第 4 模块自动化测试！先看这张总图，一秒分清三层测试在巴山轮里各管哪一块：最里面绿色是第一层 Unit Test（单元测试，0.05秒），不联网不开服务，专查单条规则和单个人物 JSON；中间红色是第二层 Integration Test（集成测试，0.3秒），查 CSV 证据表、地图区域和后端接口接在一起对不对；最外圈虚线是第三层 End-to-End Test（Playwright 端到端测试，2秒），真开浏览器点按钮看画面。下一页我们直接看怎么在你们的项目里一步配齐！
-->

::read::
Unit tests check isolated rules (`<0.05s`), integration tests verify cross-file and API contracts (`~0.3s`), and Playwright E2E tests verify the real browser UI (`~2.0s`).
