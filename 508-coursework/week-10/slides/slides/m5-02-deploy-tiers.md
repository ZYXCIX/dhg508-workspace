---
minutes: 1
---

# Start from pure static hosting and add server layers only when forced.

<div class="route">
<div class="step"><span class="yr">Tier 1 · Free</span><p class="what">Static site</p><p class="how">HTML, JS, JSON, Unity WebGL</p></div>
<div class="arrow">→</div>
<div class="step red"><span class="yr">Tier 2 · $0–$5</span><p class="what">Static + Worker</p><p class="how">secret API keys &amp; rate limits</p></div>
<div class="arrow">→</div>
<div class="step"><span class="yr">Tier 3 · $5/mo</span><p class="what">Virtual Machine</p><p class="how">24/7 Python, DB writes, sockets</p></div>
</div>

<p class="sub">Ninety percent of humanities and game prototypes belong in Tier 1 or Tier 2.</p>

<!--
大家选部署方案记住一个原则：能轻绝不重。第一档是纯静态网站（Static），零成本、零维护；如果必须调大模型或第三方付费 API、要藏密钥，就升到第二档：静态页面加一个超轻量的 Serverless Worker；只有当你非跑长驻 Python 大进程、实时写数据库或多人联机房间不可时，才需要第三档：租一台虚拟机（VPS）。我们班 90% 的项目用第一档或第二档就够了。
-->

::read::
Choose the lightest deployment tier that fits: pure static hosting first, a serverless worker second when secret API keys are required, and a virtual machine only for stateful heavy backends.
