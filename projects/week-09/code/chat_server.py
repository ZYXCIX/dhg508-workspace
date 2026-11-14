#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local server for the Confucius–Laozi scene.

It does two things:
  1. serves the week-09 directory (so /code/dialogue_scene.html works);
  2. exposes POST /api/chat, a small proxy to DeepSeek for free dialogue.

The API key stays on the server:
    Windows PowerShell:
        $env:DEEPSEEK_API_KEY="sk-..."
        python code/chat_server.py
    macOS / Linux:
        export DEEPSEEK_API_KEY="sk-..."
        python code/chat_server.py

Then open:
    http://127.0.0.1:8000/code/dialogue_scene.html

If DEEPSEEK_API_KEY is missing, /api/chat returns 503 and the page falls back
to its local improvisation pool. The fixed script never depends on the API.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_URL = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()

SYSTEM_PROMPT = """你在为一件教学用的历史想象作品写对话，不是写史料。
场景：春秋晚期，周守藏室。孔子适周问礼，见到周守藏室之史老子。两人席地而坐，也可以起身走动。

人物：
- 孔子：鲁国人，约三十余岁，重视礼、仁、君子，知其不可而为之；语气温和、执着，会化用《论语》，但不说后世才有的词。
- 老子：年长，周守藏室史，主张道法自然、无为、上善若水；语气简短，常反问，不把自己的话当教条。

写作要求：
1. 只写孔子和老子各一句，形成一轮对话；每句 15–60 字。
2. 文言与口语混合，自然、有生活气；可以化用《论语》《老子》《庄子》《史记》的句子，但不要标出处，不要伪造引文。
3. 不写旁白、动作说明、现代词汇、电影台词。
4. 不重复此前出现过的句子；接着上文的意思往下说。
5. 这是教学拟构；不要声称是真实记录。

只输出 JSON，不要 Markdown 代码块：
{"kong":"孔子的下一句","lao":"老子的下一句","topic":"两个字的话题"}"""


def _strip_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3]
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    return text.strip()


def call_model(history: list, question: str) -> dict:
    lines = []
    for item in (history or [])[-10:]:
        who = str(item.get("who", "")).strip()
        cls = str(item.get("cls", "")).strip()
        if who in ("孔子", "老子", "你") and cls:
            lines.append("%s：%s" % (who, cls))

    user = "此前的对话：\n" + ("\n".join(lines) if lines else "（还没有对话）")
    if question:
        user += "\n\n学生刚刚说：%s" % question
    user += "\n\n请写下一轮。只输出 JSON。"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
        ],
        "temperature": 0.9,
        "max_tokens": 300,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % API_KEY,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    content = data["choices"][0]["message"]["content"]
    obj = json.loads(_strip_fence(content))

    kong = str(obj.get("kong", "")).strip()
    lao = str(obj.get("lao", "")).strip()
    topic = str(obj.get("topic", "即兴")).strip() or "即兴"
    if not kong or not lao:
        raise ValueError("model returned empty dialogue")
    return {"kong": kong[:200], "lao": lao[:200], "topic": topic[:20]}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def _send_json(self, obj: dict, code: int = 200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/api/health":
            if API_KEY:
                self._send_json({"ok": True, "model": MODEL})
            else:
                # Keep health at 200 so the page can fall back without a
                # browser console error. /api/chat still returns 503.
                self._send_json(
                    {"ok": False, "error": "DEEPSEEK_API_KEY not set"}
                )
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/chat":
            self.send_error(404)
            return
        if not API_KEY:
            self._send_json(
                {"ok": False, "error": "DEEPSEEK_API_KEY not set"}, 503
            )
            return

        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(raw)
        except Exception as exc:
            self._send_json({"ok": False, "error": "bad JSON: %s" % exc}, 400)
            return

        try:
            result = call_model(payload.get("history", []), payload.get("question", ""))
            self._send_json({"ok": True, **result})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:300]
            self._send_json(
                {"ok": False, "error": "upstream HTTP %s: %s" % (exc.code, detail)}, 502
            )
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)[:300]}, 502)


def main(argv):
    port = int(os.environ.get("PORT", argv[1] if len(argv) > 1 else "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("Serving %s" % PROJECT)
    print("Open http://127.0.0.1:%d/code/dialogue_scene.html" % port)
    if API_KEY:
        print("Free dialogue: DeepSeek (%s)" % MODEL)
    else:
        print("DEEPSEEK_API_KEY not set: free dialogue will use the local pool.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
