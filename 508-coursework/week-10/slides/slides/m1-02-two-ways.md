---
minutes: 1
---

# Ideation 1 · Ask the agent to restate scope and open questions before coding.

<div class="body">
<div class="term">
<div class="term-bar"><span>OpenCode · Plan mode (Tab)</span></div>
<pre>
<span class="you">Do NOT write code yet. Restate the 1987 home computer</span>
<span class="you">room dimensions, objects, and 3 open questions.</span>
&nbsp;
<span class="ok">Scope I understand:</span>
<span class="blk">• Compact 3.5 × 3.8 m 1987 Beijing/Shanghai room (not a garage)</span>
<span class="blk">• CEC-I / Apple IIe clone on wooden desk + 14" CRT</span>
<span class="blk ask">Q1: Does the visitor enter from a corridor or stairwell?</span>
<span class="blk ask">Q2: Should cassette tape loading play real audio?</span>
</pre>
<div class="term-foot">Plan · DeepSeek V4.1 Flash · high</div>
</div>
<div class="frame hot"><span class="label">How to set up verbal ideation</span><div class="text">

- press **`Tab`** in OpenCode to switch `Build → Plan` (forbids file edits)
- require **3 uncertainties** so the agent surfaces hidden assumptions instead of guessing silently

</div></div>
</div>

<!--
先看 Ideation 闭环的第一招：怎么设置？在 OpenCode 里按一下 `Tab` 键切到 `Plan` 模式（这个模式下它不能乱改代码），然后加上一句硬要求：“先别写代码，用几句话复述你理解的空间尺寸、核心物件，并向我提出三个不确定的问题。”如果我不这么问，直接让它建“1987年的电脑房间”，它十有八九给你建一个美国大车库配霓虹灯！让它开口反问你，十五秒钟就能把方向对齐。
-->

::read::
Switch OpenCode to **Plan** mode (`Tab`) and require the agent to restate your design boundaries and ask three clarifying questions before any code is written.
