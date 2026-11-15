---
layout: compare
kicker: Humanities advantage
minutes: 1
steps: false
left:
  title: Naive live backend
  items:
    - Re-computes summaries, clusters, or embeddings on a server per visitor
    - Needs a paid vector database and 24/7 Python server
    - Slow, fragile, and bills you for every click
right:
  title: Pre-compute once, ship static
  items:
    - Historical & literary corpora rarely change after curation
    - Compute embeddings, UMAP coordinates, and indexes once on your laptop
    - Export static JSON / binary files to Cloudflare Pages for $0/month
verdict: Never compute at request time what already existed at build time.
---

# Pre-compute fixed humanities corpora locally so deployment stays nearly free.

<!--
讲部署时我特别想教大家一个数字人文项目的“降维打击”思路：Pre-compute（预计算）！商业社交软件每秒都有新帖子，所以不得不买昂贵的实时数据库；但我们做历史、文学、神话研究，你的两千条史料整理完之后是固定不变的！与其让每个访客点进来都现算一遍，不如在你自己电脑上提前全部算好，导出成静态文件直接免费部署出去！
-->

::read::
Because historical and literary corpora are static once curated, you can pre-compute embeddings, coordinates, and indexes locally at build time instead of paying for a 24/7 backend database.
