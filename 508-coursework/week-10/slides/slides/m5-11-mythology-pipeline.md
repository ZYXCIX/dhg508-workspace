---
minutes: 1.5
---

# Build the myth vector bundle once in Python, then search in 12 lines of JS.

```python {1-8|10-16}
# scripts/precompute_myths.py — Run ONCE locally ($0.02 total API cost!)
import json, numpy as np
from openai import OpenAI

client = OpenAI()  # or OpenRouter / Gemini embedding endpoint
passages = json.load(open("data/myths.json"))
resp = client.embeddings.create(model="text-embedding-3-small", dimensions=512,
                                input=[p["text"] for p in passages])
vecs = np.array([d.embedding for d in resp.data], dtype=np.float16)
vecs.tofile("public/myth-vectors.f16.bin")  # 2,000 × 512 × 2 bytes ≈ 2.0 MB!

# Browser JS (public/search.js): zero backend database!
# const scores = passages.map((p, i) => ({
#   ...p, score: dot(queryVec, slice512(mythVectors, i))
# })).sort((a, b) => b.score - a.score).slice(0, 10)
```

<!--
大家看代码有多干净：上半段 Python 脚本只在你电脑上跑一次，把 2000 条神话转成 512 维 float16 数组，写进 public/myth-vectors.f16.bin（总共才两兆字节，算一次只要两美分！）。下半段网页端连数据库都不用，直接读这个静态二进制文件做点积排序，前十条最相似的神话瞬间出来。所有做档案库、文献库、图像库的同学都可以照搬这个模式！
-->

::read::
A 10-line offline Python script packs 2,000 512-dimensional `float16` embeddings into `public/myth-vectors.f16.bin` (`~2 MB`, `$0.02` one-time cost), which static browser JavaScript searches directly via dot products.
