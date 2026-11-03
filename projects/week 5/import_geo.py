#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在 greatwall.db 中导入中国/周边地图数据与地形（栅格）数据。

数据来源
--------
    中国省级行政区（DataV.GeoAtlas，阿里云）
        https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json
    世界各国边界、海洋（Natural Earth 1:50m，public domain）
        https://github.com/nvkelso/natural-earth-vector  (geojson/)
    长城走向 / 长城关隘（MIT License）
        https://github.com/Adl3rAi/The-Great-Wall-of-China-geodata
    地形高程（Mapzen/AWS 开源地形瓦片 terrarium，公开发布）
        https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png

投影
----
    兰勃特等角圆锥投影（Lambert Conformal Conic，中国常用）
    标准纬线 25°N / 47°N，中央经线 105°E，原点纬度 35°N，球体半径 6371008.8 m
    —— 与前端 map.html 使用完全相同的参数，保证矢量与栅格套合。

写入表
------
    geo_layers(layer, title, source, license, n)
    geo_features(layer, fid, name, geom_type, geom)      -- 矢量（GeoJSON）
    geo_rasters(name, mime, width, height, minx, miny, maxx, maxy, data) -- 栅格

图层：china(省界)、world(各国)、ocean(海洋)、greatwall(长城走向)、passes(关隘)
栅格：terrain（投影后的地形晕渲 JPEG）

用法
----
    python import_geo.py            # 缺失时下载并导入（含地形）
    python import_geo.py --fresh    # 强制重新下载源数据
    python import_geo.py --no-terrain   # 跳过地形栅格
