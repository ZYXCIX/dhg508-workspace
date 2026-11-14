"""
Build a low-poly 3D scene of Confucius and Laozi in the Zhou archive.
Run with Blender (headless):

  blender.exe --background --factory-startup --python build_scene.py

Outputs:
  code/assets/confucius_laozi_3d.glb
  code/blender/confucius_laozi_3d.blend
  artifacts/blender_preview.png
"""

import bpy
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(PROJECT, "code", "assets")
ARTIFACTS = os.path.join(PROJECT, "artifacts")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(ARTIFACTS, exist_ok=True)

# ----------------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------------

def srgb(hex_value):
    hex_value = hex_value.lstrip("#")
    rgb = tuple(int(hex_value[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    def lin(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return tuple(lin(v) for v in rgb)


def material(name, hex_value, roughness=0.85, metallic=0.0, emission=None, emission_strength=2.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    color = srgb(hex_value)
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        try:
            bsdf.inputs["Emission Color"].default_value = (*srgb(emission), 1.0)
            bsdf.inputs["Emission Strength"].default_value = emission_strength
        except KeyError:
            pass
    mat.diffuse_color = (*color, 1.0)
    return mat


def box(name, dims, loc, mat, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.rotation_euler = rot
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def cylinder(name, radius, depth, loc, mat, parent=None, vertices=12, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = rot
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def cone(name, r1, r2, depth, loc, mat, parent=None, vertices=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = rot
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def empty(name, loc=(0, 0, 0)):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=loc)
    obj = bpy.context.object
    obj.name = name
    return obj


def key(obj, path, frame, value):
    setattr(obj, path, value)
    obj.keyframe_insert(data_path=path, frame=frame)


# ----------------------------------------------------------------------------
# Clear
# ----------------------------------------------------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.meshes):
    if block.users == 0:
        bpy.data.meshes.remove(block)

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------
M = {
    "floor": material("floor", "#5a4632", 0.95),
    "floor2": material("floor2", "#634e38", 0.95),
    "wall": material("wall", "#4a3a2c", 0.95),
    "wall2": material("wall2", "#52402f", 0.95),
    "wood": material("wood", "#6b4a2f", 0.8),
    "wood_dark": material("wood_dark", "#3d2a1c", 0.85),
    "wood_light": material("wood_light", "#8a6440", 0.8),
    "bamboo": material("bamboo", "#b09355", 0.8),
    "bamboo_light": material("bamboo_light", "#c2a566", 0.8),
    "mat": material("mat", "#8a7448", 0.95),
    "mat2": material("mat2", "#7a653d", 0.95),
    "bronze": material("bronze", "#7a6a3a", 0.45, 0.7),
    "lamp": material("lamp", "#9a8a4a", 0.4, 0.7),
    "flame": material("flame", "#ffb347", 0.2, 0.0, emission="#ff8a2a", emission_strength=6.0),
    "skin": material("skin", "#d9a066", 0.58),
    "skin_dark": material("skin_dark", "#b07a4a", 0.65),
    "eye_white": material("eye_white", "#f0e8d8", 0.22),
    "iris": material("iris", "#3a2a1a", 0.18),
    "lip": material("lip", "#a85a4a", 0.68),
    "lip2": material("lip2", "#8f443a", 0.68),
    "black": material("black", "#1c1a18", 0.9),
    "white": material("white", "#e8e0cc", 0.9),
    "grey": material("grey", "#cfc6b0", 0.9),
    "kong": material("kong", "#33475c", 0.9),
    "kong_dark": material("kong_dark", "#2a3a4c", 0.9),
    "kong_light": material("kong_light", "#3e5570", 0.9),
    "red": material("red", "#8f3b2e", 0.85),
    "red_light": material("red_light", "#b04a38", 0.85),
    "gold": material("gold", "#c9a227", 0.4, 0.5),
    "jade": material("jade", "#6f9a6a", 0.35, 0.2),
    "lao": material("lao", "#6b543a", 0.9),
    "lao_dark": material("lao_dark", "#3a2f26", 0.9),
    "lao_light": material("lao_light", "#7d6344", 0.9),
    "window": material("window", "#d8b46a", 0.3, 0.0, emission="#d8b46a", emission_strength=2.0),
    "dust": material("dust", "#ffe2a0", 0.3, 0.0, emission="#ffcf7a", emission_strength=1.5),
}

# Subtle skin scattering for a less plastic look.
try:
    skin_bsdf = M["skin"].node_tree.nodes.get("Principled BSDF")
    skin_bsdf.inputs["Subsurface Weight"].default_value = 0.12
    skin_bsdf.inputs["Subsurface Radius"].default_value = (0.10, 0.05, 0.03)
    skin_bsdf.inputs["Subsurface Scale"].default_value = 0.05
except Exception:
    pass

# ----------------------------------------------------------------------------
# Room
# ----------------------------------------------------------------------------
# floor tiles
for ix in range(-4, 4):
    for iy in range(-3, 3):
        m = M["floor"] if (ix + iy) % 2 == 0 else M["floor2"]
        box("floor_%d_%d" % (ix, iy), (1.0, 1.0, 0.10),
            (ix + 0.5, iy + 0.5, -0.05), m)

# back and side walls
box("wall_back", (8.4, 0.24, 3.6), (0, 3.1, 1.8), M["wall"])
box("wall_left", (0.24, 6.4, 3.6), (-4.1, 0, 1.8), M["wall2"])
box("wall_right", (0.24, 6.4, 3.6), (4.1, 0, 1.8), M["wall2"])

# ceiling beams
for y in (-2.4, 0, 2.4):
    box("beam_%s" % y, (8.2, 0.28, 0.28), (0, y, 3.45), M["wood_dark"])
box("beam_front", (8.2, 0.2, 0.2), (0, -2.95, 3.45), M["wood_dark"])

# pillars
for x in (-3.7, 3.7):
    for y in (-2.5, 2.5):
        cylinder("pillar_%s_%s" % (x, y), 0.14, 3.6, (x, y, 1.8), M["wood"], vertices=10)

# window
box("window_frame", (1.9, 0.12, 1.3), (0, 2.94, 2.35), M["wood_dark"])
box("window_glow", (1.7, 0.04, 1.1), (0, 2.86, 2.35), M["window"])
for i in range(4):
    box("window_v_%d" % i, (0.05, 0.05, 1.1), (-0.6 + i * 0.4, 2.82, 2.35), M["wood"])
for j in range(3):
    box("window_h_%d" % j, (1.7, 0.05, 0.05), (0, 2.82, 1.95 + j * 0.4), M["wood"])

# shelves + bamboo bundles
for sx in (-2.3, 2.3):
    box("shelf_side_l_%s" % sx, (0.06, 0.38, 2.1), (sx - 0.85, 2.65, 1.05), M["wood"])
    box("shelf_side_r_%s" % sx, (0.06, 0.38, 2.1), (sx + 0.85, 2.65, 1.05), M["wood"])
    for k, z in enumerate((0.25, 0.72, 1.19, 1.66, 2.05)):
        box("shelf_board_%s_%d" % (sx, k), (1.76, 0.38, 0.05), (sx, 2.65, z), M["wood_light"])
        for i in range(6):
            bx = sx - 0.72 + i * 0.24
            box("bundle_%s_%d_%d" % (sx, k, i), (0.14, 0.24, 0.34),
                (bx, 2.62, z + 0.2), M["bamboo"] if i % 2 == 0 else M["bamboo_light"])
            box("bundle_band_%s_%d_%d" % (sx, k, i), (0.15, 0.25, 0.025),
                (bx, 2.62, z + 0.12), M["wood_dark"])
            box("bundle_band2_%s_%d_%d" % (sx, k, i), (0.15, 0.25, 0.025),
                (bx, 2.62, z + 0.28), M["wood_dark"])

# mats
for x in (-1.25, 1.25):
    box("mat_%s" % x, (1.5, 1.1, 0.05), (x, 0.35, 0.025), M["mat"])
    for i in range(5):
        box("mat_line_%s_%d" % (x, i), (1.5, 0.02, 0.012),
            (x, 0.35 - 0.44 + i * 0.22, 0.055), M["mat2"])

# low table
box("table_top", (1.15, 0.6, 0.09), (0, 0.35, 0.44), M["wood_light"])
for dx in (-0.48, 0.48):
    for dy in (-0.22, 0.22):
        box("table_leg_%s_%s" % (dx, dy), (0.07, 0.07, 0.36),
            (dx, 0.35 + dy, 0.2), M["wood_dark"])

# bamboo slips on table
for i in range(4):
    box("slip_%d" % i, (0.04, 0.3, 0.015), (-0.28 + i * 0.06, 0.35, 0.49), M["bamboo_light"])

# lamp
cylinder("lamp_base", 0.13, 0.04, (0.32, 0.35, 0.49), M["bronze"], vertices=12)
cylinder("lamp_stem", 0.035, 0.24, (0.32, 0.35, 0.62), M["lamp"], vertices=10)
cylinder("lamp_bowl", 0.15, 0.06, (0.32, 0.35, 0.76), M["bronze"], vertices=12)
flame = cone("flame", 0.05, 0.0, 0.16, (0.32, 0.35, 0.88), M["flame"], vertices=8)
flame.rotation_euler = (0, 0, 0.2)

# floor slip stack
for i in range(4):
    box("floor_slip_%d" % i, (0.55, 0.25, 0.08),
        (-3.25, 0.75, 0.04 + i * 0.09), M["bamboo"] if i % 2 == 0 else M["bamboo_light"])

# bronze ding
cylinder("ding_body", 0.22, 0.24, (-3.25, -0.9, 0.2), M["bronze"], vertices=10)
for dx in (-0.13, 0.13):
    box("ding_leg_%s" % dx, (0.05, 0.05, 0.16), (-3.25 + dx, -0.9, 0.08), M["bronze"])

# ----------------------------------------------------------------------------
# Characters
# ----------------------------------------------------------------------------

def sphere(name, radius, loc, mat, parent=None, segments=16, rings=10, scale=(1, 1, 1), smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if smooth:
        bpy.ops.object.shade_smooth()
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def cylinder_between(name, p1, p2, radius, mat, parent=None, vertices=8, smooth=False):
    a = Vector(p1)
    b = Vector(p2)
    vec = b - a
    length = vec.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(a + b) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = vec.to_track_quat("Z", "Y")
    if smooth:
        bpy.ops.object.shade_smooth()
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def cone_between(name, p1, p2, r1, r2, mat, parent=None, vertices=10, smooth=False):
    a = Vector(p1)
    b = Vector(p2)
    vec = b - a
    length = vec.length
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=length, location=(a + b) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = vec.to_track_quat("Z", "Y")
    if smooth:
        bpy.ops.object.shade_smooth()
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def torus(name, major, minor, loc, mat, parent=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=16, minor_segments=6, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def build_character(name, robe, robe_dark, robe_light, trim, cap_mat, beard_mat, is_kong):
    root = empty(name + "_root", (0, 0, 0))

    # lower robe / seated lap: a flared, elliptical frustum
    lap = cone(name + "_lap_robe", 0.54, 0.34, 0.34, (0, 0, 0.17), robe_dark, root, vertices=12)
    lap.scale = (1.0, 0.78, 1.0)
    bpy.context.view_layer.objects.active = lap
    lap.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    lap.select_set(False)

    lap_top = sphere(name + "_lap_top", 0.36, (0, 0, 0.30), robe,
                     parent=root, segments=16, rings=8, scale=(1.0, 0.78, 0.38))
    box(name + "_lap_fold", (0.07, 0.5, 0.02), (0, -0.05, 0.35), robe_light, root)
    for i in range(6):
        a = i * math.pi / 3
        cylinder_between(name + "_fold_%d" % i,
                         (0.31 * math.cos(a), 0.24 * math.sin(a), 0.34),
                         (0.52 * math.cos(a), 0.40 * math.sin(a), 0.06),
                         0.008, robe_dark, root, vertices=6)

    # torso: shoulder-to-waist frustum
    torso = cone(name + "_torso", 0.28, 0.36, 0.44, (0, 0, 0.57), robe, root, vertices=12)
    torso.scale = (1.0, 0.72, 1.0)
    bpy.context.view_layer.objects.active = torso
    torso.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    torso.select_set(False)

    # chest / shoulder mass
    sphere(name + "_chest", 0.30, (0, 0, 0.75), robe, parent=root,
           segments=16, rings=8, scale=(1.0, 0.72, 0.55))

    # sash: a belt ring, not a box
    torus(name + "_sash", 0.28, 0.035, (0, 0, 0.45), trim, root, scale=(1.0, 0.74, 1.0))
    sphere(name + "_sash_knot", 0.055, (0, -0.27, 0.45), M["gold"], parent=root,
           segments=10, rings=6, scale=(1.0, 0.7, 1.0))
    box(name + "_sash_end1", (0.045, 0.025, 0.20), (-0.035, -0.27, 0.33), trim, root, rot=(0.06, 0, 0))
    box(name + "_sash_end2", (0.045, 0.025, 0.26), (0.04, -0.27, 0.30), trim, root, rot=(-0.04, 0, 0))
    sphere(name + "_jade", 0.04, (0.235, -0.18, 0.41), M["jade"], parent=root,
           segments=10, rings=6, scale=(0.8, 0.45, 1.1))

    # 蔽膝
    box(name + "_bixi", (0.20, 0.025, 0.30), (0, -0.30, 0.30), trim, root)
    box(name + "_bixi_edge", (0.21, 0.015, 0.022), (0, -0.315, 0.44), M["gold"], root)

    # 交领: two angled white bands on the chest
    box(name + "_collar_l", (0.045, 0.018, 0.22), (-0.075, -0.24, 0.68),
        M["white"], root, rot=(0, 0.48, 0))
    box(name + "_collar_r", (0.045, 0.018, 0.22), (0.075, -0.24, 0.68),
        M["white"], root, rot=(0, -0.48, 0))
    box(name + "_collar_trim_l", (0.025, 0.018, 0.23), (-0.105, -0.247, 0.67),
        trim, root, rot=(0, 0.48, 0))
    box(name + "_collar_trim_r", (0.025, 0.018, 0.23), (0.105, -0.247, 0.67),
        trim, root, rot=(0, -0.48, 0))

    # neck
    cylinder(name + "_neck", 0.075, 0.12, (0, 0, 0.82), M["skin"], root, vertices=12)

    # head: low-poly sphere, slightly taller than wide
    head_z = 1.00 if is_kong else 0.97
    head = sphere(name + "_head", 0.155, (0, -0.01, head_z), M["skin"],
                  parent=root, segments=18, rings=12, scale=(1.0, 0.94, 1.12))
    # ears
    for sx in (-1, 1):
        sphere(name + "_ear_" + ("l" if sx < 0 else "r"), 0.038,
               (sx * 0.15, 0.0, head_z), M["skin"], parent=root,
               segments=10, rings=6, scale=(0.55, 0.8, 1.1))
    # hair: a cap sphere pushed back, so the face protrudes
    hair = sphere(name + "_hair", 0.16, (0, 0.035, head_z + 0.055),
                  M["black"] if is_kong else M["grey"], parent=root,
                  segments=18, rings=10, scale=(1.0, 0.95, 0.82))
    box(name + "_hairline", (0.30, 0.02, 0.05), (0, -0.145, head_z + 0.10),
        M["black"] if is_kong else M["grey"], root)

    # jaw / chin / cheeks: break the sphere silhouette
    sphere(name + "_jaw", 0.105, (0, -0.015, head_z - 0.09), M["skin"],
           parent=root, segments=16, rings=10, scale=(0.95, 0.90, 0.75))
    sphere(name + "_chin", 0.050, (0, -0.105, head_z - 0.125), M["skin"],
           parent=root, segments=12, rings=8, scale=(1.0, 0.9, 0.7))
    for sx in (-1, 1):
        sphere(name + "_cheek_" + ("l" if sx < 0 else "r"), 0.040,
               (sx * 0.070, -0.090, head_z - 0.035), M["skin"], parent=root,
               segments=12, rings=8, scale=(1.0, 0.8, 0.8))

    # eyes: sclera + iris, grouped under an empty so they can blink
    for sx in (-1, 1):
        side = "l" if sx < 0 else "r"
        eye_root = empty(name + "_eye_" + side, (sx * 0.052, -0.138, head_z + 0.015))
        eye_root.parent = root
        sphere(name + "_sclera_" + side, 0.019, (0, 0, 0), M["eye_white"],
               parent=eye_root, segments=14, rings=8, scale=(1.0, 0.42, 0.65))
        sphere(name + "_iris_" + side, 0.0125, (0, -0.010, 0), M["iris"],
               parent=eye_root, segments=12, rings=8, scale=(1.0, 0.5, 1.0))
        sphere(name + "_pupil_" + side, 0.006, (0, -0.016, 0), M["black"],
               parent=eye_root, segments=10, rings=6, scale=(1.0, 0.4, 1.0))
        sphere(name + "_upper_lid_" + side, 0.020,
               (sx * 0.052, -0.145, head_z + 0.032), M["skin"], parent=root,
               segments=12, rings=8, scale=(1.1, 0.55, 0.35))
        sphere(name + "_lower_lid_" + side, 0.018,
               (sx * 0.052, -0.145, head_z - 0.002), M["skin"], parent=root,
               segments=12, rings=8, scale=(1.1, 0.55, 0.30))
        box(name + "_brow_" + side, (0.048, 0.012, 0.014),
            (sx * 0.055, -0.155, head_z + 0.058),
            M["black"] if is_kong else M["lao_dark"], root, rot=(0, 0, sx * -0.08))

    # nose: bridge + tip + nostrils
    cylinder_between(name + "_nose_bridge", (0, -0.135, head_z + 0.035),
                     (0, -0.165, head_z - 0.018), 0.018, M["skin_dark"], root, vertices=8)
    sphere(name + "_nose_tip", 0.022, (0, -0.172, head_z - 0.022), M["skin"],
           parent=root, segments=12, rings=8, scale=(0.9, 1.0, 0.9))
    for sx in (-1, 1):
        sphere(name + "_nostril_" + ("l" if sx < 0 else "r"), 0.006,
               (sx * 0.014, -0.166, head_z - 0.034), M["black"], parent=root,
               segments=8, rings=6, scale=(1.0, 0.6, 0.6))

    # lips and mouth
    box(name + "_lip_upper", (0.070, 0.012, 0.010), (0, -0.158, head_z - 0.062), M["lip"], root)
    box(name + "_lip_lower", (0.060, 0.014, 0.012), (0, -0.160, head_z - 0.080), M["lip2"], root)
    box(name + "_mouth", (0.050, 0.008, 0.006), (0, -0.165, head_z - 0.071), M["black"], root)

    # moustache strands
    cone_between(name + "_moustache_l", (-0.014, -0.160, head_z - 0.052),
                 (-0.060, -0.155, head_z - 0.095), 0.010, 0.003,
                 M["black"] if is_kong else M["grey"], root, vertices=6)
    cone_between(name + "_moustache_r", (0.014, -0.160, head_z - 0.052),
                 (0.060, -0.155, head_z - 0.095), 0.010, 0.003,
                 M["black"] if is_kong else M["grey"], root, vertices=6)

    # beard: several tapered strands instead of one cone
    if is_kong:
        for i, x in enumerate((-0.050, -0.025, 0.0, 0.025, 0.050)):
            strand_name = name + ("_beard" if i == 2 else "_beard_%d" % i)
            cone(strand_name, 0.004, 0.020, 0.13,
                 (x, -0.135, head_z - 0.165), M["black"], root, vertices=6)
    else:
        for i, x in enumerate((-0.070, -0.045, -0.020, 0.0, 0.020, 0.045, 0.070)):
            strand_name = name + ("_beard" if i == 3 else "_beard_%d" % i)
            cone(strand_name, 0.003, 0.022, 0.30,
                 (x, -0.135, head_z - 0.25), M["grey"], root, vertices=6)
        cone(name + "_beard_tip", 0.003, 0.020, 0.16,
             (0, -0.130, head_z - 0.46), M["white"], root, vertices=6)

    # cap
    if is_kong:
        cap = cylinder(name + "_cap", 0.19, 0.11, (0, 0, head_z + 0.19),
                       M["black"], root, vertices=10)
        cap.scale = (1.0, 0.9, 1.0)
        bpy.context.view_layer.objects.active = cap
        cap.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        cap.select_set(False)
        box(name + "_cap_brim", (0.40, 0.36, 0.03), (0, -0.03, head_z + 0.14), M["black"], root)
        box(name + "_cap_top", (0.30, 0.26, 0.045), (0, 0, head_z + 0.26), M["black"], root)
    else:
        cap = sphere(name + "_cap", 0.17, (0, 0.02, head_z + 0.23), M["lao_dark"],
                     parent=root, segments=16, rings=8, scale=(1.0, 0.9, 0.5))
        box(name + "_cap_flap_l", (0.05, 0.28, 0.12), (-0.19, 0, head_z + 0.08), M["lao_dark"], root)
        box(name + "_cap_flap_r", (0.05, 0.28, 0.12), (0.19, 0, head_z + 0.08), M["lao_dark"], root)
        sphere(name + "_cap_gold", 0.035, (0, -0.165, head_z + 0.19), M["gold"],
               parent=root, segments=10, rings=6, scale=(1.0, 0.7, 1.0))

    # arms: shoulder empties with a bent upper arm + forearm, wide sleeve
    for side, sx in (("l", -1), ("r", 1)):
        sh = empty(name + "_shoulder_" + side, (sx * 0.30, 0, 0.73))
        sh.parent = root
        sphere(name + "_shoulder_ball_" + side, 0.105, (0, 0, 0), robe,
               parent=sh, segments=12, rings=8)
        elbow = (sx * 0.09, -0.11, -0.19)
        wrist = (sx * -0.02, -0.24, -0.29)
        cylinder_between(name + "_upper_" + side, (0, 0, 0), elbow, 0.055, robe_dark, sh, vertices=8)
        sphere(name + "_elbow_" + side, 0.055, elbow, robe_dark, parent=sh, segments=10, rings=6)
        cylinder_between(name + "_fore_" + side, elbow, wrist, 0.045, M["skin"], sh, vertices=8)
        sphere(name + "_palm_" + side, 0.050, wrist, M["skin"], parent=sh,
               segments=12, rings=8, scale=(0.9, 1.0, 0.75))
        for fi in range(4):
            fx = wrist[0] + (fi - 1.5) * 0.012
            cylinder_between(name + "_finger_" + side + "_" + str(fi),
                             (fx, wrist[1] - 0.005, wrist[2] - 0.005),
                             (fx, wrist[1] - 0.055, wrist[2] - 0.045),
                             0.0075, M["skin"], sh, vertices=6)
        cylinder_between(name + "_thumb_" + side,
                         (wrist[0] + sx * 0.02, wrist[1] + 0.01, wrist[2]),
                         (wrist[0] + sx * 0.048, wrist[1] - 0.030, wrist[2] - 0.020),
                         0.010, M["skin"], sh, vertices=6)
        cone_between(name + "_sleeve_" + side, (0, 0, 0.02), wrist,
                     0.12, 0.17, robe_light if sx > 0 else robe_dark, sh, vertices=12)
        cylinder_between(name + "_cuff_" + side, (sx * 0.06, -0.15, -0.24), wrist,
                         0.055, trim, sh, vertices=8)

    # Keep the whole head (face, hair, cap, beard) together when it turns.
    head_tags = ("_head", "_ear_", "_hair", "_jaw", "_chin", "_cheek_", "_eye_",
                 "_lid_", "_brow_", "_nose", "_nostril_", "_mouth", "_lip_",
                 "_moustache_", "_beard", "_cap")
    for obj in list(root.children):
        if obj is head:
            continue
        if any(tag in obj.name for tag in head_tags):
            obj.parent = head
            obj.matrix_parent_inverse = head.matrix_world.inverted()

    return root


kong = build_character("Kong", M["kong"], M["kong_dark"], M["kong_light"],
                       M["red"], M["black"], M["black"], True)
lao = build_character("Lao", M["lao"], M["lao_dark"], M["lao_light"],
                      M["lao_dark"], M["lao_dark"], M["grey"], False)

# place and face each other, angled slightly toward the camera
kong.location = (-1.15, 0.35, 0)
kong.rotation_euler = (0, 0, math.radians(62))
lao.location = (1.15, 0.35, 0)
lao.rotation_euler = (0, 0, math.radians(-62))

# ----------------------------------------------------------------------------
# Dust motes
# ----------------------------------------------------------------------------
dust = []
for i in range(14):
    cone_obj = box("dust_%d" % i, (0.025, 0.025, 0.025),
                   (-0.9 + (i * 0.17) % 1.8, 1.4, 1.2 + (i * 0.13) % 1.4),
                   M["dust"])
    dust.append(cone_obj)

# ----------------------------------------------------------------------------
# Lighting
# ----------------------------------------------------------------------------
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (*srgb("#2a2118"), 1.0)
bg.inputs[1].default_value = 1.0

# warm lamp point
lamp_data = bpy.data.lights.new("LampLight", type="POINT")
lamp_data.energy = 75
lamp_data.color = srgb("#ffb066")
lamp = bpy.data.objects.new("LampLight", lamp_data)
lamp.location = (0.32, 0.35, 0.92)
bpy.context.scene.collection.objects.link(lamp)

# cool window area light (area lights are for preview only)
win_data = bpy.data.lights.new("WindowLight", type="AREA")
win_data.energy = 260
win_data.shape = "RECTANGLE"
win_data.size = 2.0
win_data.size_y = 1.2
win_data.color = srgb("#d8e6ff")
win = bpy.data.objects.new("WindowLight", win_data)
win.location = (0, 2.6, 2.35)
win.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.collection.objects.link(win)

# soft fill
fill_data = bpy.data.lights.new("FillLight", type="AREA")
fill_data.energy = 190
fill_data.size = 4.0
fill_data.color = srgb("#b8c6e0")
fill = bpy.data.objects.new("FillLight", fill_data)
fill.location = (0, -3.0, 2.6)
fill.rotation_euler = (math.radians(70), 0, 0)
bpy.context.scene.collection.objects.link(fill)

# low warm bounce from the front, so the robes read
bounce_data = bpy.data.lights.new("BounceLight", type="AREA")
bounce_data.energy = 90
bounce_data.size = 3.0
bounce_data.color = srgb("#ffd2a0")
bounce = bpy.data.objects.new("BounceLight", bounce_data)
bounce.location = (0, -4.2, 1.4)
bounce.rotation_euler = (math.radians(80), 0, 0)
bpy.context.scene.collection.objects.link(bounce)

# ----------------------------------------------------------------------------
# Animation: 10 s loop at 24 fps
# ----------------------------------------------------------------------------
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 240

def loop_keys(obj, path, values, frames):
    for f, v in zip(frames, values):
        key(obj, path, f, v)

# breathing (root z)
loop_keys(kong, "location", [
    (kong.location.x, kong.location.y, 0.0),
    (kong.location.x, kong.location.y, 0.018),
    (kong.location.x, kong.location.y, 0.0),
    (kong.location.x, kong.location.y, 0.018),
    (kong.location.x, kong.location.y, 0.0),
], [1, 60, 120, 180, 240])
loop_keys(lao, "location", [
    (lao.location.x, lao.location.y, 0.0),
    (lao.location.x, lao.location.y, 0.014),
    (lao.location.x, lao.location.y, 0.0),
    (lao.location.x, lao.location.y, 0.014),
    (lao.location.x, lao.location.y, 0.0),
], [1, 50, 100, 170, 240])

# head nods / turns
for who, root in (("Kong", kong), ("Lao", lao)):
    head = bpy.data.objects[who + "_head"]
    head.rotation_mode = "XYZ"
    loop_keys(head, "rotation_euler", [
        (0, 0, 0), (0.035, 0.02, 0), (0, -0.03, 0.02),
        (0.02, 0.03, -0.02), (0, 0, 0)
    ], [1, 60, 120, 180, 240])

    # beard sway
    beard = bpy.data.objects.get(who + "_beard")
    if beard:
        beard.rotation_mode = "XYZ"
        loop_keys(beard, "rotation_euler", [
            (0, 0, 0), (0.03, 0, 0.01), (0, 0, -0.01), (-0.02, 0, 0), (0, 0, 0)
        ], [1, 50, 120, 180, 240])

    # blink: scale the eye group vertically
    for side in ("l", "r"):
        eye = bpy.data.objects.get(who + "_eye_" + side)
        if eye:
            eye.scale = (1, 1, 1)
            loop_keys(eye, "scale", [
                (1, 1, 1), (1, 1, 1), (1, 1, 0.12), (1, 1, 1),
                (1, 1, 1), (1, 1, 0.12), (1, 1, 1), (1, 1, 1)
            ], [1, 80, 84, 88, 160, 164, 168, 240])

    # lower lip: subtle speaking motion
    lip = bpy.data.objects.get(who + "_lip_lower")
    if lip:
        lip.scale = (1, 1, 1)
        loop_keys(lip, "scale", [
            (1, 1, 1), (1, 1, 1.5), (1, 1, 1), (1, 1, 1.3), (1, 1, 1)
        ], [1, 60, 120, 180, 240])

# arm gestures: rotate the shoulder empties, so the whole arm swings
for who, root in (("Kong", kong), ("Lao", lao)):
    for side, sx in (("l", -1), ("r", 1)):
        shoulder = bpy.data.objects.get(who + "_shoulder_" + side)
        if shoulder:
            shoulder.rotation_mode = "XYZ"
            loop_keys(shoulder, "rotation_euler", [
                (0, 0, 0), (0.035, 0, sx * 0.02),
                (0, 0, 0), (-0.018, 0, sx * 0.01), (0, 0, 0)
            ], [1, 50, 110, 170, 240])

# lamp flicker
flame.rotation_mode = "XYZ"
loop_keys(flame, "scale", [
    (1, 1, 1), (1.15, 1.1, 1.2), (0.9, 0.95, 0.9),
    (1.1, 1.05, 1.15), (1, 1, 1)
], [1, 40, 90, 150, 240])
loop_keys(flame, "rotation_euler", [
    (0, 0, 0.2), (0.05, 0, 0.1), (-0.04, 0, 0.3),
    (0.03, 0, 0.15), (0, 0, 0.2)
], [1, 40, 90, 150, 240])

# dust drift
for i, d in enumerate(dust):
    x0, y0, z0 = d.location
    loop_keys(d, "location", [
        (x0, y0, z0), (x0 + 0.15, y0 - 0.08, z0 + 0.35),
        (x0 - 0.05, y0 + 0.06, z0 + 0.70), (x0 + 0.08, y0, z0 + 1.0),
        (x0, y0, z0)
    ], [1, 60, 120, 180, 240])

# Blender 5.x stores actions in layered slots; default Bezier interpolation
# is already what we want for these slow breathing/gesture curves.

# ----------------------------------------------------------------------------
# Camera + preview render
# ----------------------------------------------------------------------------
cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
cam.location = (0, -6.3, 2.9)
bpy.context.scene.collection.objects.link(cam)

target = empty("CameraTarget", (0, 0.5, 1.05))
con = cam.constraints.new(type="TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"
bpy.context.scene.camera = cam

scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(ARTIFACTS, "blender_preview.png")
scene.render.film_transparent = False
try:
    scene.eevee.taa_render_samples = 32
except Exception:
    pass
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "None"
scene.view_settings.exposure = 0.8

bpy.ops.render.render(write_still=True)
print("PREVIEW_RENDERED", scene.render.filepath)

# ----------------------------------------------------------------------------
# Save + export
# ----------------------------------------------------------------------------
blend_path = os.path.join(HERE, "confucius_laozi_3d.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

glb_path = os.path.join(ASSETS, "confucius_laozi_3d.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format="GLB",
    use_selection=False,
    export_apply=True,
    export_animations=True,
    export_animation_mode="SCENE",
    export_frame_range=True,
    export_force_sampling=True,
    export_lights=False,
    export_cameras=False,
)
print("GLB_EXPORTED", glb_path)
print("BLEND_SAVED", blend_path)
