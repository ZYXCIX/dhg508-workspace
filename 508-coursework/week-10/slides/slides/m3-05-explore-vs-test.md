---
layout: compare
kicker: Crucial distinction
minutes: 1.5
steps: false
left:
  title: Exploratory browser feedback
  items:
    - Agent opens browser interactively via MCP while building a new feature
    - Clicks around, inspects layout, tweaks CSS colours and spacing live
    - Ephemeral — vanishes once the chat turn ends
right:
  title: Test browser feedback
  items:
    - Agent saves those exact browser checks into tests/bow-smoke.spec.ts
    - Asserts 0 console errors, 0 broken 404s, and no text clipping
    - Permanent — re-runs in 2 seconds after every future edit
verdict: Use exploratory browser feedback to design; lock the result into test feedback so tomorrow's edit cannot break today's scene.
---

# Distinguish live browser exploration from repeatable browser test feedback.

<!--
这里大家一定要分清两种截然不同的浏览器 feedback！第一种叫探索式 feedback（观看）：你刚做船头对话框，让 agent 用 MCP 打开浏览器看一眼好不好看、字挤不挤，调完就完了，这跟人看一眼一样是一次性的。第二种叫测试 feedback：调好之后，必须让 agent 把刚才看的条件写进 Playwright 测试脚本！这样下周你去改餐厅场景时，跑一遍测试，立刻知道船头场景有没有被意外改坏。
-->

::read::
Interactive browser MCP exploration helps build and polish a UI once, whereas saved Playwright browser tests permanently guard against regressions on every subsequent edit.
