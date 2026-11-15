---
minutes: 1
---

# Chat messages coordinate work; repository files remain the source of truth.

<Box kind="warning" title="Team rule for multi-agent projects">Never leave an agreed historical boundary only inside chat history. Every verified answer must also land in <code>data/bashan-evidence.csv</code> or <code>design-document.md</code>.</Box>

<div class="tree"><span class="label">bashan/</span><pre>
├─ .agent-mail/               <span class="dim">ephemeral inbox threads &amp; file leases (coordination)</span>
├─ design-document.md         <span class="hl">permanent scene &amp; boundary spec (committed)</span>
├─ data/bashan-evidence.csv   <span class="hl">permanent claim · page · 据/推断/设 table (committed)</span>
└─ game/people/expert-1.json  <span class="hl">character card checked against CSV (committed)</span>
</pre></div>

<!--
但多 agent 聊天有一条铁律，我用 reslides 的 Warning Box 标出来了：聊天记录只是临时协调，绝不能代替仓库里的正式文档！研究 agent 在聊天里确认完一条边界，必须同步写进 bashan-evidence.csv 或 design-document.md 并 git commit，否则明天开新窗口就全忘了。
-->

::read::
Inter-agent chat is only for transient coordination; every evidentiary decision must still be committed to `design-document.md` and `data/bashan-evidence.csv` so tests and future sessions can enforce it.
