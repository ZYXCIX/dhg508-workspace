#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the Confucius–Laozi source database.

Input : sources/processed/passages.json
Output: artifacts/confucius_laozi.db  (SQLite)

Usage:
    python code/build_db.py
    python code/build_db.py path/to/passages.json path/to/out.db
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
DEFAULT_JSON = os.path.join(PROJECT, "sources", "processed", "passages.json")
DEFAULT_DB = os.path.join(PROJECT, "artifacts", "confucius_laozi.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS v_passages;
DROP TABLE IF EXISTS scholarship_passages;
DROP TABLE IF EXISTS scholarship;
DROP TABLE IF EXISTS objects;
DROP TABLE IF EXISTS date_claims;
DROP TABLE IF EXISTS passage_topics;
DROP TABLE IF EXISTS passages;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS sources;
DROP TABLE IF EXISTS meta;

CREATE TABLE meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE sources (
    id      TEXT PRIMARY KEY,
    title   TEXT NOT NULL,
    section TEXT,
    author  TEXT,
    period  TEXT,
    date    TEXT,
    genre   TEXT,
    url     TEXT,
    note    TEXT
);

CREATE TABLE topics (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE passages (
    id          TEXT PRIMARY KEY,
    source_id   TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    locator     TEXT NOT NULL,
    quote_type  TEXT NOT NULL CHECK (quote_type IN ('全文', '节录')),
    quote       TEXT NOT NULL,
    summary     TEXT NOT NULL,
    speaker     TEXT,
    place       TEXT,
    evidence    TEXT,
    historicity TEXT,
    note        TEXT
);

CREATE TABLE passage_topics (
    passage_id TEXT NOT NULL REFERENCES passages(id) ON DELETE CASCADE,
    topic_id   TEXT NOT NULL REFERENCES topics(id)   ON DELETE CASCADE,
    PRIMARY KEY (passage_id, topic_id)
);

CREATE TABLE date_claims (
    id        TEXT PRIMARY KEY,
    source_id TEXT REFERENCES sources(id) ON DELETE SET NULL,
    claim     TEXT NOT NULL,
    gregorian TEXT,
    status    TEXT,
    note      TEXT
);

CREATE TABLE objects (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT,
    date        TEXT,
    place       TEXT,
    source_id   TEXT REFERENCES sources(id) ON DELETE SET NULL,
    description TEXT,
    status      TEXT
);

CREATE TABLE scholarship (
    id          TEXT PRIMARY KEY,
    author      TEXT,
    title       TEXT NOT NULL,
    publication TEXT,
    publisher   TEXT,
    volume      TEXT,
    year        TEXT,
    pages       TEXT,
    doi         TEXT,
    argument    TEXT,
    relation    TEXT,
    read_status TEXT,
    core        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE scholarship_passages (
    scholarship_id TEXT NOT NULL REFERENCES scholarship(id) ON DELETE CASCADE,
    passage_id     TEXT NOT NULL REFERENCES passages(id)   ON DELETE CASCADE,
    relation       TEXT,
    PRIMARY KEY (scholarship_id, passage_id)
);

CREATE INDEX idx_passages_source  ON passages(source_id);
CREATE INDEX idx_passages_place   ON passages(place);
CREATE INDEX idx_passages_evid    ON passages(evidence);
CREATE INDEX idx_pt_topic         ON passage_topics(topic_id);
CREATE INDEX idx_dates_source     ON date_claims(source_id);
CREATE INDEX idx_scholar_core     ON scholarship(core);

CREATE VIEW v_passages AS
SELECT
    p.id,
    s.title || '·' || s.section AS source,
    p.locator,
    p.quote_type,
    p.quote,
    p.summary,
    p.speaker,
    p.place,
    p.evidence,
    p.historicity,
    GROUP_CONCAT(t.name, '、') AS topics
FROM passages p
JOIN sources s ON s.id = p.source_id
LEFT JOIN passage_topics pt ON pt.passage_id = p.id
LEFT JOIN topics t ON t.id = pt.topic_id
GROUP BY p.id;
"""

META_KEYS = [
    "title", "subtitle", "compiled", "compiler",
    "scope", "conventions", "caution", "source_policy",
]


def _insert_many(conn, sql, rows):
    if rows:
        conn.executemany(sql, rows)


def build(json_path: str, db_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)

    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)

        meta = doc.get("meta", {})
        conn.executemany(
            "INSERT INTO meta(key, value) VALUES (?, ?)",
            [(k, str(meta[k])) for k in META_KEYS if k in meta],
        )
        conn.execute(
            "INSERT INTO meta(key, value) VALUES (?, ?)",
            ("passage_count", str(len(doc.get("passages", [])))),
        )

        _insert_many(
            conn,
            "INSERT INTO sources(id,title,section,author,period,date,genre,url,note) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            [
                (s["id"], s["title"], s.get("section"), s.get("author"),
                 s.get("period"), s.get("date"), s.get("genre"),
                 s.get("url"), s.get("note"))
                for s in doc.get("sources", [])
            ],
        )

        _insert_many(
            conn,
            "INSERT INTO topics(id,name,description) VALUES (?,?,?)",
            [(t["id"], t["name"], t.get("description"))
             for t in doc.get("topics", [])],
        )

        _insert_many(
            conn,
            "INSERT INTO passages(id,source_id,locator,quote_type,quote,summary,"
            "speaker,place,evidence,historicity,note) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            [
                (p["id"], p["source_id"], p["locator"], p["quote_type"],
                 p["quote"], p["summary"], p.get("speaker"), p.get("place"),
                 p.get("evidence"), p.get("historicity"), p.get("note"))
                for p in doc.get("passages", [])
            ],
        )

        _insert_many(
            conn,
            "INSERT INTO passage_topics(passage_id,topic_id) VALUES (?,?)",
            [(p["id"], tid)
             for p in doc.get("passages", [])
             for tid in p.get("topics", [])],
        )

        _insert_many(
            conn,
            "INSERT INTO date_claims(id,source_id,claim,gregorian,status,note) "
            "VALUES (?,?,?,?,?,?)",
            [
                (d["id"], d.get("source_id"), d["claim"], d.get("gregorian"),
                 d.get("status"), d.get("note"))
                for d in doc.get("date_claims", [])
            ],
        )

        _insert_many(
            conn,
            "INSERT INTO objects(id,name,type,date,place,source_id,description,status) "
            "VALUES (?,?,?,?,?,?,?,?)",
            [
                (o["id"], o["name"], o.get("type"), o.get("date"),
                 o.get("place"), o.get("source_id"), o.get("description"),
                 o.get("status"))
                for o in doc.get("objects", [])
            ],
        )

        _insert_many(
            conn,
            "INSERT INTO scholarship(id,author,title,publication,publisher,volume,"
            "year,pages,doi,argument,relation,read_status,core) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [
                (k["id"], k.get("author"), k["title"], k.get("publication"),
                 k.get("publisher"), k.get("volume"), k.get("year"),
                 k.get("pages"), k.get("doi"), k.get("argument"),
                 k.get("relation"), k.get("read_status"),
                 1 if k.get("core") else 0)
                for k in doc.get("scholarship", [])
            ],
        )

        _insert_many(
            conn,
            "INSERT INTO scholarship_passages(scholarship_id,passage_id,relation) "
            "VALUES (?,?,?)",
            [(x["scholarship_id"], x["passage_id"], x.get("relation"))
             for x in doc.get("scholarship_passages", [])],
        )

        conn.commit()
    finally:
        conn.close()

    return {
        "sources": len(doc.get("sources", [])),
        "passages": len(doc.get("passages", [])),
        "topics": len(doc.get("topics", [])),
        "date_claims": len(doc.get("date_claims", [])),
        "objects": len(doc.get("objects", [])),
        "scholarship": len(doc.get("scholarship", [])),
    }


def main(argv):
    json_path = argv[1] if len(argv) > 1 else DEFAULT_JSON
    db_path = argv[2] if len(argv) > 2 else DEFAULT_DB

    if not os.path.isfile(json_path):
        sys.stderr.write("ERROR: file not found: %s\n" % json_path)
        return 1

    stats = build(json_path, db_path)
    print("Built %s" % db_path)
    for key, value in stats.items():
        print("  %-12s %d" % (key, value))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
