---
minutes: 1
---

# Real 2026 web and AI costs are pennies when you pre-compute static assets.

<DataTable from="data/deployment-costs.csv" labels="Layer | Service | Scale | Real Cost | Best Use" mark="2" caption="2026 student deployment & API cost benchmark" />

<!--
很多同学不敢 deploy 是怕云服务很贵。我把 2026 年真实的网页端和 API 价格列在这张表里给大家吃颗定心丸：静态网页和每天十万次以内的 Cloudflare Worker 全是 0 美金；像神话数据库那样预计算两千段神话的 embedding，总共一次性只要 0.02 美金（一毛五港币）！就算像巴山轮那样真让玩家在线跟 NPC 聊一千轮，用 DeepSeek 或 Gemini Flash 也才两到四角美金。真需要租 VPS 虚拟机，一个月也就四五美金。
-->

::read::
With static hosting (`$0/mo`), free-tier Workers (`$0/mo`), one-time embedding pre-computation (`$0.02`), and fast models like DeepSeek or Gemini Flash (`~$0.20–$0.45` per 1,000 turns), shipping a live AI humanities project costs pennies.
