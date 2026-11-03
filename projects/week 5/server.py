#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
greatwall.db 的只读 HTTP 后端 + 前端页面生成器。

index.html（记载检索列表）在本服务启动时由 greatwall.db 生成：页面的
静态部分（信息框、筛选标签及计数、总条数）写入 HTML，记载列表（检索/
筛选/分页）在运行时由 /api/records 提供。

提供：
    GET /                      -> index.html（若数据库比页面新则自动重新生成）
    GET /health                -> {"status":"ok"}
    GET /api/rebuild           -> 由 greatwall.db 重新生成 index.html
    GET /api/meta              -> meta 表（数据源、主题、收录标准、日期…）
    GET /api/stats             -> 汇总统计（总数、按类别/部分/用词）
    GET /api/records           -> 记录列表（支持筛选与分页）
        参数：q 全文关键词、category 类别、section 部分、term 用词、
              page 页码(默认1)、page_size 每页(默认10，最大100)

仅使用 Python 标准库，无需安装依赖。

用法
----
    python server.py                 # http://127.0.0.1:8000
    python server.py 0.0.0.0 8080    # 指定地址与端口
"""

import html
import json
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "greatwall.db")
INDEX_PATH = os.path.join(HERE, "index.html")
MAP_PATH = os.path.join(HERE, "map.html")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
MAX_PAGE_SIZE = 100
TITLE = "中国长城数据库"


# ---------------------------------------------------------------------------
# index.html 模板与生成逻辑
#   页面静态部分（标题、信息框、筛选标签及计数、总条数）在生成时由
#   greatwall.db 写入；记载列表（检索/筛选/分页）在运行时由本服务的
#   /api/records 提供。
# ---------------------------------------------------------------------------
PAGE = r"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{
    --bg:#f6f3ec; --panel:#fffdf8; --ink:#2b2622; --muted:#7d746a;
    --line:#e4ddcf; --accent:#8c2f24; --accent-soft:#f3e3df;
    --chip:#efe9dc; --chip-on:#8c2f24;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;line-height:1.6}
  header{background:linear-gradient(180deg,#7f2a20,#6a231b);color:#fdf8f2;padding:26px 20px 22px}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px;text-align:center}
  header h1{margin:0 0 6px;font-size:24px;letter-spacing:2px;font-weight:600}
  main{max-width:1080px;margin:0 auto;padding:22px 20px 60px}
  .meta{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);
        border-radius:8px;padding:12px 16px;font-size:13px;color:var(--muted);margin-bottom:18px}
  .meta b{color:var(--ink)}
  .controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
  .search{flex:1;min-width:220px;display:flex;gap:8px}
  input[type=text]{flex:1;padding:10px 12px;border:1px solid var(--line);border-radius:8px;
                   background:var(--panel);font-size:14px;color:var(--ink)}
  input[type=text]:focus{outline:2px solid var(--accent-soft);border-color:var(--accent)}
  button{padding:9px 14px;border:1px solid var(--line);background:var(--panel);color:var(--ink);
         border-radius:8px;cursor:pointer;font-size:14px}
  button:hover{border-color:var(--accent)}
  button:disabled{opacity:.45;cursor:default}
  .stats{background:var(--panel);border:1px solid var(--line);border-radius:8px;
         padding:12px 16px;margin-bottom:18px}
  .statrow{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:6px 0}
  .statrow .label{font-size:12px;color:var(--muted);width:52px;flex:none}
  .chip{display:inline-block;padding:3px 10px;border-radius:999px;background:var(--chip);
        font-size:12.5px;cursor:pointer;border:1px solid transparent}
  .chip:hover{border-color:var(--accent)}
  .chip.on{background:var(--chip-on);color:#fff}
  .count{font-size:13px;color:var(--muted);margin:4px 0 12px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;
        padding:14px 16px;margin-bottom:12px}
  .card .top{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
  .id{font-family:ui-monospace,Consolas,monospace;font-size:12px;color:var(--muted)}
  .badge{font-size:12px;padding:2px 8px;border-radius:6px;background:var(--accent-soft);color:var(--accent)}
  .badge.term{background:#e6efe4;color:#3c6b39}
  .badge.vol{background:#e8eef5;color:#38567b}
  .text{font-family:"Songti SC","SimSun",Georgia,serif;font-size:16px;line-height:1.95;
        text-align:justify}
  .pager{display:flex;gap:10px;align-items:center;justify-content:center;margin-top:22px;color:var(--muted);font-size:14px}
  .empty{text-align:center;color:var(--muted);padding:40px 0}
  footer{text-align:center;color:var(--muted);font-size:12px;padding:10px 0 30px}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>__TITLE__</h1>
    <div style="margin-top:10px">
      <a href="/map.html" style="display:inline-block;color:#fff;background:rgba(255,255,255,.14);
         border:1px solid rgba(255,255,255,.45);padding:6px 14px;border-radius:8px;
         text-decoration:none;font-size:13.5px">🗺 在中国地图上查看长城位置 →</a>
    </div>
  </div>
</header>
<main>
  <!-- 以下信息框与筛选标签由 server.py 从 greatwall.db 生成 -->
  <div class="meta" id="meta">
__META__
  </div>

  <div class="controls">
    <div class="search">
      <input type="text" id="q" placeholder="全文检索，如：边墙 / 墩台 / 戚继光 / 花马池 …">
      <button id="searchBtn">检索</button>
      <button id="resetBtn">重置</button>
    </div>
  </div>

  <div class="stats" id="stats">
__CHIPS__
  </div>
  <div class="count" id="count"></div>
  <div id="list"><div class="empty">载入中…</div></div>
  <div class="pager" id="pager"></div>
  <footer>数据源：《明史》· 共 __COUNT__ 条（简体）· 后端 server.py + greatwall.db</footer>
</main>

<script>
/* 记载列表由后端 server.py 提供：GET /api/records?q=&category=&term=&section=&page=&page_size= */
const state = {q:"", category:"", section:"", term:"", page:1, page_size:10};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"']/g,
  (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

async function api(path){
  const res = await fetch(path);
  if(!res.ok) throw new Error("HTTP " + res.status);
  return res.json();
}

function queryString(){
  const p = new URLSearchParams();
  if(state.q) p.set("q", state.q);
  if(state.category) p.set("category", state.category);
  if(state.section) p.set("section", state.section);
  if(state.term) p.set("term", state.term);
  p.set("page", state.page);
  p.set("page_size", state.page_size);
  return p.toString();
}

async function loadRecords(){
  const d = await api("/api/records?" + queryString());
  const list = $("list");
  if(!d.records.length){ list.innerHTML = `<div class="empty">没有匹配的记载</div>`; }
  else {
    list.innerHTML = d.records.map(r => `
      <div class="card">
        <div class="top">
          <span class="id">${esc(r.id)}</span>
          <span class="badge vol">${esc(r.volume)}</span>
          <span class="badge">${esc(r.section)}</span>
          <span class="badge">${esc(r.category)}</span>
          ${(r.terms||[]).map(t=>`<span class="badge term">${esc(t)}</span>`).join("")}
          <span class="id">行 ${r.line}</span>
        </div>
        <div class="text">${esc(r.text)}</div>
      </div>`).join("");
  }
  const pages = Math.max(1, Math.ceil(d.total / d.page_size));
  $("count").textContent = `共 ${d.total} 条　·　第 ${d.page} / ${pages} 页`;
  $("pager").innerHTML =
    `<button id="prev" ${d.page<=1?"disabled":""}>上一页</button>` +
    `<span>${d.page} / ${pages}</span>` +
    `<button id="next" ${d.page>=pages?"disabled":""}>下一页</button>` +
    `<select id="ps">${[10,20,50,100].map(n=>`<option ${n===d.page_size?"selected":""}>${n}</option>`).join("")}</select>`;
  $("prev").onclick = () => { if(state.page>1){ state.page--; render(); } };
  $("next").onclick = () => { if(state.page<pages){ state.page++; render(); } };
  $("ps").onchange = (e) => { state.page_size = +e.target.value; state.page = 1; render(); };
}

async function render(){
  try{ await loadRecords(); }
  catch(e){ $("list").innerHTML = `<div class="empty">加载失败：${esc(e.message)}</div>`; }
}

/* 筛选标签（生成时写入 DOM） */
$("stats").querySelectorAll(".chip").forEach(el => {
  el.onclick = () => {
    const k = el.dataset.k, v = el.dataset.v;
    state[k] = (state[k] === v) ? "" : v;
    state.page = 1;
    $("stats").querySelectorAll(`.chip[data-k="${k}"]`).forEach(c =>
      c.classList.toggle("on", c.dataset.v === state[k]));
    render();
  };
});

$("searchBtn").onclick = () => { state.q = $("q").value.trim(); state.page = 1; render(); };
$("q").addEventListener("keydown", (e)=>{ if(e.key==="Enter") $("searchBtn").click(); });
$("resetBtn").onclick = () => {
  Object.assign(state, {q:"", category:"", section:"", term:"", page:1});
  $("q").value = "";
  $("stats").querySelectorAll(".chip").forEach(c => c.classList.toggle("on", c.dataset.v === ""));
  render();
};

render();
</script>
</body>
</html>
"""


