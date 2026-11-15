---
layout: process
kicker: Self-verification pipeline
minutes: 1
steps: false
items:
  - { label: "01 · Compile / Build", what: "Syntax & types", how: "py_compile, ruff, mypy, tsc (< 0.2s)" }
  - { label: "02 · Browser View", what: "DOM, console & pixels", how: "Playwright / Chrome DevTools MCP (~1s)", mark: true }
  - { label: "03 · Test Suite", what: "Unit · Integration · E2E", how: "pytest, Vitest, Playwright (~2s)" }
---

# An agent checks cheap static errors first, then live browser state, then full tests.

<!--
Agent 自己排查问题是有先后顺序的，从最快、最便宜的检查往后走：第一步先过 Compile / Build，零点几秒抓出语法错误、拼错的变量名和类型不匹配；第二步打开无头浏览器看一眼 DOM、控制台报错和截图；第三步跑完整的单元、集成和端到端测试。我们先讲浏览器怎么看，再讲 Python 怎么“编译”。
-->

::read::
A fast agent feedback loop layers three checks from cheapest to richest: static compile/type checks in milliseconds, browser inspection in one second, and full automated tests in two seconds.
