---
minutes: 1.5
---

# Case study · Pre-computing embeddings for a comparative mythology database.

<div class="body">
<div class="frame"><span class="label">Comparative mythology project need</span><div class="text">

- a corpus of ~2,000 myth motifs and narrative passages across traditions
- readers search by **meaning** (*"floods sent as divine punishment"*) and explore related motifs visually
- seems to require Pinecone + FastAPI + Docker (`$25+/mo`)

</div></div>
<div class="frame hot"><span class="label">Pre-computed static architecture (`$0/mo`)</span><div class="text">

- **Offline (once)**: Python script embeds all 2,000 passages (`512 dims × float16` = **2 MB** binary file!) + 2D UMAP coordinates
- **Deployed static (`Pages`)**: Browser downloads the 2 MB vector index once and runs cosine similarity in `< 4 ms` in JS
- **Query vector**: Either a tiny free Worker calling the embedding API (`$0.00001/search`) or in-browser `Transformers.js`!

</div></div>
</div>

<!--
我们就拿世界神话数据库项目来具体算一笔账：做比较神话数据库，需要用 Embeddings 做跨文本的母题语义检索。如果按网上的重型教程，得租向量数据库 Pinecone 加云服务器，一个月几十美金。换成 Pre-compute 怎么做？本地跑一次 Python，把两千段神话算成 512 维 float16 向量，存出来总共只有 2MB！直接当静态文件发到 Cloudflare Pages，浏览器用 JS 算余弦相似度只要 4 毫秒，托管费 0 元！
-->

::read::
For a comparative mythology database, pre-computing 2,000 passage embeddings into a `2 MB` static binary file eliminates vector database servers entirely: cosine similarity runs in browser JavaScript in under `4 ms`.
