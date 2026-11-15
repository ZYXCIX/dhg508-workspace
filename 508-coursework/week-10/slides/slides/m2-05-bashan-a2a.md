---
minutes: 1.5
---

# In Bashan, the Game Agent verifies a source boundary before writing dialogue.

<div class="body">
<div class="term">
<div class="term-bar"><span>Terminal 2 · builder</span></div>
<pre>
<span class="tool">● agent_mail.send_message</span>   to: <span class="hl">researcher</span>
<span class="blk">"Can Talbot cite Kornai's 'investment hunger' on the bow deck, or is that Kornai's own paper?"</span>
&nbsp;
<span class="tool">● agent_mail.fetch_inbox</span>    from: <span class="hl">researcher</span>
<span class="blk">"Do NOT put 'investment hunger' in Talbot's mouth. Tobin pp. 152–158 argues credit &amp; statistical preconditions; Kornai speaks separately."</span>
&nbsp;
<span class="tool">← Edit</span> game/people/expert-1.json
<span class="ok">✓ Kept Talbot strictly on Tobin pp. 152–158</span>
</pre>
<div class="term-foot">Build · DeepSeek V4.1 Flash · high</div>
</div>
<div class="frame"><span class="label">Why this beats one giant session</span><div class="text">

- `builder` never pollutes its context with 200 pages of Chinese PDFs
- `researcher` guards historical accuracy full-time
- prevents **character conflation** (mixing Tobin [@tobin1986macro] with Kornai [@kornai2006force])

</div></div>
</div>

<!--
看巴山轮里的真实场景：开发 agent 在写船头对话时想给 Talbot 加词，拿不准“投资饥渴症”能不能从 Talbot 嘴里说出来。它直接调 team_chat 问研究 agent；研究 agent 一查《宏观经济的管理与改革》第 152 到 158 页，马上回信：“不行！投资饥渴是科尔奈的概念，托宾讲的是信贷控制与统计制度前提。”开发 agent 收到后立刻守住边界，既没串台，也没把几百页史料塞爆开发窗口的上下文。
-->

::read::
When the Game Agent asks the Research Agent whether James Talbot can mention "investment hunger," the Research Agent checks Tobin's 1986 text and blocks conflating Tobin's argument with János Kornai's.
