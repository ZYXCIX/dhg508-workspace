---
name: confucius-laozi-db
description: 检索「孔子见老子」史料数据库（projects/week-09）。当用户询问孔子与老子会面的记载、年代异说、文本出处、老子形象、相关研究书目，或要求从数据库取证、核对引文、扩展材料时使用。
---

# 孔子见老子 · 史料数据库

## 这是什么

一个关于「孔子见老子／孔子问礼于老子」的材料库，不是「孔子真的见过老子」的证明。库内收 10 种文献、16 条文本、5 条系年异说、2 件碑刻／图像、10 项研究文献。

- 数据源：`projects/week-09/sources/processed/passages.json`
- 数据库：`projects/week-09/artifacts/confucius_laozi.db`（gitignored，可重建）
- 查询工具：`projects/week-09/code/query.py`
- 建库脚本：`projects/week-09/code/build_db.py`

## 先看哪里

| 作业／任务 | 读这些文件 |
|---|---|
| **Week 9 展示**：把设计放进学术讨论，解释史料与选择 | [`what-it-does.md`](what-it-does.md) ＋ [`principles.md`](principles.md) ＋ [`../research/notes/source_database.md`](../research/notes/source_database.md) |
| **做对话动画**：场景、年龄、服饰、台词来源 | [`../code/dialogue_scene.html`](../code/dialogue_scene.html) ＋ [`../research/notes/scene_design.md`](../research/notes/scene_design.md) |
| **回答具体问题**：某句原文、某条系年、某件碑刻／图像 | [`what-it-does.md`](what-it-does.md) |
| **新增材料／补书目／改表结构／重建数据库** | [`how-to-maintain.md`](how-to-maintain.md) |
| **判断材料能不能用、怎么标注、哪些话不能说** | [`principles.md`](principles.md) |

## 快速开始

在 `projects/week-09/` 下：

```bash
# 数据库不存在时先重建
python code/validate.py
python code/build_db.py

# 总览
python code/query.py stats

# 全文检索
python code/query.py search 仁义

# 按主题、文献筛选
python code/query.py list --topic 问礼
python code/query.py list --source S03

# 看一条全文、出处与史料判断
python code/query.py show P04

# 系年异说、碑刻图像、研究文献
python code/query.py dates
python code/query.py objects
python code/query.py scholarship
```

Windows 若中文输出乱码，先设 `$env:PYTHONIOENCODING="utf-8"`。

## 编号速查

| 前缀 | 含义 | 例子 |
|---|---|---|
| `S` | 文献 | `S03` = 《礼记·曾子问》 |
| `P` | 文本条目 | `P01` = 《史记·老子韩非列传》孔子适周问礼 |
| `T` | 主题 | `T01` = 问礼 |
| `D` | 系年主张 | `D01` = 边韶《老子铭》的「孔子十七岁」说 |
| `O` | 碑刻／图像 | `O02` = 武氏祠「孔子见老子」画像石 |
| `K` | 研究文献 | `K02` = Galambos 2016 |

## 一句话原则

**只用库内材料回答；每条结论带出处；冲突的记载保留冲突；「库中没有」不等于「历史上没有」。**

详细规则见 [`principles.md`](principles.md)。
