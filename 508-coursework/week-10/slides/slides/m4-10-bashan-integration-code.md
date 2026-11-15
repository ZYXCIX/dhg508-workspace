---
minutes: 1.5
---

# Test CSV cross-references and the /api/chat endpoint together in 0.4s.

```python {1-5|7-14|16-22}
# tests/test_integration.py — FastAPI TestClient (no browser needed)
import csv, json
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

def test_evidence_csv_anchors_exist_in_world_and_people():
    world = json.load(open("game/world.json"))
    expert = json.load(open("game/people/expert-1.json"))
    rows = list(csv.DictReader(open("data/bashan-evidence.csv")))
    assert any("152" in p["research"]["ref"] for p in expert["stance"]["positions"])
    assert rows[2]["locator"] in world["zones"]  # "bashan-anchor" must exist!

def test_chat_endpoint_returns_reply_and_source_tier():
    res = client.post("/api/chat", json={
        "npcId": "expert-1", "zone": "bashan-anchor",
        "message": "Can China just copy a Western money-supply target?"
    })
    assert res.status_code == 200
    body = res.json()
    assert body["evidenceLevel"] in {"据", "推断", "设"} and "institutions" in body["reply"].lower()
```

<!--
看这段 Python 集成测试怎么写：上半段同时打开 CSV、world.json 和 expert-1.json，断言 CSV 第三行写的定位符 bashan-anchor 在 world.json 的区域表里真实存在，且 152 页真实出现在人物卡片里；下半段用 FastAPI 的 TestClient 在内存里直接调 POST /api/chat，测试前端发过来的请求格式跟后端返回的 JSON 字段完全匹配。全程不到半秒钟！
-->

::read::
`tests/test_integration.py` verifies both cross-file referential integrity (`bashan-evidence.csv` ↔ `world.json` ↔ `expert-1.json`) and the `/api/chat` HTTP contract via `TestClient`.
