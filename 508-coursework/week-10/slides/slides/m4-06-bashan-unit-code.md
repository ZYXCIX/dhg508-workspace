---
minutes: 1.5
---

# Write pure unit tests for Bashan's cutoff rule and character schema.

```python {1-6|8-14|16-21}
# tests/test_unit.py — Run with: pytest tests/test_unit.py -q
import json, pathlib
from src.dialogue_rules import violates_1985_cutoff, select_topic_cards

def test_1985_cutoff_blocks_future_events():
    assert violates_1985_cutoff("What did Deng say on his 1992 Southern Tour?") is True
    assert violates_1985_cutoff("How should China control credit in winter 1985?") is False

def test_expert_card_has_epistemic_levels_and_unknowns():
    card = json.loads(pathlib.Path("game/people/expert-1.json").read_text())
    assert "## What you do not know" in card["persona"]
    for pos in card["stance"]["positions"]:
        assert pos["research"]["evidenceLevel"] in {"据", "推断", "设"}
        assert len(pos["research"]["ref"]) > 0

def test_credit_query_selects_tobin_institutions_position():
    card = json.loads(pathlib.Path("game/people/expert-1.json").read_text())
    hits = select_topic_cards(card, query="interest rates and credit volume")
    assert hits[0]["id"] == "expert-1:Positions:Credit and institutions"
```

<!--
一步步看这三个单元测试：第一个测纯函数 violates_1985_cutoff，问“1992年南巡”必须返回 True 拦截，问“1985年冬天信贷控制”返回 False 放行；第二个测 expert-1.json 必须含 What you do not know，且每条立场都有“据/推断/设”和出处；第三个测检索纯函数 select_topic_cards，搜利率和信贷时，必须命中托宾关于金融制度前提的那张卡。
-->

::read::
Three unit tests in `tests/test_unit.py` verify the 1985 anachronism filter, the presence of epistemic tiers and `## What you do not know` in `expert-1.json`, and deterministic topic-card matching.
