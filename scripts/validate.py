#!/usr/bin/env python3
"""校验 data/data.json：字段、分类、评分平均分、重复 id。

用法：python3 scripts/validate.py [data/data.json]
退出码 0 表示通过。
"""
import json
import sys
from collections import Counter
from pathlib import Path

CATEGORIES = {"api", "app", "cloud", "dev", "compute"}
SCORE_KEYS = {"quota", "trust", "ease", "utility", "audience", "scarcity", "safety"}
REQUIRED = [
    "id", "title", "desc", "quota", "category", "is_new", "expiring",
    "source", "source_url", "verified", "expires", "claim_url",
    "cost", "risk", "scores", "avg",
    "region", "valid_from", "claim_steps", "value", "type",
]


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/data.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data["items"]

    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids)), "存在重复 id"

    for it in items:
        for key in REQUIRED:
            assert key in it, f"缺字段 {key}: {it.get('id')}"
        assert it["category"] in CATEGORIES, f"分类非法 {it['id']}: {it['category']}"
        assert set(it["scores"]) == SCORE_KEYS, f"评分项不全 {it['id']}"
        assert all(isinstance(v, int) and 0 <= v <= 10 for v in it["scores"].values()), \
            f"评分超出 0-10: {it['id']}"
        expect = round(sum(it["scores"].values()) / 7, 1)
        assert abs(it["avg"] - expect) < 1e-9, \
            f"avg 不符 {it['id']}: {it['avg']} vs {expect}"

    cats = Counter(it["category"] for it in items)
    best = max(items, key=lambda i: i["avg"])
    print(f"通过：{len(items)} 条；分类 {dict(cats)}；"
          f"新上 {sum(1 for i in items if i['is_new'])} 条；"
          f"即将过期 {sum(1 for i in items if i['expiring'])} 条")
    print(f"最高分：{best['title']}（{best['avg']}）")
    print(f"核实日期：{data['meta'].get('verified_date')}；生成时间：{data['meta'].get('generated')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
