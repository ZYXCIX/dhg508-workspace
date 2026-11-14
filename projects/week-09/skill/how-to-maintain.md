# 如何维护这个数据库

## 一、先记住三个文件

| 文件 | 作用 | 能不能手改 |
|---|---|---|
| `sources/processed/passages.json` | 唯一数据源 | **能**，改这里 |
| `code/build_db.py` | 建库脚本＋表结构 | 能，改结构时改 |
| `artifacts/confucius_laozi.db` | 生成的 SQLite | **不要手改**，会被重建覆盖 |

改完 JSON 后，永远按这个顺序：

```bash
cd projects/week-09
python code/validate.py     # 先检查
python code/build_db.py     # 再重建
python code/query.py stats  # 最后抽查
```

## 二、编号规则

| 前缀 | 用途 | 下一个可用 |
|---|---|---|
| `S` | 文献 | 先看 `python code/query.py sources` |
| `P` | 文本条目 | 先看 `python code/query.py list` |
| `T` | 主题 | 先看 `python code/query.py topics` |
| `D` | 系年主张 | 先看 `python code/query.py dates` |
| `O` | 碑刻／图像 | 先看 `python code/query.py objects` |
| `K` | 研究文献 | 先看 `python code/query.py scholarship` |

不要跳号，不要复用旧号。编号一旦写进文档或幻灯片，就不要再改。

## 三、加一种新文献

在 `passages.json` 的 `sources` 数组里加一项：

```json
{
  "id": "S11",
  "title": "说苑",
  "section": "卷十·敬慎",
  "author": "刘向",
  "period": "西汉",
  "date": "约公元前1世纪",
  "genre": "杂事",
  "url": "https://zh.wikisource.org/wiki/说苑/卷10",
  "note": "清代以前多视为刘向所编；材料来源复杂。"
}
```

- `title` 和 `section` 分开写，查询时显示为「书名·篇卷」。
- `date` 用「约公元前1世纪」这种可读写法；精确年份放 `date_claims`。
- `url` 放可核对的原文本链接；不要放搜索结果页。
- `note` 写文本性质、真伪、版本问题，不写你的评价。

## 四、加一条文本材料

在 `passages` 数组里加一项：

```json
{
  "id": "P17",
  "source_id": "S11",
  "locator": "卷十·敬慎",
  "quote_type": "节录",
  "quote": "……（原文）……",
  "summary": "……（白话摘要）……",
  "speaker": "孔子；老子",
  "place": "周",
  "evidence": "杂事记载",
  "historicity": "西汉编成，材料或早于汉代",
  "note": "这段和《史记》的送言同源，但文字更繁。",
  "topics": ["T05"]
}
```

字段说明：

| 字段 | 怎么写 |
|---|---|
| `quote_type` | 只写 `全文` 或 `节录`；有删节必须写 `节录`，并用「……」标出 |
| `quote` | 原文；简体转写可以，但不要改字、补字、删字 |
| `summary` | 你自己的白话复述，不加库外史实 |
| `speaker` | 直接说话的人；引述他人时写「孔子（引老聃）」 |
| `place` | 周、沛、巷党等；没有就写 `—` |
| `evidence` | 史书记载／礼书引述／诸子寓言／杂家记载／儒门追述／碑刻／图像 |
| `historicity` | 一句话判断：较早材料、寓言、后世追述、待考等 |
| `topics` | 必须是 `topics` 表里已有的 `T` 编号；没有就新加主题 |

**不要把创作台词写进 `passages`。** 动画里的「拟构」对白属于 `research/notes/scene_design.md` 和 HTML，不属于史料库。

## 五、加一个主题

在 `topics` 数组里加：

```json
{ "id": "T10", "name": "朋友", "description": "孔子与老子之间的私人情谊。" }
```

然后把相关条目的 `topics` 里加上 `"T10"`。主题名要短，描述只写一句。

## 六、加一条系年主张

在 `date_claims` 数组里加：

