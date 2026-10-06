"""A minimal app: a browser page, this server, a model, and a database.

    python3 server.py        then open http://localhost:8000

Standard library only. Nothing to install.
"""
import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / ".." / ".." / "week-03" / "demo-buildings" / "buildings.db"
ARCHIVE = DB.parent                      # the archive photos live beside the database
FIXTURE = HERE / "fixtures" / "model-response.json"
PORT = int(os.environ.get("PORT", 8000))   # busy? run: PORT=8765 python3 server.py


def ask_model(image: bytes) -> dict:
    """THE ONE SPOT TO REPLACE.

    A real version sends the image to a model API (for example DeepSeek) and
    asks which building it shows, answering in JSON:
        {"building_id": ..., "confidence": ..., "reason": ...}

    This demo does not call any model. It returns the same saved answer for
    every photo (fixtures/model-response.json), and says so ("source": "fixture").
    """
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def find_building(building_id):
    if building_id is None:
        return None
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    row = con.execute("SELECT * FROM buildings WHERE id = ?", (building_id,)).fetchone()
    con.close()
    return dict(row) if row else None


class Handler(BaseHTTPRequestHandler):
    def send(self, status, body: bytes, kind: str):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self.send(200, (HERE / "static" / "index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path.startswith("/archive/"):
            name = Path(self.path).name                      # images/bld-04.jpg -> bld-04.jpg only
            file = ARCHIVE / "images" / name
            if file.is_file():
                return self.send(200, file.read_bytes(), "image/jpeg")
        self.send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/identify":
            return self.send(404, b"not found", "text/plain")
        image = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        answer = ask_model(image)                            # 1. ask the model
        building = find_building(answer.get("building_id"))  # 2. look it up in the database
        body = json.dumps({"model": answer, "building": building}, ensure_ascii=False)
        self.send(200, body.encode("utf-8"), "application/json; charset=utf-8")

    def log_message(self, fmt, *args):
        print("  " + fmt % args)


if __name__ == "__main__":
    print(f"Open http://localhost:{PORT}   (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
