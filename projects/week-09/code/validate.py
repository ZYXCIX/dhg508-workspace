#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate sources/processed/passages.json before rebuilding the database."""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
DEFAULT_JSON = os.path.join(PROJECT, "sources", "processed", "passages.json")

REQUIRED_TOP = ["meta", "sources", "topics", "passages"]
REQUIRED_SOURCE = ["id", "title"]
REQUIRED_PASSAGE = ["id", "source_id", "locator", "quote_type", "quote", "summary"]
REQUIRED_TOPIC = ["id", "name"]


def validate(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)

    errors: list[str] = []
    for key in REQUIRED_TOP:
        if key not in doc:
            errors.append("missing top-level key: %s" % key)
    if errors:
        return errors

    def unique(rows, label):
        seen = set()
        for row in rows:
            rid = row.get("id")
            if not rid:
                errors.append("%s: row without id" % label)
            elif rid in seen:
                errors.append("%s: duplicate id %s" % (label, rid))
            seen.add(rid)
        return seen

    source_ids = unique(doc.get("sources", []), "sources")
    topic_ids = unique(doc.get("topics", []), "topics")
    passage_ids = unique(doc.get("passages", []), "passages")
    scholarship_ids = unique(doc.get("scholarship", []), "scholarship")

    for s in doc.get("sources", []):
        for key in REQUIRED_SOURCE:
            if not s.get(key):
                errors.append("source %s: missing %s" % (s.get("id"), key))

    for t in doc.get("topics", []):
        for key in REQUIRED_TOPIC:
            if not t.get(key):
                errors.append("topic %s: missing %s" % (t.get("id"), key))

    for p in doc.get("passages", []):
        pid = p.get("id")
        for key in REQUIRED_PASSAGE:
            if not p.get(key):
                errors.append("passage %s: missing %s" % (pid, key))
        if p.get("source_id") not in source_ids:
            errors.append("passage %s: unknown source_id %s" % (pid, p.get("source_id")))
        if p.get("quote_type") not in ("全文", "节录", "節錄"):
            errors.append("passage %s: quote_type must be 全文/节录, got %r" % (pid, p.get("quote_type")))
        for tid in p.get("topics", []):
            if tid not in topic_ids:
                errors.append("passage %s: unknown topic %s" % (pid, tid))
        if "topics" not in p:
            errors.append("passage %s: missing topics list" % pid)

    for d in doc.get("date_claims", []):
        sid = d.get("source_id")
        if sid and sid not in source_ids:
            errors.append("date_claim %s: unknown source_id %s" % (d.get("id"), sid))

    for o in doc.get("objects", []):
        sid = o.get("source_id")
        if sid and sid not in source_ids:
            errors.append("object %s: unknown source_id %s" % (o.get("id"), sid))

    for x in doc.get("scholarship_passages", []):
        if x.get("scholarship_id") not in scholarship_ids:
            errors.append("scholarship_passages: unknown scholarship_id %s" % x.get("scholarship_id"))
        if x.get("passage_id") not in passage_ids:
            errors.append("scholarship_passages: unknown passage_id %s" % x.get("passage_id"))

    return errors


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_JSON
    if not os.path.isfile(path):
        sys.stderr.write("ERROR: file not found: %s\n" % path)
        return 1
    errors = validate(path)
    if errors:
        print("FAIL: %d problem(s)" % len(errors))
        for e in errors:
            print("  - " + e)
        return 1
    print("OK: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
