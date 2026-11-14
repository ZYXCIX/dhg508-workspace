# 孔子见老子 · 史料数据库

> 目的：把「孔子见老子」的各种记载集中起来，标明出处、文类与年代层次，为后续的对话模拟提供一个可查、可核对的材料库。

## 这是什么

| 项目 | 数量 |
|---|---|
| 文献 | 10 种 |
| 文本条目 | 16 条 |
| 主题 | 9 个 |
| 系年异说 | 5 条 |
| 碑刻／图像 | 2 件 |
| 研究文献 | 10 项（3 项核心，7 项线索） |

这不是「孔子真的见过老子」的证明，而是「关于会面的记载如何一层一层形成」的材料库。同一件事在不同文献里的年代、地点、对话都不一样；数据库保留差异，不替它们合并成一个和谐的故事。

## 快速使用

```bash
# 1. 由 JSON 建立 SQLite（输出到 artifacts/，该目录不入 git）
python code/build_db.py

# 2. 查询
python code/query.py stats          # 总览
python code/query.py sources        # 文献列表
python code/query.py topics         # 主题列表
python code/query.py list           # 全部条目
python code/query.py list --topic 问礼
python code/query.py list --source S03
python code/query.py search 仁义
python code/query.py show P04
python code/query.py dates          # 系年异说
python code/query.py objects        # 碑刻与图像
python code/query.py scholarship    # 研究文献
```

Windows 若中文输出乱码，先设 `$env:PYTHONIOENCODING="utf-8"`。

## 文件

```text
week-09/
├── sources/processed/passages.json   ← 唯一资料来源（可编辑）
├── code/build_db.py                  ← JSON → SQLite
├── code/validate.py                  ← 建库前检查 JSON
├── code/query.py                     ← 查询工具
├── code/dialogue_scene.html          ← 像素对话动画
├── artifacts/confucius_laozi.db      ← 生成物（gitignored，可重建）
├── skill/                            ← 数据库技能（索引＋检索＋维护＋原则）
│   ├── SKILL.md
│   ├── what-it-does.md
│   ├── how-to-maintain.md
│   └── principles.md
└── research/notes/
    ├── source_database.md            ← 本文件
    └── scene_design.md               ← 动画的场景与台词设计
```

维护流程见 `skill/how-to-maintain.md`；回答问题的格式与例子见 `skill/what-it-does.md`。

## 数据表

| 表 | 内容 |
|---|---|
| `meta` | 标题、范围、体例、警告 |
| `sources` | 10 种文献：书名、篇卷、作者、年代、文类、网址 |
| `topics` | 9 个主题：问礼、仁义、道、龙、送言、丧礼、藏书、师承、老子形象 |
| `passages` | 16 条原文＋摘要＋说话者＋地点＋文类＋史料判断 |
| `passage_topics` | 条目与主题的多对多关系 |
| `date_claims` | 5 条系年主张，保留彼此冲突的说法 |
| `objects` | 老子铭碑、武氏祠「孔子见老子」画像石 |
| `scholarship` | 10 项研究文献，`core=1` 为三项核心 |
| `scholarship_passages` | 研究文献与材料的关联 |
| `v_passages` | 方便阅读的合并视图 |

## 收录原则

1. **只收与会面直接相关的材料**：或记会面，或记「孔子学于老聃」，或直接证明二人关系。
2. **每条都有出处**：书名、篇卷、维基文库网址；古籍无页码，以卷／篇定位。
3. **文类分开标记**：史书记载、礼书引述、诸子寓言、杂家记载、儒门追述、碑刻、图像。
4. **年代异说不合并**：放入 `date_claims`，让用户看见冲突。
5. **未读的书目标为线索**：`read_status` 区分「已读摘要」「未读全文」「仅检索到书目」。

## 三个关键判断

1. **最早的层次不是「问礼」故事。** 《礼记·曾子问》四次引「吾闻诸老聃」，老聃是丧礼、迁庙主、日食止柩等礼制的权威；孔子与他是共事者、请教者，但没有《史记》那套「适周问礼」的完整叙事（P03–P06）。
2. **「适周问礼」的完整叙事是汉代史书。** 《史记·孔子世家》说「适周问礼，盖见老子云」，「盖」「云」是存疑笔法；《老子韩非列传》则把重点放在老子对孔子的训诫与「其犹龙邪」的赞叹（P01–P02）。《庄子》把会面放到沛，且明言孔子五十一岁，属寓言系年（P08–P10）。
3. **东汉以后是接受史。** 边韶《老子铭》说孔子十七岁学礼、老子已二百余岁（P15），武氏祠把「孔子见老子」刻成画像石（O02）；老子形象被神化，会面成为固定的文化母题。Galambos 研究的西夏文写本更把这个故事带到十一至十二世纪（K02）。

## 限制与待办

- 原文取自维基文库，**未逐字校勘**中华书局点校本；引用前应核对纸本。
- 古籍没有现代页码；期刊论文才有页码。K01、K03、K06 未读全文；K07–K10 已读摘要，全文待借阅。
- 最新的检索记录、候选书目与阅读顺序见 `research/references/bibliography.md`。
- O02 的具体图版、榜题、尺寸与复原位置**待核**。
- 全部使用简体字。引文按通行简化字转写，原文的繁体字形可在维基文库链接核对。
- 下一步：为对话模拟加 `personas` 与 `scenes` 表，把 P03–P06（礼学问答）、P01–P02／P13（适周问礼）、P07–P11（仁义与道）分成三个可玩场景，并逐句标明「有文本依据」或「推演」。
