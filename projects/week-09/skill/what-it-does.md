# 这个数据库能回答什么

## 一、能回答的问题

- 某句话出自哪本书、哪一卷／哪一篇？
- 关于「孔子见老子」，哪些文献说过？它们各自是什么时代、什么文类？
- 孔子见老子有哪几种系年？彼此冲突在哪里？
- 「老聃」在《礼记·曾子问》里是什么角色？和《史记》的「适周问礼」有什么不同？
- 老子被写成年寿多少？哪些说法是神化？
- 武氏祠的「孔子见老子」画像石是什么时代的材料？
- 哪些研究讨论过这个题目？作者是谁、在哪本书／哪一期、第几页？

## 二、表结构

| 表 | 字段 | 用途 |
|---|---|---|
| `sources` | `id,title,section,author,period,date,genre,url,note` | 文献本身 |
| `passages` | `id,source_id,locator,quote_type,quote,summary,speaker,place,evidence,historicity,note` | 一条文本材料 |
| `topics` | `id,name,description` | 主题词 |
| `passage_topics` | `passage_id,topic_id` | 条目与主题的多对多 |
| `date_claims` | `id,source_id,claim,gregorian,status,note` | 系年主张（保留冲突） |
| `objects` | `id,name,type,date,place,source_id,description,status` | 碑刻、画像石等实物 |
| `scholarship` | `id,author,title,publication,publisher,volume,year,pages,doi,argument,relation,read_status,core` | 研究文献 |
| `scholarship_passages` | `scholarship_id,passage_id,relation` | 研究与材料的关联 |
| `v_passages` | 合并视图 | 方便阅读：条目＋文献＋主题 |

`quote_type` 只有两种：`全文`、`节录`。`core=1` 表示三项核心研究，`core=0` 是待读线索。

## 三、常用查询

### 命令行

```bash
python code/query.py stats
python code/query.py sources
python code/query.py topics
python code/query.py list
python code/query.py list --topic 问礼
python code/query.py list --source S03
python code/query.py search 老聃
python code/query.py show P04
python code/query.py dates
python code/query.py objects
python code/query.py scholarship
```

### SQL 直查

```sql
-- 所有提到「老聃」的条目
SELECT id, source_id, locator, quote
FROM passages
WHERE quote LIKE '%老聃%';

-- 某条材料的完整出处
SELECT s.title, s.section, s.author, s.date, p.locator, p.quote
FROM passages p JOIN sources s ON s.id = p.source_id
WHERE p.id = 'P04';

-- 某主题下的所有条目
SELECT p.id, s.title, s.section, p.locator, p.summary
FROM passages p
JOIN sources s ON s.id = p.source_id
JOIN passage_topics pt ON pt.passage_id = p.id
JOIN topics t ON t.id = pt.topic_id
WHERE t.name = '问礼'
ORDER BY p.id;

-- 系年异说
SELECT id, source_id, claim, gregorian, status
FROM date_claims ORDER BY id;

-- 三项核心研究
SELECT id, author, title, year, pages, doi, read_status
FROM scholarship WHERE core = 1 ORDER BY id;
```

## 四、回答格式

回答历史问题，按这个顺序：

1. **先给结论**：一句话说清楚，不要先铺陈。
2. **再给证据**：引原文或摘要，附「书名·篇卷」和数据库编号（如 `P04`）。
3. **标性质**：这是史书记载、礼书引述、诸子寓言、碑刻、图像，还是教学拟构？
4. **列异说**：如果库内有冲突的系年或说法，并列，不要合并。
5. **说限制**：库中没有的，就说「库中没有」；没读全文的，就说「仅见摘要／书目」。

### 示例一：最早的记载

**问**：孔子见老子最早的记载是什么？

**答**：要分两层。最早提到「老聃」的是《礼记·曾子问》的四次「吾闻诸老聃」（`P03`–`P06`），但那里老聃是丧礼、迁庙主、日食止柩的礼制权威，没有「适周问礼」的完整故事。最早的「孔子适周，将问礼于老子」完整叙事，是《史记·老子韩非列传》（`P01`）和《孔子世家》（`P02`），成书约公元前 94 年，晚于孔子约四百年。

### 示例二：老子活了多少岁

**问**：老子活了多少岁？

**答**：库内没有可靠的年龄记载。东汉边韶《老子铭》说孔子十七岁学礼时，老子已二百余岁（`P15`、`D01`）；这是东汉老子崇拜的神化，不能当信史。数据库不采用「二百余岁」作为事实。

### 示例三：孔子见老子在哪一年

**问**：孔子见老子是哪一年？

**答**：库内至少有三种互相冲突的系年，不能合并：

- `D01`：前 535 年，孔子十七岁（边韶《老子铭》，东汉碑刻）。
- `D02`：前 522 年以前，孔子未满三十（由《史记·孔子世家》叙事顺序推得）。
- `D03`：前 501 年，孔子五十一岁，地点在沛（《庄子·天运》，寓言系年）。

《史记》本身没有明记年份，所以数据库只给「异说」，不给唯一答案。

## 五、不能做什么

- 不能给先秦古籍的现代页码；库内只有卷／篇定位，期刊论文才有页码。
- 不能把 16 条材料当成「所有」记载；这是一个精选材料库。
- 不能把《庄子》寓言直接当史实；`evidence` 和 `historicity` 字段会标。
- 不能替用户判断「哪个版本是真的」；只能说明每层记载在做什么。
- 不能把 HTML 动画里的创作台词当史料；那些台词标为「拟构」，不进 `passages`。
- 不能引用未读的全文；`scholarship.read_status` 会写明「未读全文」「仅检索到书目」。