```json
{
  "id": "D06",
  "source_id": "S11",
  "claim": "某书说孔子见老子在某某年。",
  "gregorian": "前500",
  "status": "后世追述",
  "note": "与 D02 冲突，保留异说。"
}
```

规则：**不要合并冲突**。每一条主张单独一行，`status` 写清楚它是原记、推算、寓言系年还是考古断代。

## 七、加一件碑刻或图像

在 `objects` 数组里加：

```json
{
  "id": "O03",
  "name": "某地「孔子见老子」画像石",
  "type": "画像石",
  "date": "东汉",
  "place": "山东某地",
  "source_id": "S10",
  "description": "画面内容、榜题、尺寸。",
  "status": "实物存在；图版待核"
}
```

没亲眼核对图录的，`status` 一律写「待核」，不要写「已确认」。

## 八、加一项研究文献

在 `scholarship` 数组里加：

```json
{
  "id": "K07",
  "author": "作者",
  "title": "篇名",
  "publication": "期刊或书名",
  "publisher": "出版社（书籍才填）",
  "volume": "卷期（有就填）",
  "year": "2020",
  "pages": "12–34",
  "doi": "10.xxxx/xxxx",
  "argument": "作者的核心论点，一句话。",
  "relation": "和本库哪条材料有关。",
  "read_status": "未读全文；仅见摘要",
  "core": false
}
```

- 只看到摘要，就写「仅见摘要」；只看到书目，就写「仅检索到书目」。
- 不要为了凑数把没读过的书写成「已读」。
- 核心三项用 `"core": true`，其余用 `false`。

如果要把研究和某条材料关联，在 `scholarship_passages` 里加：

```json
{ "scholarship_id": "K07", "passage_id": "P17", "relation": "讨论该段的成书年代" }
```

## 九、检查、重建、抽查

```bash
python code/validate.py
python code/build_db.py
python code/query.py show P17
python code/query.py search 新关键词
```

`validate.py` 会检查：必填字段、重复 ID、`source_id` 是否存在、`topics` 是否存在、`quote_type` 是否合法、研究链接是否指向存在的条目。

## 十、改表结构

只有确实需要时才改：

1. 修改 `code/build_db.py` 里的 `SCHEMA`。
2. 修改对应的 `INSERT` 语句。
3. 在 `passages.json` 里给所有相关条目补字段。
4. 重新运行 `build_db.py`（它会先 DROP 再 CREATE）。
5. 更新 `what-it-does.md` 的表结构说明。

不要用 SQLite 客户端手改数据库；下次重建就没了。

## 十一、文档同步

每次增加材料后，顺手更新：

- `README.md` 的统计数字（文献、条目、系年、实物、研究）。
- `research/notes/source_database.md` 的「这是什么」表和「三个关键判断」（如果判断变了）。
- 如果新增了核心研究，更新 `SKILL.md` 的编号速查。

## 十二、Git 规则

- **要提交**：`passages.json`、`build_db.py`、`validate.py`、`query.py`、`SKILL.md`、三个说明文件、研究笔记。
- **不要提交**：`artifacts/*.db`（`.gitignore` 已忽略）、临时截图、`__pycache__`。
- 每次提交信息写清楚：加了哪条材料、为什么加、来源是什么。

## 十三、常见错误

| 错误 | 原因 | 处理 |
|---|---|---|
| `unknown source_id S99` | 先引用了不存在的文献 | 先在 `sources` 里加 `S99` |
| `duplicate id P04` | 编号重复 | 换下一个未用编号 |
| `quote_type must be 全文/节录` | 写成了「节选」「摘录」 | 改成 `节录` |
| `unknown topic T99` | 主题没建 | 先在 `topics` 里加 |
| 查询搜不到 | 简体／繁体不一致 | 统一用简体；原文的繁体字形可在维基文库链接核对 |
| `FOREIGN KEY constraint failed` | 条目引用了不存在的父项 | 先加父项，再重建 |
