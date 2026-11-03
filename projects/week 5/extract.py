#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从《明史》（明史.txt）中提取关于长城的记载，生成 records.json。

说明
----
明代称长城为“边墙”，《明史》中相关用字有：
    邊牆(U+7246) / 邊墻(U+58BB) / 邊垣 / 塞垣 / 大牆（提調大牆）
另有“長城”一词，多用作关隘名（長城關）或比喻（倚之若長城）。

收录标准（“只收长城/边墙本体记载”）：
    * 收录：明确记载长城/边墙本体的段落——修筑、增建、损毁（地震/水患/被攻破）、
      地理建置、关隘、职官、方略议论、戍守作用等。
    * 排除：比喻用法（如“倚之若長城”）、与长城无关的同名地名
      （長城嶺、長城山、長城島、牆子嶺、蒙牆口、蕭牆、高牆等）
      以及城/宫/庙/围/狱等普通墙垣。

因“收录/排除”依赖逐条人工判断，本脚本把经人工校订后的行号→类别映射
（INCLUDE）内置其中，再据此从原文抽取整段文字，保证结果可复现。

用法
----
    python extract.py [源文件] [输出文件]
默认：脚本同目录下的 明史.txt  ->  records.json
"""

import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SOURCE = os.path.join(HERE, "明史.txt")
DEFAULT_OUTPUT = os.path.join(HERE, "records.json")

# ---------------------------------------------------------------------------
# 人工校订后的收录清单：源文件行号(1-based) -> 记载类别
# ---------------------------------------------------------------------------
INCLUDE = {
    2055: "修筑",      # 築邊牆自紫城砦至花馬池
    2458: "修筑",      # 罷修邊垣
    4803: "损毁",      # 大水，邊垣多圮
    4914: "损毁",      # 霪雨，圮南山邊垣
    5009: "损毁",      # 地震，傾倒邊牆、墩臺
    5013: "损毁",      # 地震，圮邊牆
    5019: "损毁",      # 地震，邊牆、墩臺悉圮
    7667: "地理建置",  # 榆林衛：又北有邊牆，成化九年築
    7681: "关隘",      # 寧夏後衛：東有長城關
    13334: "职官",     # 延綏：提調大牆及牆口等處
    13827: "边禁",     # 互市：非互市日，毋輒近塞垣
    14704: "修筑",     # 築橫城堡邊牆
    15069: "修筑",     # 請修塞垣
    15076: "修筑",     # 所築塞垣僅四十餘里
    15088: "修筑",     # 請修築宣、大邊牆千餘里
    15090: "修筑",     # 薊鎮：宜築牆建臺
    16824: "修筑",     # 寧夏築邊牆，鼒枋出銀米佐工
    22367: "行经",     # 循塞垣而西
    22810: "修筑",     # 與子俊築邊墻，增營堡
    22812: "战事",     # 寇分數道入，寧蹙之邊墻
    22830: "修筑",     # 余子俊築邊墻
    22832: "修筑",     # 玉督邊墻工峻急
    22999: "修筑",     # 余子俊築邊墻，命英董役
    23325: "修筑",     # 隨形勢為溝墻
    23446: "修筑",     # 請沿邊築墻建堡 / 以成邊墻
    23448: "修筑",     # 臣前請築墻建堡
    23450: "修筑",     # 東起清水營，西抵花馬池……鑿崖築墻
    23456: "作用",     # 寇扼於墻塹，散漫不得出
    23460: "方略",     # 請以延綏邊墻法行之兩鎮
    24031: "议论",     # 謂築邊墻糜費 / 一清為國修邊
    24594: "修筑",     # 築大同邊墻六百里
    24672: "修筑",     # 築邊墻自山海關迄開原靉陽堡
    24769: "修筑",     # 建議增築塞垣……地近邊垣
    26076: "修筑",     # 築邊墻綿亙二百餘里 / 寇毀墻入
    26080: "修筑",     # 平衍宜墻者百三十一里 / 使一清築墻
    26090: "方略",     # 請增築邊墻
    26126: "修筑",     # 諸邊各以農隙築墻浚濠
    26158: "修筑",     # 屢疏請修築邊墻
    26164: "损毁",     # 萬一如往年潰墻而入
    26168: "修筑",     # 修大同西路、宣府東路邊墻
    26170: "作用",     # 墻堞近遠……墻內戍者得以暇耕牧
    26245: "修筑",     # 又築蘭州邊垣
    26259: "修筑",     # 罷築薊鎮邊垣
    26332: "修筑",     # 歲當繕邊垣
    26344: "修筑",     # 築東路邊牆百三十八里
    26366: "修筑",     # 修邊牆濠塹
    26612: "修筑",     # 築邊垣萬一千八百餘丈
    26759: "修筑",     # 役軍築邊牆
    26781: "修筑",     # 尋以築邊垣，賚銀幣
    26814: "修筑",     # 修邊墻三百九十餘里
    26818: "损毁",     # 於萬全右衛毀墻入
    26830: "修筑",     # 築邊墻禦寇
    26884: "修筑",     # 宜大修邊墻
    26896: "损毁",     # 自墻子嶺、磨刀峪潰墻入犯
    26975: "议论",     # 言修治邊墻非上策
    27338: "修筑",     # 時方大修邊墻，之鸞董役
    27909: "修筑",     # 築墻百二十里 / 王瓊築邊墻
    27915: "修筑",     # 議築邊墻……敵臺千餘
    28080: "增筑墩台",  # 邊牆雖修，墩台未建……請跨牆為台
    28286: "战事",     # 犯薊鎮，攻墻
    28288: "修筑",     # 大同墻圮，繕治為急……修……諸墻塹
    28290: "修筑",     # 議築故總督翁萬達所創邊墻
    28296: "议论",     # 議者以守墻為怯……墻外邀擊
    29086: "增筑墩台",  # 築敵臺三千，起居庸至山海
    29102: "关隘",     # 出花馬池、長城關與戰
    29340: "修筑",     # 兵部尚書趙錦檄畿輔民築塞垣
    29386: "修筑",     # 築邊墻萬余丈
    29449: "修筑",     # 修築黃花鎮、古北口邊墻
    30136: "修筑",     # 築邊墻萬有餘丈
    30692: "损毁",     # 朵顏兀露絲罕……毀牆入
    30696: "损毁",     # 敵方分騎繞牆入
    30859: "损毁",     # 由沙梁隤牆入
    30873: "修筑",     # 松山既復，為築邊垣
    31954: "修筑",     # 修塞垣，繕戰壘
    32472: "修筑",     # 以閑修築邊墻
    42329: "修筑",     # 議築邊牆，設立臺堡
    42387: "损毁",     # 別遣精騎從間道潰牆入
    42391: "损毁",     # 墮諸邊垣
    42395: "战事",     # 攻薊鎮牆，百道並進
}

# 表示长城的专用词（按优先级）；若均未命中，则回退到裸字“牆/墻”
WALL_TERMS = ["長城", "邊牆", "邊墻", "邊垣", "塞垣", "大牆"]
BARE_WALL = ["牆", "墻"]

JUAN_RE = re.compile(r"^卷[一二三四五六七八九十百零〇]+$")

TOPIC = "长城在明代多称“边墙”，亦称“边垣/塞垣/大墙”；“长城”一词多见于关隘名及比喻"
CRITERIA = ("收录明确记载长城/边墙本体的段落：修筑、增建、损毁、地理建置、关隘、"
            "职官、方略议论等；排除比喻用法（如“倚之若长城”）及与长城无关的"
            "同名地名（长城岭、长城山、长城岛、墙子岭、蒙墙口等）和城/宫/庙/围/狱等墙。")


def split_lines(raw: str):
    """按 .NET ReadAllLines 的方式切分（\\r\\n | \\r | \\n），并去掉末尾空行。"""
    lines = re.split(r"\r\n|\r|\n", raw)
    if lines and lines[-1] == "":
        lines.pop()
    return lines


_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
           "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def zh_num(s: str) -> int:
    """解析中文数字，如 十三=13、一百十七=117、二百〇二=202、三百三十二=332。"""
    section = 0
    num = 0
    for ch in s:
        if ch in _DIGITS:
            num = _DIGITS[ch]
        elif ch == "十":
            section += (num or 1) * 10
            num = 0
        elif ch == "百":
            section += (num or 1) * 100
            num = 0
    return section + num


def section_of(juan: str) -> str:
    """由卷号推断所属部分：本纪(1-24)、志(25-99)、表(100-112)、列传(113-332)。"""
    n = zh_num(juan[1:])  # 去掉“卷”
    if n <= 24:
        return "本纪"
    if n <= 99:
        return "志"
    if n <= 112:
        return "表"
    return "列传"


def get_terms(text: str):
    """返回该段命中的长城用词。"""
    terms = [w for w in WALL_TERMS if w in text]
    if not terms:
        terms = [w for w in BARE_WALL if w in text]
    return terms


def build(source_path: str):
    with open(source_path, "r", encoding="utf-8") as fh:
        lines = split_lines(fh.read())

    # 卷号索引（记录每个“卷X”标题所在的行下标）
    juan_at = [(i, lines[i]) for i in range(len(lines)) if JUAN_RE.match(lines[i])]

    def volume_of(line_no: int) -> str:
        juan = ""
        for idx, name in juan_at:
            if idx <= line_no - 1:
                juan = name
            else:
                break
        return juan

    records = []
    for n, line_no in enumerate(sorted(INCLUDE), start=1):
        text = lines[line_no - 1]
        terms = get_terms(text)
        if not terms:
            print("WARNING: line %d has no wall term: %s" % (line_no, text[:30]))
        juan = volume_of(line_no)
        records.append({
            "id": "MZ-%03d" % n,
            "volume": juan,
            "section": section_of(juan),
            "line": line_no,
            "terms": terms,
            "category": INCLUDE[line_no],
            "text": text,
        })

    doc = {
        "source": os.path.basename(source_path),
        "source_path": source_path,
        "topic": TOPIC,
        "criteria": CRITERIA,
        "generated": date.today().isoformat(),
        "count": len(records),
        "records": records,
    }
    return doc


def main(argv):
    source = argv[1] if len(argv) > 1 else DEFAULT_SOURCE
    output = argv[2] if len(argv) > 2 else DEFAULT_OUTPUT

    if not os.path.isfile(source):
        print("ERROR: source file not found: %s" % source)
        return 1

    doc = build(source)
    with open(output, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("Wrote %d records -> %s" % (doc["count"], output))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
