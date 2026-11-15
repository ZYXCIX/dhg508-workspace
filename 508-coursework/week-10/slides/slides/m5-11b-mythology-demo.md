---
minutes: 1.5
preload: false
fit: false
---

# Interactive demo: pre-computed mythology embeddings at `$0/month`.

<LazyDemo
  src="./demos/mythology-embeddings-demo.html"
  badge="STATIC CLIENT-SIDE VECTOR SEARCH · ZERO RUNTIME API CALLS"
  title="Pre-Compute Embeddings Once ($0.04) → Search Instantly in Browser ($0/mo)"
  summary="Click Load to query cross-cultural motifs (Great Flood, Stealing Fire, Descent to the Underworld, Cosmic Egg) over a static float16 vector index right inside browser memory in under 1 millisecond."
  height={555}
/>

<!--
为了让大家直观看到什么叫“预计算（Pre-compute）省大钱”，点开这个比较神话数据库交互演示：左边是我们在本地打包时花 4 美分算好、压成 2MB 静态文件的向量空间，右边是浏览器直接用 JS 做点积余弦相似度检索——点“大洪水”、“盗火”、“下冥界”、“盘古宇宙卵”，不到 1 毫秒就把中国《山海经》《淮南子》和希腊、两河流域的神话配对出来了，线上服务器成本和 API 成本统统是 0！
-->

::read::
Explore how pre-computing static `float16` embeddings at build time enables sub-millisecond cross-cultural motif search across Chinese, Greek, Mesopotamian, and Norse mythology directly in the browser at `$0/month` runtime cost.
