# Week 9 · 孔子见老子

本周工作：为「孔子与老子对话」的模拟建立史料基础。

## 目前成果

- **史料数据库**：10 种文献、16 条文本、5 条系年异说、2 件碑刻／图像、10 项研究文献。
- **像素对话动画**：`code/dialogue_scene.html`，单文件、离线可用，Minecraft 风格；角色可起身、走动、回席，支持循环和「再谈一轮」。
- **自由对话**：本地即兴池（离线可用）＋可选的 DeepSeek 代理（`code/chat_server.py`）；AI 生成的内容标为「AI 即兴」，不是史料。
- 资料来源：`sources/processed/passages.json`
- 建库与查询：`code/build_db.py`、`code/validate.py`、`code/query.py`
- 技能：`skill/SKILL.md`（索引；检索、维护、原则分在三个文件）
- 生成物：`artifacts/confucius_laozi.db`（不入 git，可重建）
- 说明：`research/notes/source_database.md`、`research/notes/scene_design.md`
- 文献检索记录：`research/references/bibliography.md`（OpenAlex 查询、候选书目、阅读顺序）
- 展示大纲：`research/outputs/slides.md`（Reslides markdown，10 分钟，含讲者备注与计时）

```bash
python code/validate.py
python code/build_db.py
python code/query.py stats
python code/query.py list --topic 问礼
python code/query.py show P04

# 打开动画（直接双击也可以）
python -m http.server 8000
# 然后访问 http://localhost:8000/code/dialogue_scene.html
```

### 自由对话（可选 AI）

不用 AI 也能用：点「自由对话」，会从本地即兴池里抽一段新的对话，输入「礼」「仁」「道」「水」「龙」等词可以换题。

要用 AI 生成，不在 HTML 里写 key，而是走本地代理：

```powershell
$env:DEEPSEEK_API_KEY="sk-..."
python code/chat_server.py
# 打开 http://127.0.0.1:8000/code/dialogue_scene.html
```

没有 key 时，`/api/health` 返回 `{"ok": false}`，页面直接回退到本地即兴池；`/api/chat` 也会返回 503。固定剧本永远不依赖 API。

动画预览参数：

```text
?skip=1                 跳过开场，直接进入对话
?skip=1&still=1&line=9  静态定格在第 9 句（不播放打字机、不做镜头移动）
?end=1                  直接显示结尾字幕
?free=1                 直接进入自由对话
```

## 放进 Reslides

Reslides 仓库的 `package.json` 已把 `dev` 指向：

```text
C:/Users/37391/Desktop/课程/dhg508-workspace/projects/week-09/research/outputs/slides.md
```

在 Reslides 仓库运行：

```powershell
npm.cmd run dev
```

- 正常放映：`http://localhost:3031/`
- 讲者模式与计时：`http://localhost:3031/#/presenter/`
- 总览：`http://localhost:3031/#/overview/`
- 第 3 页的 iframe 使用 `research/outputs/public/dialogue_scene.html`。改了动画后，复制一次：

```powershell
Copy-Item projects\week-09\code\dialogue_scene.html projects\week-09\research\outputs\public\dialogue_scene.html -Force
```

> PowerShell 可能拦截 `npm.ps1`；用 `npm.cmd run dev` 或 `cmd /c npm run dev`。

## 下一步

1. 核对纸本原文与《老子铭》拓片。
2. 补读 Graham、Galambos、巫雪如三项核心研究，并跟进 `research/references/bibliography.md` 里的 K07–K10，记录页码与论点。
3. 把材料分成三个模拟场景：礼学问答（P03–P06）、适周问礼（P01–P02、P13）、仁义与道（P07–P11）。
4. 为每个场景建立人物设定（目标、语气、知识边界），并标明哪些台词有文本依据。

## 项目结构

```text
week-09/
├── research/
│   ├── design/design-document.md
│   ├── journal/research-journal.md
│   ├── notes/
│   │   ├── source_database.md
│   │   └── scene_design.md
│   ├── references/bibliography.md
│   └── outputs/
│       ├── slides.md
│       └── public/dialogue_scene.html
├── sources/
│   ├── raw/
│   └── processed/passages.json
├── artifacts/
│   └── confucius_laozi.db
├── code/
│   ├── build_db.py
│   ├── query.py
│   ├── validate.py
│   ├── dialogue_scene.html
│   └── chat_server.py
└── skill/
    ├── SKILL.md
    ├── what-it-does.md
    ├── how-to-maintain.md
    └── principles.md
```
