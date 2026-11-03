#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 records.json 中的繁体字转换为简体字（默认就地覆盖）。

依赖
----
    pip install zhconv

说明
----
    * 递归遍历 JSON，把所有字符串值（topic / criteria / volume / section /
      terms / category / text 等）转换为简体，保持键顺序与结构不变。
    * 键名（英文）与数字、日期等非字符串字段不受影响。
    * 默认输入 = 输出 = 脚本同目录下的 records.json（就地覆盖）。

用法
----
    python simplify.py                      # records.json 就地转简体
    python simplify.py in.json out.json     # 也可指定输入/输出文件
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(HERE, "records.json")


def _load_converter():
    try:
        import zhconv
    except ImportError:
        sys.stderr.write(
            "ERROR: 需要 zhconv 库。请先安装：\n"
            "    python -m pip install zhconv\n"
        )
        raise SystemExit(1)

    def convert(text: str) -> str:
        return zhconv.convert(text, "zh-cn")

    return convert


def to_simplified(obj, convert):
    """递归地把 JSON 对象中的所有字符串转为简体。"""
    if isinstance(obj, str):
        return convert(obj)
    if isinstance(obj, list):
        return [to_simplified(x, convert) for x in obj]
    if isinstance(obj, dict):
        return {k: to_simplified(v, convert) for k, v in obj.items()}
    return obj


def main(argv):
    src = argv[1] if len(argv) > 1 else DEFAULT_FILE
    dst = argv[2] if len(argv) > 2 else src  # 默认就地覆盖

    if not os.path.isfile(src):
        sys.stderr.write("ERROR: file not found: %s\n" % src)
        return 1

    convert = _load_converter()

    with open(src, "r", encoding="utf-8") as fh:
        doc = json.load(fh)

    simplified = to_simplified(doc, convert)

    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(simplified, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("Simplified %d records -> %s" % (len(simplified.get("records", [])), dst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
