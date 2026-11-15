---
minutes: 1
class: compact
---

# Every stack in our class has a single one-line build gate for AGENTS.md.

| Project stack | Exact build / compile command to put in `AGENTS.md` | Speed |
|---|---|---|
| **Python backend / scripts** | `python3 -m compileall -q . && ruff check . && mypy src/` | `~0.15s` |
| **TypeScript / React / Vite web** | `npx tsc --noEmit && npm run build` | `~1.5s` |
| **Reslides deck / academic site** | `npm run check` (validates JSX, `refs.bib`, `figures.yaml`, timing) | `~2.0s` |
| **Godot 4 game** | `godot --headless --check-only --script res://scripts/main.gd` | `~0.8s` |
| **Unity 3D (*Bashan*)** | `Unity -batchmode -nographics -quit -projectPath . -logFile -` | `~6–12s` |

<!--
不管你做的是哪种项目，今天下课第一件事，就是从这张表里把属于你的那一行抄进你仓库根目录的 AGENTS.md 里，写明：“每次修改代码后必须先跑通这条 build 命令。”不管是 Python、前端 Vite、Godot 还是巴山轮用的 Unity batchmode，都有对应的无人值守编译门槛。
-->

::read::
Every project stack—Python, TypeScript/Vite, Reslides, Godot, and Unity—provides a CLI compile/build gate that should be mandated in `AGENTS.md`.
