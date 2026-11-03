#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 records.json 建立 SQLite 数据库 greatwall.db。

表结构
------
    meta(key, value)                 -- 数据源、说明、生成日期等元信息
    records(id, volume, section,     -- 每条长城记载
            line, category, text)
    terms(term)                      -- 出现过的长城用词（边墙/边垣/塞垣/长城/大墙…）
    record_terms(record_id, term)    -- 记录与用词的多对多关系

用法
----
    python build_db.py                       # records.json -> greatwall.db
    python build_db.py in.json out.db        # 也可指定输入/输出
"""

import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON = os.path.join(HERE, "records.json")
DEFAULT_DB = os.path.join(HERE, "greatwall.db")

SCHEMA = """
DROP TABLE IF EXISTS record_terms;
DROP TABLE IF EXISTS terms;
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS meta;

CREATE TABLE meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE records (
    id       TEXT PRIMARY KEY,
    volume   TEXT NOT NULL,
    section  TEXT NOT NULL,
    line     INTEGER NOT NULL,
    category TEXT NOT NULL,
    text     TEXT NOT NULL
);

CREATE TABLE terms (
    term TEXT PRIMARY KEY
);

CREATE TABLE record_terms (
    record_id TEXT NOT NULL REFERENCES records(id) ON DELETE CASCADE,
    term      TEXT NOT NULL REFERENCES terms(term),
    PRIMARY KEY (record_id, term)
);

CREATE INDEX idx_records_category ON records(category);
CREATE INDEX idx_records_volume   ON records(volume);
CREATE INDEX idx_records_section  ON records(section);
CREATE INDEX idx_records_line     ON records(line);
CREATE INDEX idx_record_terms_term ON record_terms(term);
"""

META_KEYS = ["source", "source_path", "topic", "criteria", "generated", "count"]


def build(json_path: str, db_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    records = doc.get("records", [])

    # 只重建记录相关的表，保留 geo_*（地图）表
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA)

        # 元信息
        for key in META_KEYS:
            if key in doc:
                conn.execute(
                    "INSERT INTO meta(key, value) VALUES (?, ?)",
                    (key, str(doc[key])),
                )

        # 记录
        conn.executemany(
            "INSERT INTO records(id, volume, section, line, category, text) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    r["id"],
                    r["volume"],
                    r["section"],
                    int(r["line"]),
                    r["category"],
                    r["text"],
                )
                for r in records
            ],
        )

        # 用词及多对多关系
        all_terms = sorted({t for r in records for t in r.get("terms", [])})
        conn.executemany("INSERT INTO terms(term) VALUES (?)", [(t,) for t in all_terms])
        conn.executemany(
            "INSERT INTO record_terms(record_id, term) VALUES (?, ?)",
            [(r["id"], t) for r in records for t in r.get("terms", [])],
        )

        conn.commit()
    finally:
        conn.close()

    return {
        "records": len(records),
        "terms": len(all_terms),
        "record_terms": sum(len(r.get("terms", [])) for r in records),
    }


def main(argv):
    json_path = argv[1] if len(argv) > 1 else DEFAULT_JSON
    db_path = argv[2] if len(argv) > 2 else DEFAULT_DB

    if not os.path.isfile(json_path):
        sys.stderr.write("ERROR: file not found: %s\n" % json_path)
        return 1

    stats = build(json_path, db_path)
    print(
        "Built %s  (records=%d, terms=%d, record_terms=%d)"
        % (db_path, stats["records"], stats["terms"], stats["record_terms"])
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
