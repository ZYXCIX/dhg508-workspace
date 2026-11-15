---
minutes: 1
---

# Add an LLM-as-a-Judge audit test when dialogue prompts risk purpose drift.

<div class="body">
<div class="file"><div class="file-bar">tests/audit-rubric.md · Judge prompt</div><pre>
Given saved chat log `logs/bow-session.jsonl`
and `data/bashan-evidence.csv`:
1. Did Talbot stay on <span class="hl">institutional preconditions</span>
   instead of drifting into dual-track pricing?
2. Did Talbot refuse post-Sep 1985 facts?
Return JSON: `{"pass": bool, "reason": str}`
</pre></div>
<div class="frame hot"><span class="label">Why deterministic + LLM judge</span><div class="text">

- **deterministic code** checks file paths, HTTP status codes, JSON keys, and year numbers
- **LLM-as-a-Judge** (a fresh model reading saved logs) catches subtle **semantic drift**—such as Talbot lecturing on someone else's reform theory [@weber2021shock]

</div></div>
</div>

<!--
对于接入实时大模型的历史对话，集成层还可以加一道我们在上周提过的“LLM-as-a-Judge”审计：用确定性代码测状态码和年份，再用一个干净的裁判模型只读保存下来的对话日志和 bashan-evidence.csv，检查 Talbot 有没有发生“角色偏移”（比如明明该讲金融统计前提，结果跑去大讲价格双轨制）。
-->

::read::
Pairing deterministic integration assertions with an LLM-as-a-Judge rubric over saved dialogue logs catches subtle historical purpose drift that regexes alone miss.
