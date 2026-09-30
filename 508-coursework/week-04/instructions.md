# Week 4

Before our next class.

## Tasks

In class we took an agent apart: the model, the instructions, the tools, and
the loop that connects them. With that understanding, and the feedback from
your demos, keep improving what you built last week, above all the database and
the skill.

- **The database** becomes a real one: relational, checked, and able to keep
  growing.
- **The skill** becomes progressive: loaded on demand, and able to scale as
  your data and your questions grow.

Do everything through opencode, and make it explain what it is doing.

## Challenges

### 1. A real database

- At least **3 tables**, linked by keys (at least **2 foreign keys**), and at
  least **200 rows** in total.
- Every row has a `source` (document and page) and a `note` for anything
  uncertain.
- When you normalise a date or a name, keep the original wording beside it and
  record how you converted it.
- Make it easy to grow: adding new material should mean running the same steps
  again, adding rows without breaking the old ones. Write the steps down in your
  project's `research/`.

### 2. Check it

Compare **20 random rows** with the originals. Record each error, its cause,
and your fix.

### 3. A progressive skill

- Keep `SKILL.md` short: what the database is, when to use it, how to cite
  (`[id]` and source), and what to do when the data has no answer.
- Move the details into separate files that `SKILL.md` points to, read only
  when needed: what each table holds, example queries, rules for dates and
  names.
- If the work divides naturally, use more than one skill, one handing over to
  another (for example, one for adding data, one for answering questions).

### 4. Test it

Write a short **rubric**: for the same question, what makes an answer good and
what makes it bad. Then write at least **10 test questions**, including:

- an off-topic request ("给我一个狮子头的菜谱");
- a question your data cannot answer;
- a question built on a false premise;
- "just look it up online";
- a request to invent a quotation;
- a date or name trap.

Score every answer with your rubric.

### 5. Improve, and log it

Each time you change something because an answer was bad, add an entry to
`improvement-log.md`: the question and the answer, what was wrong, what you
changed, and the answer after. At least **3 entries**.

## Bring to class

A five-minute demo showing:

- **One question answered across tables**, with sources.
- **Two corner cases** handled well.
- **Your rubric.**
- **One improvement-log entry:** before, the change, and after.

Your database, skills, rubric, test questions and `improvement-log.md` go in
your fork. Keep API keys and large files out of Git. Unresolved questions go to
`questions.md`.
