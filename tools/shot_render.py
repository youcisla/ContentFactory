"""Render one still from a JSON shot spec against the studio template.

Run:
  blender.exe -b -P tools/shot_render.py -- shots/<name>.json

The spec is the only input. Shot fields: output, resolution, samples, camera,
camera_location, lens, f_stop, exposure, marker, terminal, light,
world_strength, screen, card, contactless.
Renders are content-addressed: the key is a hash of the spec (minus `output`)
plus the template hash plus the Blender version, so an unchanged shot is served
from render/cache/ and a changed one misses. A .json sidecar records the key,
settings and render seconds beside every output.
"""

import hashlib
import json
import os
import shutil
import sys
import time

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "templates", "cf_studio_v1.blend")
MASTER = os.path.join(ROOT, "assets", "models", "terminal_master.blend")
ASSET_COLL = "ASSET_Terminal"
CACHE = os.path.join(ROOT, "render", "cache")

LIGHT_PRESETS = {
    "premium_realistic": {
        "key": (1.0, 0.94, 0.86, 2.2, 0.35),
        "fill": (0.82, 0.90, 1.0, 0.55, 0.60),
        "rim": (0.85, 0.92, 1.0, 7.0, 0.25),
        "world": 0.30,
    },
    "premium_stylized": {
        "key": (1.0, 0.98, 0.94, 6.0, 0.10),
        "fill": (0.16, 0.34, 0.75, 0.9, 0.30),
        "rim": (0.15, 0.95, 0.85, 22.0, 0.08),
        "world": 0.06,
    },
}


def spec_path():
    argv = sys.argv
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        if rest:
            return os.path.abspath(rest[0])
    raise SystemExit("usage: blender -b -P tools/shot_render.py -- <shot.json>")


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_asset():
    with bpy.data.libraries.load(MASTER, link=True) as (src, dst):
        dst.collections = [ASSET_COLL]
    coll = dst.collections[0]
    inst = bpy.data.objects.new("PROP_Terminal", None)
    inst.instance_type = "COLLECTION"
    inst.instance_collection = coll
    props = bpy.data.collections.get("PROPS") or bpy.context.scene.collection
    props.objects.link(inst)
    return coll, inst


def add_card(spec, inst):
    t = spec.get("card", {})
    contact = spec.get("contactless", {})
    if not t.get("enabled") and not (contact.get("enabled") and contact.get("card", True)):
        return None
    if contact.get("enabled"):
        loc = (0, contact.get("y", 0.030), 0.0645 + contact.get("height", 0.03))
    else:
        # 74 mm wide so it enters the 74 mm slot; 0.76 mm thick.
        loc = (0, -0.109 - 0.045 + 0.09 * t.get("insert", 0), 0.022)
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    card = bpy.context.object
    card.name = "PROP_Card"
    s = contact.get("scale", 1.0)
    card.scale = (0.037 * s, 0.027 * s, 0.00038)
    bpy.ops.object.transform_apply(scale=True)
    bev = card.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.0025
    bev.segments = 3
    mat = bpy.data.materials.new("CardPlastic")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.045, 0.10, 0.28, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.30
    card.data.materials.append(mat)
    props = bpy.data.collections.get("PROPS")
    for c in list(card.users_collection):
        c.objects.unlink(card)
    props.objects.link(card)
    card.parent = inst
    card.rotation_euler[0] = contact.get("tilt_x_deg", 0.0) * 3.14159265 / 180.0
    card.rotation_euler[2] = contact.get("rot_z_deg", 0.0) * 3.14159265 / 180.0
    return card


def add_field_ring(spec, inst):
    contact = spec.get("contactless", {})
    if not contact.get("enabled") or not contact.get("ring", True):
        return
    bpy.ops.mesh.primitive_torus_add(
        major_radius=contact.get("ring_radius", 0.022),
        minor_radius=0.0012,
        location=(0, contact.get("y", 0.030), contact.get("ring_z", 0.072)),
    )
    ring = bpy.context.object
    ring.name = "FX_FieldRing"
    mat = bpy.data.materials.new("FieldEmit")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    bsdf.inputs["Emission Color"].default_value = (0.25, 0.85, 1.0, 1.0)
    bsdf.inputs["Emission Strength"].default_value = 6.0
    ring.data.materials.append(mat)
    props = bpy.data.collections.get("PROPS")
    for c in list(ring.users_collection):
        c.objects.unlink(ring)
    props.objects.link(ring)
    ring.parent = inst


