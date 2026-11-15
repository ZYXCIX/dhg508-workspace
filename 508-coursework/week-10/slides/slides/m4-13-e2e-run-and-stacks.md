---
minutes: 1.5
---

# Pick the exact testing recipe that matches your project's technology stack.

<Tabs labels="Python + Web App | HTML / JS / Canvas Game | Unity / Godot Engine">
<div>

- **Compile gate**: `python3 -m compileall -q . && ruff check . && mypy src/`
- **Unit & Integration**: `pytest -q` (pure functions + `FastAPI TestClient` / `Flask test_client`)
- **End-to-End & Visual**: `npx playwright test` against `localhost`

</div>
<div>

- **Architecture rule**: Move game state & dialogue out of `index.html` into `src/state.js`
- **Unit & Integration**: `npx vitest run` checking `src/state.js` and all `.json` / `.csv` files
- **End-to-End & Visual**: `npx playwright test` checking `pageerror`, `404` assets, and canvas/UI screenshots

</div>
<div>

- **Unit & Data (`< 0.1s`)**: Keep NPC cards & evidence in `.json` / `.csv` and test with `pytest` or `Vitest`
- **Engine Integration**: Unity Test Framework (`Unity -batchmode -runTests`) or Godot `GUT` (`godot --headless`)
- **WebGL Export E2E**: Run `npx playwright test` on your exported HTML5/WebGL folder before deploying

</div>
</Tabs>

<!--
我用新版 reslides 的交互式 Tabs 组件把班上三大类项目的测试配方全列好了，大家对号入座：第一类 Python 加网页，用 ruff + mypy + pytest + Playwright；第二类纯网页或 Canvas/Three.js 游戏，把状态抽出来用 Vitest 测逻辑、Playwright 测画面；第三类 Unity 或 Godot 引擎，人物 JSON 照样用 pytest 秒测，引擎逻辑用 headless CLI 跑，导出成 WebGL 后再用 Playwright 冒烟测试。
-->

::read::
Every student project archetype—Python web apps, HTML/Canvas games, and Unity/Godot builds—maps cleanly onto a three-tier compile, unit/integration, and Playwright E2E workflow.