"""

import io
import json
import math
import os
import sys
import urllib.request

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "greatwall.db")

# --- 投影参数（必须与 map.html 一致）---------------------------------------
R = 6371008.8          # 球体半径（米）
LAT1, LAT2 = 25.0, 47.0
LAT0, LON0 = 35.0, 105.0
VIEW = dict(lon_min=70.0, lon_max=142.0, lat_min=14.0, lat_max=54.0)

SOURCES = {
    "china": {
        "file": os.path.join(HERE, "china_provinces.json"),
        "url": "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json",
        "title": "中国省级行政区", "license": "DataV.GeoAtlas (aliyun)", "simplify": 0.0,
    },
    "world": {
        "file": os.path.join(HERE, "ne_50m_countries.geojson"),
        "url": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson",
        "title": "世界各国", "license": "Natural Earth (public domain)", "simplify": 0.01,
    },
    "ocean": {
        "file": os.path.join(HERE, "ne_50m_ocean.geojson"),
        "url": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_ocean.geojson",
        "title": "海洋", "license": "Natural Earth (public domain)", "simplify": 0.01,
    },
    "greatwall": {
        "file": os.path.join(HERE, "gw_direction.geojson"),
        "url": "https://raw.githubusercontent.com/Adl3rAi/The-Great-Wall-of-China-geodata/HEAD/direction/fulldirection.geojson",
        "title": "明长城走向", "license": "MIT (Adl3rAi/The-Great-Wall-of-China-geodata)", "simplify": 0.0002,
    },
    "passes": {
        "file": os.path.join(HERE, "gw_passes.geojson"),
        "url": "https://raw.githubusercontent.com/Adl3rAi/The-Great-Wall-of-China-geodata/HEAD/passes/fullpasses.geojson",
        "title": "长城关隘", "license": "MIT (Adl3rAi/The-Great-Wall-of-China-geodata)", "simplify": 0.0,
    },
}

# --- 兰勃特等角圆锥 ---------------------------------------------------------
_d2r = math.radians
_p1, _p2, _p0, _l0 = _d2r(LAT1), _d2r(LAT2), _d2r(LAT0), _d2r(LON0)
N = math.log(math.cos(_p1) / math.cos(_p2)) / math.log(
    math.tan(math.pi / 4 + _p2 / 2) / math.tan(math.pi / 4 + _p1 / 2))
F = math.cos(_p1) * math.tan(math.pi / 4 + _p1 / 2) ** N / N
RHO0 = R * F / math.tan(math.pi / 4 + _p0 / 2) ** N


def proj(lon, lat):
    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(lat, dtype=float)
    rho = R * F / np.tan(np.pi / 4 + np.radians(lat) / 2) ** N
    th = N * np.radians(lon - LON0)
    return rho * np.sin(th), RHO0 - rho * np.cos(th)


def inv_proj(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rho = np.sign(N) * np.hypot(x, RHO0 - np.asarray(y, dtype=float))
    th = np.arctan2(x, RHO0 - y)
    lon = LON0 + np.degrees(th / N)
    lat = np.degrees(2 * np.arctan((R * F / rho) ** (1.0 / N)) - np.pi / 2)
    return lon, lat


def view_bounds():
    """VIEW 经纬度矩形的投影外包框（采样边界）。"""
    lons = np.linspace(VIEW["lon_min"], VIEW["lon_max"], 200)
    lats = np.linspace(VIEW["lat_min"], VIEW["lat_max"], 200)
    lo = np.concatenate([lons, lons, np.full(200, VIEW["lon_min"]), np.full(200, VIEW["lon_max"])])
    la = np.concatenate([np.full(200, VIEW["lat_min"]), np.full(200, VIEW["lat_max"]), lats, lats])
    x, y = proj(lo, la)
    return float(x.min()), float(y.min()), float(x.max()), float(y.max())


def raster_bounds():
    """当前地形栅格的范围（与 view_bounds 一致）。"""
    return view_bounds()


# --- 下载 / 抽稀 ------------------------------------------------------------
def download(url, path):
    print("  downloading %s" % url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as resp, open(path, "wb") as fh:
        fh.write(resp.read())


def ensure_source(key, spec, fresh=False):
    if fresh or not os.path.isfile(spec["file"]):
        download(spec["url"], spec["file"])
    with open(spec["file"], "r", encoding="utf-8") as fh:
        return json.load(fh)


def _perp(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(x - x1, y - y1)
    t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))


def _dp(points, eps):
    n = len(points)
    if n < 3:
        return list(points)
    keep = [False] * n
    keep[0] = keep[n - 1] = True
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        dmax, idx = 0.0, -1
        for k in range(i + 1, j):
            d = _perp(points[k], points[i], points[j])
            if d > dmax:
                dmax, idx = d, k
        if dmax > eps and idx > 0:
            keep[idx] = True
            stack.append((i, idx))
            stack.append((idx, j))
    return [points[k] for k in range(n) if keep[k]]


def _simplify_ring(ring, eps):
    closed = len(ring) > 2 and ring[0] == ring[-1]
    body = ring[:-1] if closed else ring
    out = _dp(body, eps)
    if closed:
        if len(out) < 3:
            out = body[:3]
        out = out + [out[0]]
    return out


def simplify_geometry(geom, eps):
    if not eps:
        return geom
    t, c = geom.get("type"), geom.get("coordinates")
    if t == "LineString":
        return dict(geom, coordinates=_simplify_ring(c, eps))
    if t == "MultiLineString":
        return dict(geom, coordinates=[_simplify_ring(r, eps) for r in c])
    if t == "Polygon":
        return dict(geom, coordinates=[_simplify_ring(r, eps) for r in c])
    if t == "MultiPolygon":
        return dict(geom, coordinates=[[_simplify_ring(r, eps) for r in poly] for poly in c])
    return geom


def count_points(geom):
    def flat(x):
        if x and isinstance(x[0], (int, float)):
            return 1
        return sum(flat(i) for i in x)
    c = geom.get("coordinates")
    return flat(c) if c else 0


def lat_range(geom):
    """返回几何体的纬度范围 (min, max)。"""
    lo, hi = 90.0, -90.0

    def walk(x):
        nonlocal lo, hi
        if x and isinstance(x[0], (int, float)):
            lat = x[1]
            if lat < lo:
                lo = lat
            if lat > hi:
                hi = lat
        else:
            for i in x:
                walk(i)

    walk(geom.get("coordinates"))
    return lo, hi


# --- 地形栅格（DEM 瓦片 -> 晕渲图）-----------------------------------------
TILE_Z = 6
TILE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/%d/%d/%d.png"


# 从源属性中保留的字段（用于前端标注/识别国家）
PROP_ALLOW = ("name", "NAME", "NAME_ZH", "ISO_A2", "ADMIN", "SOVEREIGNT", "adcode", "center", "centroid")


def _extract_meta(props):
    keep = {k: props[k] for k in PROP_ALLOW if k in props}
    name = props.get("NAME_ZH") or props.get("NAME") or props.get("name") or ""
    return name, keep


def _tile_xy(lon, lat, z):
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)
    return max(0, min(n - 1, x)), max(0, min(n - 1, y))


def _fetch_tile(z, x, y):
    from urllib.request import Request, urlopen
    req = Request(TILE_URL % (z, x, y), headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        img = Image.open(io.BytesIO(r.read())).convert("RGB")
    a = np.asarray(img).astype(np.float32)
    return x, y, (a[:, :, 0] * 256.0 + a[:, :, 1] + a[:, :, 2] / 256.0) - 32768.0


def build_dem(z=TILE_Z):
    pad = 1
    n = 2 ** z
    # 取投影外包框的边界反算经纬度范围，确保瓦片覆盖整幅输出
    minx, miny, maxx, maxy = raster_bounds()
    t = np.linspace(0.0, 1.0, 400)
    bx = np.concatenate([minx + (maxx - minx) * t, minx + (maxx - minx) * t,
                         np.full_like(t, minx), np.full_like(t, maxx)])
    by = np.concatenate([np.full_like(t, miny), np.full_like(t, maxy),
                         miny + (maxy - miny) * t, miny + (maxy - miny) * t])
    lon, lat = inv_proj(bx, by)
    x0, y0 = _tile_xy(float(np.min(lon)), float(np.max(lat)), z)
    x1, y1 = _tile_xy(float(np.max(lon)), float(np.min(lat)), z)
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(n - 1, x1 + pad), min(n - 1, y1 + pad)
    xs, ys = range(x0, x1 + 1), range(y0, y1 + 1)
    nx, ny = len(xs), len(ys)
    dem = np.zeros((ny * 256, nx * 256), dtype=np.float32)
    from concurrent.futures import ThreadPoolExecutor
    tasks = [(z, x, y) for y in ys for x in xs]
    print("  DEM tiles: %d x %d = %d" % (nx, ny, len(tasks)))
    done = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for x, y, tile in ex.map(lambda t: _fetch_tile(*t), tasks):
            dem[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = tile
            done += 1
            if done % 40 == 0:
                print("    %d/%d" % (done, len(tasks)))
    return dem, x0, y0, z


def _sample(dem, x0, y0, z, lon, lat):
    n = 2 ** z
    gx = (lon + 180.0) / 360.0 * n * 256.0 - x0 * 256.0
    gy = (1.0 - np.arcsinh(np.tan(np.radians(lat))) / np.pi) / 2.0 * n * 256.0 - y0 * 256.0
    gy = np.clip(gy, 0, dem.shape[0] - 1.001)
    gx = np.clip(gx, 0, dem.shape[1] - 1.001)
    x_i, y_i = gx.astype(int), gy.astype(int)
    fx, fy = gx - x_i, gy - y_i
    return (dem[y_i, x_i] * (1 - fx) * (1 - fy) + dem[y_i, x_i + 1] * fx * (1 - fy)
            + dem[y_i + 1, x_i] * (1 - fx) * fy + dem[y_i + 1, x_i + 1] * fx * fy)


SEA_STOPS = [(-6000, (12, 34, 66)), (-1500, (28, 66, 118)),
             (-200, (52, 104, 158)), (0, (92, 140, 178))]
LAND_STOPS = [(0, (108, 145, 96)), (200, (150, 172, 110)), (500, (188, 192, 122)),
              (1000, (208, 190, 132)), (2000, (196, 160, 112)), (3000, (172, 130, 92)),
              (4000, (150, 122, 96)), (5000, (176, 168, 158)), (6500, (235, 235, 235))]


def _ramp(v, stops):
    out = np.zeros(v.shape + (3,), dtype=np.float32)
    for i in range(len(stops) - 1):
        a, ca = stops[i]
        b, cb = stops[i + 1]
        m = (v >= a) & (v <= b)
        if not m.any():
            continue
        t = (v[m] - a) / (b - a)
        for k in range(3):
            out[..., k][m] = ca[k] + t * (cb[k] - ca[k])
    out[..., 0][v < stops[0][0]] = stops[0][1][0]
    out[..., 1][v < stops[0][0]] = stops[0][1][1]
    out[..., 2][v < stops[0][0]] = stops[0][1][2]
    for k in range(3):
        out[..., k][v > stops[-1][0]] = stops[-1][1][k]
    return out


def build_terrain_rasters(dem, x0, y0, z, out_w=2000):
    minx, miny, maxx, maxy = raster_bounds()
    aspect = (maxy - miny) / (maxx - minx)
    W = out_w
    H = max(200, int(round(W * aspect)))
    xs = np.linspace(minx, maxx, W)
    ys = np.linspace(maxy, miny, H)          # 上边界 -> 下边界
    X, Y = np.meshgrid(xs, ys)
    lon, lat = inv_proj(X, Y)
    E = _sample(dem, x0, y0, z, lon, lat)

    # 晕渲
    dx = (maxx - minx) / W
    dy = (maxy - miny) / H
    gy, gx = np.gradient(E, dy, dx)          # 轴0(y)用 dy，轴1(x)用 dx
    az, alt = math.radians(315.0), math.radians(45.0)
    slope = np.arctan(np.hypot(gx, gy))
    aspect_a = np.arctan2(gy, -gx)
    hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect_a)
    shade = np.clip(0.55 + 0.75 * hs, 0.35, 1.25)

    sea = E <= 0
    rgb = np.where(sea[..., None], _ramp(np.minimum(E, 0.0), SEA_STOPS),
                   _ramp(np.maximum(E, 0.0), LAND_STOPS))
    rgb = np.clip(rgb * shade[..., None], 0, 255).astype(np.uint8)

    buf = io.BytesIO()
    Image.fromarray(rgb, "RGB").save(buf, "JPEG", quality=88, optimize=True)
    return buf.getvalue(), W, H, minx, miny, maxx, maxy


# --- 主流程 -----------------------------------------------------------------
def build(fresh=False, terrain=True):
    import sqlite3

    layers, features = [], {}
    for key, spec in SOURCES.items():
        print("layer %-10s ..." % key)
        fc = ensure_source(key, spec, fresh)
        rows, pts = [], 0
        for feat in fc.get("features", []):
            geom = feat.get("geometry")
            if not geom:
                continue
            # 跳过极南要素（南极洲等）：在兰勃特投影下绕极点自相交，会填满整幅图
            if lat_range(geom)[1] < -5.0:
                continue
            geom = simplify_geometry(geom, spec["simplify"])
            pts += count_points(geom)
            nm, keep = _extract_meta(feat.get("properties") or {})
            rows.append((nm, geom["type"],
                         json.dumps(geom, ensure_ascii=False, separators=(",", ":")),
                         json.dumps(keep, ensure_ascii=False, separators=(",", ":"))))
        features[key] = rows
        layers.append((key, spec["title"], spec["url"], spec["license"], len(rows)))
        print("  features=%d points=%d" % (len(rows), pts))

    # 中国国界：由省级行政区（DataV，含藏南、台湾，符合中国主张）合并而成
    from shapely.geometry import shape, mapping
    from shapely.ops import unary_union
    from shapely import make_valid
    china_fc = ensure_source("china", SOURCES["china"])
    geoms = [make_valid(shape(f["geometry"]))
             for f in china_fc.get("features", []) if f.get("geometry")]
    union = simplify_geometry(json.loads(json.dumps(mapping(unary_union(geoms)))), 0.004)
    features["china_border"] = [("中国国界", union["type"],
        json.dumps(union, ensure_ascii=False, separators=(",", ":")), "{}")]
    layers.append(("china_border", "中国国界", "DataV 省级行政区合并",
                   "DataV.GeoAtlas (aliyun)", 1))
    print("layer %-10s ...\n  features=1 points=%d" % ("china_border", count_points(union)))

    rasters = []
    if terrain:
        print("terrain ...")
        dem, x0, y0, z = build_dem()
        data, W, H, minx, miny, maxx, maxy = build_terrain_rasters(dem, x0, y0, z)
        rasters.append(("terrain", "image/jpeg", W, H, minx, miny, maxx, maxy, data))
        print("  terrain %dx%d  %.0f KB" % (W, H, len(data) / 1024))

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(
            "DROP TABLE IF EXISTS geo_features;"
            "DROP TABLE IF EXISTS geo_layers;"
            "CREATE TABLE geo_layers(layer TEXT PRIMARY KEY, title TEXT, source TEXT,"
            "  license TEXT, n INTEGER);"
            "CREATE TABLE geo_features(layer TEXT NOT NULL, fid INTEGER NOT NULL, name TEXT,"
            "  geom_type TEXT NOT NULL, geom TEXT NOT NULL, props TEXT,"
            "  PRIMARY KEY(layer, fid));"
            "CREATE INDEX idx_geo_layer ON geo_features(layer);"
            "CREATE TABLE IF NOT EXISTS geo_rasters(name TEXT PRIMARY KEY, mime TEXT,"
            "  width INTEGER, height INTEGER, minx REAL, miny REAL, maxx REAL, maxy REAL,"
            "  data BLOB);"
        )
        conn.executemany("INSERT INTO geo_layers VALUES (?,?,?,?,?)", layers)
        for key, rows in features.items():
            conn.executemany("INSERT INTO geo_features VALUES (?,?,?,?,?,?)",
                             [(key, i, nm, gt, gj, pj)
                              for i, (nm, gt, gj, pj) in enumerate(rows)])
        if terrain:
            conn.execute("DELETE FROM geo_rasters")
            conn.executemany("INSERT INTO geo_rasters VALUES (?,?,?,?,?,?,?,?,?)", rasters)
        conn.commit()
    finally:
        conn.close()
    return layers, rasters


def main(argv):
    fresh = "--fresh" in argv
    terrain = "--no-terrain" not in argv
    if not os.path.isfile(DB_PATH):
        sys.stderr.write("ERROR: %s 不存在，请先运行 build_db.py\n" % DB_PATH)
        return 1
    layers, rasters = build(fresh, terrain)
    print("\nImported into %s:" % DB_PATH)
    for layer, title, _s, lic, n in layers:
        print("  %-10s %-14s features=%d  (%s)" % (layer, title, n, lic))
    for name, mime, W, H, *_ in rasters:
        print("  raster %-8s %s %dx%d" % (name, mime, W, H))
    print("db size: %.1f KB" % (os.path.getsize(DB_PATH) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