def add_screen(spec, inst):
    s = spec.get("screen")
    if not s:
        return
    mat = bpy.data.materials.new("ScreenEmit")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    colour = tuple(s.get("color", (0.75, 1.0, 0.85))) + (1.0,)
    bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    bsdf.inputs["Emission Color"].default_value = colour
    bsdf.inputs["Emission Strength"].default_value = s.get("strength", 3.0)
    props = bpy.data.collections.get("PROPS")

    def line(name, body, size, y):
        bpy.ops.object.text_add(location=(0.0, y, 0.0652))
        ob = bpy.context.object
        ob.name = name
        ob.data.body = body
        ob.data.size = size
        ob.data.align_x = "CENTER"
        ob.data.align_y = "CENTER"
        ob.data.materials.append(mat)
        for c in list(ob.users_collection):
            c.objects.unlink(ob)
        props.objects.link(ob)
        ob.parent = inst

    line("SCREEN_Amount", s.get("amount", "12.40"), 0.010, 0.045)
    line("SCREEN_Status", s.get("status", "APPROVED"), 0.004, 0.036)


def main():
    spec_path_abs = spec_path()
    spec = json.load(open(spec_path_abs, encoding="utf-8"))
    key_src = {k: v for k, v in spec.items() if k != "output"}
    key = hashlib.sha256(
        json.dumps(key_src, sort_keys=True).encode()
        + sha256_file(TEMPLATE).encode()
        + sha256_file(MASTER).encode()
        + sha256_file(os.path.abspath(__file__)).encode()
        + bpy.app.version_string.encode()
    ).hexdigest()[:16]
    out = os.path.join(ROOT, spec["output"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    cached = os.path.join(CACHE, key + ".png")

    started = time.time()
    if os.path.isfile(cached):
        shutil.copyfile(cached, out)
        print(f"CACHE HIT {key} {out}")
        return

    bpy.ops.wm.open_mainfile(filepath=TEMPLATE)
    scene = bpy.context.scene

    coll, inst = load_asset()
    term = spec.get("terminal", {})
    inst.location = Vector(term.get("location", (0, 0, 0)))
    inst.rotation_euler[2] = term.get("rotation_z_deg", 0) * 3.14159265 / 180.0
    inst.scale = (term.get("scale", 1.0),) * 3

    add_card(spec, inst)
    add_field_ring(spec, inst)
    add_screen(spec, inst)

    cam = bpy.data.objects[spec.get("camera", "CAM_Macro_85")]
    scene.camera = cam
    if spec.get("camera_location"):
        cam.location = Vector(spec["camera_location"])
    if spec.get("lens"):
        cam.data.lens = spec["lens"]
    if spec.get("f_stop"):
        cam.data.dof.aperture_fstop = spec["f_stop"]

    marker = bpy.data.objects["SubjectMarker"]
    marker.location = Vector(spec.get("marker", (0, 0, 0.05)))

    preset = LIGHT_PRESETS[spec.get("light", "premium_realistic")]
    for name, (r, g, b, power, size) in ((k, preset[k]) for k in ("key", "fill", "rim")):
        light = bpy.data.objects[name.capitalize()]
        light.data.color = (r, g, b)
        light.data.energy = power
        light.data.size = size
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = spec.get(
        "world_strength", preset["world"]
    )
    scene.view_settings.exposure = spec.get("exposure", 0.0)

    w, h = spec.get("resolution", [1080, 1920])
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    scene.eevee.taa_render_samples = spec.get("samples", 32)
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    seconds = round(time.time() - started, 2)

    shutil.copyfile(out, cached)
    sidecar = {
        "spec": os.path.relpath(spec_path_abs, ROOT),
        "cache_key": key,
        "seconds": seconds,
        "resolution": [w, h],
        "samples": scene.eevee.taa_render_samples,
        "camera": cam.name,
        "lens": cam.data.lens,
        "f_stop": cam.data.dof.aperture_fstop,
        "template_sha256": sha256_file(TEMPLATE),
        "asset": "receipt-pos-terminal-cc0",
    }
    json.dump(sidecar, open(os.path.splitext(out)[0] + ".json", "w", encoding="utf-8"), indent=2)
    print(f"RENDER {key} {seconds}s {out}")


main()
