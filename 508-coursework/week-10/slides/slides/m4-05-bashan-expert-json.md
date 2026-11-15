---
minutes: 1
---

# Inspect the real Bashan character record that our unit test protects.

<div class="json" data-src="bashan/game/people/expert-1.json (James Talbot)"><pre>
{
  "id": "expert-1",
  "name": "James Talbot",
  "stance": {
    "positions": [{
      "id": "expert-1:Positions:Credit and institutions",
      "provenance": { "how": "own", "strength": 0.8, "when": <span class="hl">"September 1985"</span> },
      "research": {
        "evidenceLevel": <span class="hl">"据"</span>,
        "ref": <span class="hl">"《宏观经济的管理与改革》（1986），托宾，pp.152、157–158"</span>
      }
    }]
  },
  "persona": <span class="hl">"## What you do not know\n- You cannot know events that have not happened..."</span>
}
</pre></div>

::foot::
Real character record from *Bashan* [@tobin1986macro] · Rendered with Reslides JSON viewer

<!--
用我们新版 reslides 的 JSON 视图看一下巴山轮里真实的 expert-1.json（也就是以托宾为原型的 James Talbot）。注意标出来的四个关键位置：时间锚点是 September 1985，证据等级是“据”，页码指向 1986 年会议选编第 152、157–158 页，最底下 persona 必须带一段 What you do not know（不知道尚未发生的事）。下面我们就针对它写单元测试。
-->

::read::
James Talbot's real `expert-1.json` record in *Bashan* encodes a September 1985 timestamp, an epistemic level (`据`), exact page locators (`pp. 152, 157–158`), and a `## What you do not know` section.