def _esc(v):
    return html.escape(str(v if v is not None else ""), quote=True)


def _statrow(label, key, rows, namekey):
    out = [f'<div class="statrow"><span class="label">{_esc(label)}</span>',
           f'<span class="chip on" data-k="{key}" data-v="">全部</span>']
    for r in rows:
        v = r[namekey]
        out.append(f'<span class="chip" data-k="{key}" data-v="{_esc(v)}">{_esc(v)} {r["n"]}</span>')
    out.append("</div>")
    return "".join(out)


def render_index(conn):
    """由 greatwall.db 的现有连接渲染 index.html（返回页面文本与各项计数）。"""
    meta = {r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM meta")}
    total = conn.execute("SELECT COUNT(*) n FROM records").fetchone()["n"]
    by_category = conn.execute(
        "SELECT category, COUNT(*) n FROM records GROUP BY category ORDER BY n DESC, category"
    ).fetchall()
    by_term = conn.execute(
        "SELECT term, COUNT(*) n FROM record_terms GROUP BY term ORDER BY n DESC, term"
    ).fetchall()
    by_section = conn.execute(
        "SELECT section, COUNT(*) n FROM records GROUP BY section ORDER BY n DESC, section"
    ).fetchall()

    meta_html = "\n".join([
        f'    <div><b>收录标准：</b>{_esc(meta.get("criteria"))}</div>',
        f'    <div style="margin-top:4px"><b>备注：</b>{_esc(meta.get("topic"))}</div>',
        f'    <div style="margin-top:4px"><b>数据源：</b>{_esc(meta.get("source"))}'
        f' · 生成日期 {_esc(meta.get("generated"))}</div>',
    ])
    chips_html = "\n".join([
        "    " + _statrow("类别", "category", by_category, "category"),
        "    " + _statrow("用词", "term", by_term, "term"),
        "    " + _statrow("部分", "section", by_section, "section"),
    ])
    page = (PAGE
            .replace("__TITLE__", _esc(TITLE))
            .replace("__META__", meta_html)
            .replace("__CHIPS__", chips_html)
            .replace("__COUNT__", str(total)))
    return page, total, len(by_category), len(by_term), len(by_section)


def build_index(db_path=DB_PATH, out_path=INDEX_PATH):
    """读取 greatwall.db 并写出 index.html；返回 (总数, 类别数, 用词数, 部分数)。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        page, total, nc, nt, ns = render_index(conn)
    finally:
        conn.close()
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    return total, nc, nt, ns


def index_is_stale():
    """index.html 不存在、或比 greatwall.db 旧时为 True。"""
    if not os.path.isfile(INDEX_PATH):
        return True
    try:
        return os.path.getmtime(DB_PATH) > os.path.getmtime(INDEX_PATH)
    except OSError:
        return True


def query_db(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def get_meta():
    rows = query_db("SELECT key, value FROM meta")
    return {r["key"]: r["value"] for r in rows}


def get_stats():
    return {
        "total": query_db("SELECT COUNT(*) AS n FROM records")[0]["n"],
        "by_category": query_db(
            "SELECT category, COUNT(*) AS n FROM records "
            "GROUP BY category ORDER BY n DESC, category"
        ),
        "by_section": query_db(
            "SELECT section, COUNT(*) AS n FROM records "
            "GROUP BY section ORDER BY n DESC, section"
        ),
        "by_term": query_db(
            "SELECT term, COUNT(*) AS n FROM record_terms "
            "GROUP BY term ORDER BY n DESC, term"
        ),
    }


def get_rasters():
    return query_db(
        "SELECT name, mime, width, height, minx, miny, maxx, maxy FROM geo_rasters"
    )


def get_raster_blob(name):
    conn = sqlite3.connect(DB_PATH)
    try:
        return conn.execute(
            "SELECT mime, data FROM geo_rasters WHERE name = ?", (name,)
        ).fetchone()
    finally:
        conn.close()


def get_geo_layers():
    return query_db(
        "SELECT layer, title, source, license, n FROM geo_layers ORDER BY layer"
    )


def get_geo_layer(layer):
    rows = query_db(
        "SELECT fid, name, geom, props FROM geo_features WHERE layer = ? ORDER BY fid",
        (layer,),
    )
    features = []
    for r in rows:
        props = json.loads(r["props"]) if r["props"] else {}
        props["name"] = r["name"]
        features.append(
            {"type": "Feature", "properties": props, "geometry": json.loads(r["geom"])}
        )
    return {"type": "FeatureCollection", "layer": layer, "features": features}


def get_records(params):
    q = params.get("q", [""])[0].strip()
    category = params.get("category", [""])[0].strip()
    section = params.get("section", [""])[0].strip()
    term = params.get("term", [""])[0].strip()
    try:
        page = max(1, int(params.get("page", ["1"])[0]))
    except ValueError:
        page = 1
    try:
        page_size = int(params.get("page_size", ["10"])[0])
    except ValueError:
        page_size = 10
    page_size = min(MAX_PAGE_SIZE, max(1, page_size))

    where, args = [], []
    if q:
        where.append("text LIKE ?")
        args.append("%" + q + "%")
    if category:
        where.append("category = ?")
        args.append(category)
    if section:
        where.append("section = ?")
        args.append(section)
    if term:
        where.append(
            "EXISTS (SELECT 1 FROM record_terms rt "
            "WHERE rt.record_id = records.id AND rt.term = ?)"
        )
        args.append(term)
    clause = ("WHERE " + " AND ".join(where)) if where else ""

    total = query_db("SELECT COUNT(*) AS n FROM records " + clause, args)[0]["n"]

    sql = (
        "SELECT id, volume, section, line, category, text, "
        "(SELECT GROUP_CONCAT(term, ',') FROM record_terms rt "
        " WHERE rt.record_id = records.id) AS terms "
        "FROM records " + clause + " ORDER BY line LIMIT ? OFFSET ?"
    )
    rows = query_db(sql, args + [page_size, (page - 1) * page_size])
    for r in rows:
        r["terms"] = r["terms"].split(",") if r["terms"] else []

    return {"total": total, "page": page, "page_size": page_size, "records": rows}


class Handler(BaseHTTPRequestHandler):
    server_version = "GreatWallServer/1.0"
    protocol_version = "HTTP/1.1"

    # -- helpers -----------------------------------------------------------
    def _send_bytes(self, body, ctype, status=200):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send_bytes(body, "application/json; charset=utf-8", status)

    def _send_file(self, path, ctype):
        if not os.path.isfile(path):
            self._send_json({"error": "not found: " + os.path.basename(path)}, 404)
            return
        with open(path, "rb") as fh:
            self._send_bytes(fh.read(), ctype)

    # -- routing -----------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        try:
            if path in ("/", "/index.html"):
                if index_is_stale():      # 数据库比页面新 -> 重新生成，保持同步
                    build_index()
                self._send_file(INDEX_PATH, "text/html; charset=utf-8")
            elif path == "/health":
                self._send_json({"status": "ok"})
            elif path == "/api/rebuild":  # 手动由 greatwall.db 重新生成 index.html
                total, nc, nt, ns = build_index()
                self._send_json({"ok": True, "records": total, "categories": nc,
                                 "terms": nt, "sections": ns})
            elif path in ("/map.html", "/map"):
                self._send_file(MAP_PATH, "text/html; charset=utf-8")
            elif path == "/api/meta":
                self._send_json(get_meta())
            elif path == "/api/stats":
                self._send_json(get_stats())
            elif path == "/api/records":
                self._send_json(get_records(params))
            elif path == "/api/geo/layers":
                self._send_json(get_geo_layers())
            elif path == "/api/geo/rasters":
                self._send_json(get_rasters())
            elif path.startswith("/api/geo/raster/"):
                row = get_raster_blob(path[len("/api/geo/raster/"):])
                if row is None:
                    self._send_json({"error": "no such raster"}, 404)
                else:
                    self._send_bytes(row[1], row[0])
            elif path.startswith("/api/geo/"):
                self._send_json(get_geo_layer(path[len("/api/geo/"):]))
            else:
                self._send_json({"error": "not found"}, 404)
        except BrokenPipeError:
            pass
        except Exception as exc:  # noqa: BLE001 - surface errors to the client
            self._send_json({"error": str(exc)}, 500)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class Server(ThreadingHTTPServer):
    """忽略客户端提前断开（浏览器刷新 / 关闭连接）产生的噪声。"""
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError)):
            return                      # 客户端断开属于正常现象，不打印堆栈
        super().handle_error(request, client_address)


def main(argv):
    host = argv[1] if len(argv) > 1 else DEFAULT_HOST
    try:
        port = int(argv[2]) if len(argv) > 2 else DEFAULT_PORT
    except ValueError:
        port = DEFAULT_PORT

    if not os.path.isfile(DB_PATH):
        sys.stderr.write("ERROR: database not found: %s\n" % DB_PATH)
        sys.stderr.write("Run: python build_db.py\n")
        return 1

    try:                                   # 启动时由 greatwall.db 生成 index.html
        total, nc, nt, ns = build_index()
        print("Built index.html  (records=%d, categories=%d, terms=%d, sections=%d)"
              % (total, nc, nt, ns))
    except Exception as exc:  # noqa: BLE001 - 生成失败不应阻止服务启动
        sys.stderr.write("WARN: could not build index.html: %s\n" % exc)

    httpd = Server((host, port), Handler)
    print("Serving on http://%s:%d/  (Ctrl+C to stop)" % (host, port))
    print("  DB   : %s" % DB_PATH)
    print("  Page : %s" % INDEX_PATH)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
