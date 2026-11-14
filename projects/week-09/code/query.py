#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Query the Confucius–Laozi source database.

Examples:
    python code/query.py stats
    python code/query.py sources
    python code/query.py topics
    python code/query.py list
    python code/query.py list --topic 问礼
    python code/query.py list --source S03
    python code/query.py search 仁义
    python code/query.py show P04
    python code/query.py dates
    python code/query.py scholarship
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
DEFAULT_DB = os.path.join(PROJECT, "artifacts", "confucius_laozi.db")


def connect(path: str) -> sqlite3.Connection:
    if not os.path.isfile(path):
        sys.exit(
            "数据库不存在：%s\n先运行：python code/build_db.py" % path
        )
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def wrap(text: str, width: int = 78, indent: str = "  ") -> str:
    if not text:
        return ""
    return "\n".join(
        textwrap.fill(par, width=width, initial_indent=indent,
                      subsequent_indent=indent)
        for par in str(text).splitlines()
    )


def cmd_stats(conn, args):
    rows = {
        "sources": conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0],
        "passages": conn.execute("SELECT COUNT(*) FROM passages").fetchone()[0],
        "topics": conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0],
        "date_claims": conn.execute("SELECT COUNT(*) FROM date_claims").fetchone()[0],
        "objects": conn.execute("SELECT COUNT(*) FROM objects").fetchone()[0],
        "scholarship": conn.execute("SELECT COUNT(*) FROM scholarship").fetchone()[0],
    }
    meta = {r["key"]: r["value"] for r in conn.execute("SELECT key,value FROM meta")}
    print(meta.get("title", "孔子见老子：史料数据库"))
    if meta.get("subtitle"):
        print(meta["subtitle"])
    print()
    for key, value in rows.items():
        print("  %-12s %d" % (key, value))
    print()
    print("按文献：")
    for r in conn.execute(
        "SELECT s.id, s.title, s.section, COUNT(p.id) AS n "
        "FROM sources s LEFT JOIN passages p ON p.source_id = s.id "
        "GROUP BY s.id ORDER BY s.id"
    ):
        print("  %-4s %-4d %s·%s" % (r["id"], r["n"], r["title"], r["section"]))


def cmd_sources(conn, args):
    for r in conn.execute("SELECT * FROM sources ORDER BY id"):
        print("%s  %s·%s" % (r["id"], r["title"], r["section"]))
        print("    %s / %s / %s" % (r["author"], r["period"], r["date"]))
        if r["note"]:
            print(wrap(r["note"], indent="    "))
        print("    %s" % r["url"])
        print()


def cmd_topics(conn, args):
    for r in conn.execute(
        "SELECT t.id, t.name, t.description, COUNT(pt.passage_id) AS n "
        "FROM topics t LEFT JOIN passage_topics pt ON pt.topic_id = t.id "
        "GROUP BY t.id ORDER BY t.id"
    ):
        print("%s  %s（%d 条）" % (r["id"], r["name"], r["n"]))
        if r["description"]:
            print(wrap(r["description"], indent="    "))


def cmd_list(conn, args):
    sql = (
        "SELECT p.id, p.locator, p.quote_type, p.place, p.evidence, "
        "s.title || '·' || s.section AS source, "
        "(SELECT GROUP_CONCAT(t2.name, '、') FROM passage_topics pt2 "
        " JOIN topics t2 ON t2.id = pt2.topic_id "
        " WHERE pt2.passage_id = p.id) AS topics "
        "FROM passages p "
        "JOIN sources s ON s.id = p.source_id "
        "LEFT JOIN passage_topics pt ON pt.passage_id = p.id "
        "LEFT JOIN topics t ON t.id = pt.topic_id "
    )
    where, params = [], []
    if args.topic:
        where.append("t.name LIKE ?")
        params.append("%" + args.topic + "%")
    if args.source:
        where.append("p.source_id = ?")
        params.append(args.source)
    if args.evidence:
        where.append("p.evidence LIKE ?")
        params.append("%" + args.evidence + "%")
    if where:
        sql += "WHERE " + " AND ".join(where) + " "
    sql += "GROUP BY p.id ORDER BY p.id"

    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("没有匹配的条目。")
        return
    for r in rows:
        print("%-4s %-28s %-6s %s" % (
            r["id"], r["source"], r["quote_type"], r["topics"] or ""))
        print("     %s｜%s｜地点：%s" % (
            r["locator"], r["evidence"] or "", r["place"] or "—"))
    print("\n共 %d 条。用 `show <ID>` 看全文。" % len(rows))


