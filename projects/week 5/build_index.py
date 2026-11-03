#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
由 greatwall.db 生成前端页面 index.html。

生成逻辑已并入 server.py（server.build_index / server.render_index）——
server.py 启动时也会自动生成 index.html；本脚本只是命令行封装，便于单独重建。

用法
----
    python3 build_index.py            # greatwall.db -> index.html
    python3 build_index.py out.html   # 指定输出文件
"""

import os
import sys

from server import DB_PATH, INDEX_PATH, build_index


def main(argv):
    out_path = argv[1] if len(argv) > 1 else INDEX_PATH
    if not os.path.isfile(DB_PATH):
        sys.stderr.write("ERROR: 数据库不存在：%s（请先运行 build_db.py）\n" % DB_PATH)
        return 1
    total, nc, nt, ns = build_index(DB_PATH, out_path)
    print("Wrote %s  (records=%d, categories=%d, terms=%d, sections=%d)"
          % (out_path, total, nc, nt, ns))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