def cmd_search(conn, args):
    kw = "%" + args.keyword + "%"
    sql = (
        "SELECT p.id, p.locator, p.summary, s.title || '·' || s.section AS source "
        "FROM passages p JOIN sources s ON s.id = p.source_id "
        "WHERE p.quote LIKE ? OR p.summary LIKE ? OR p.note LIKE ? "
        "ORDER BY p.id"
    )
    rows = conn.execute(sql, (kw, kw, kw)).fetchall()
    if not rows:
        print("没有命中「%s」。" % args.keyword)
        return
    for r in rows:
        print("%-4s %s" % (r["id"], r["source"]))
        print(wrap(r["summary"], indent="     "))
    print("\n共 %d 条。" % len(rows))


def cmd_show(conn, args):
    r = conn.execute(
        "SELECT p.*, s.title, s.section, s.author, s.period, s.date, s.url, "
        "(SELECT GROUP_CONCAT(t.name, '、') FROM passage_topics pt "
        " JOIN topics t ON t.id = pt.topic_id WHERE pt.passage_id = p.id) AS topics "
        "FROM passages p JOIN sources s ON s.id = p.source_id WHERE p.id = ?",
        (args.id.upper(),),
    ).fetchone()
    if not r:
        print("没有这个条目：%s" % args.id)
        return
    print("%s  %s·%s" % (r["id"], r["title"], r["section"]))
    print("位置：%s（%s）" % (r["locator"], r["quote_type"]))
    print("主题：%s｜地点：%s｜文类：%s" % (
        r["topics"] or "—", r["place"] or "—", r["evidence"] or "—"))
    print("史料判断：%s" % (r["historicity"] or "—"))
    print()
    print("原文：")
    print(wrap(r["quote"]))
    print()
    print("摘要：")
    print(wrap(r["summary"]))
    if r["note"]:
        print()
        print("按：")
        print(wrap(r["note"]))
    print()
    print("出处：%s·%s（%s，%s）" % (r["title"], r["section"], r["author"], r["date"]))
    print(r["url"])


def cmd_dates(conn, args):
    for r in conn.execute(
        "SELECT d.*, s.title, s.section FROM date_claims d "
        "LEFT JOIN sources s ON s.id = d.source_id ORDER BY d.id"
    ):
        print("%s  %s" % (r["id"], r["gregorian"] or "—"))
        print(wrap(r["claim"], indent="    "))
        print("    状态：%s｜来源：%s·%s" % (
            r["status"] or "—", r["title"] or "—", r["section"] or "—"))
        if r["note"]:
            print(wrap(r["note"], indent="    "))
        print()


def cmd_objects(conn, args):
    for r in conn.execute("SELECT * FROM objects ORDER BY id"):
        print("%s  %s（%s）" % (r["id"], r["name"], r["type"]))
        print("    年代：%s｜地点：%s" % (r["date"], r["place"] or "—"))
        print(wrap(r["description"], indent="    "))
        print("    状态：%s" % (r["status"] or "—"))
        print()


def cmd_scholarship(conn, args):
    for r in conn.execute(
        "SELECT * FROM scholarship ORDER BY core DESC, id"
    ):
        flag = "核心" if r["core"] else "线索"
        print("%s  [%s] %s" % (r["id"], flag, r["title"]))
        print("    %s｜%s｜%s｜%s" % (
            r["author"], r["publication"], r["year"], r["pages"]))
        if r["doi"]:
            print("    https://doi.org/%s" % r["doi"])
        print(wrap("论点：" + (r["argument"] or "—"), indent="    "))
        print(wrap("与本库关系：" + (r["relation"] or "—"), indent="    "))
        print("    阅读状态：%s" % (r["read_status"] or "—"))
        print()


def main(argv=None):
    parser = argparse.ArgumentParser(description="孔子见老子史料数据库查询")
    parser.add_argument("--db", default=DEFAULT_DB, help="数据库路径")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("stats", help="总览")
    sub.add_parser("sources", help="文献列表")
    sub.add_parser("topics", help="主题列表")
    sub.add_parser("dates", help="系年异说")
    sub.add_parser("objects", help="碑刻与图像")
    sub.add_parser("scholarship", help="研究文献")

    p_list = sub.add_parser("list", help="条目列表")
    p_list.add_argument("--topic", help="按主题名筛选，如 问礼")
    p_list.add_argument("--source", help="按文献 ID 筛选，如 S03")
    p_list.add_argument("--evidence", help="按文类筛选，如 寓言")

    p_search = sub.add_parser("search", help="全文检索")
    p_search.add_argument("keyword")

    p_show = sub.add_parser("show", help="看一条全文")
    p_show.add_argument("id")

    args = parser.parse_args(argv)
    conn = connect(args.db)
    try:
        cmd = {
            "stats": cmd_stats, "sources": cmd_sources, "topics": cmd_topics,
            "list": cmd_list, "search": cmd_search, "show": cmd_show,
            "dates": cmd_dates, "objects": cmd_objects,
            "scholarship": cmd_scholarship,
        }.get(args.command, cmd_stats)
        cmd(conn, args)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
