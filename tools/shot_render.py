"""Render a still or a bounded sequence from a JSON shot spec.

Run:
  blender.exe -b -P tools/shot_render.py -- shots/<name>.json
  blender.exe -b -P tools/shot_render.py -- shots/<name>.json --check

Spec fields: output, resolution, samples, camera, camera_location, lens,
f_stop, exposure, marker, terminal, light, world_strength, screen, card,
contactless, network.

Animation is opt-in via `"animation": {"duration_s": 3.0, "fps": 24}` plus a
`channels` block. Channels are piecewise keys with smoothstep easing:
  camera_location [[t,[x,y,z]],...]   marker [[t,[x,y,z]],...]
  terminal_rot_z [[t,deg],...]        card_pos [[t,[x,y,z]],...]
  packet_pos [[t,[x,y,z]],...]
`screen_events` changes the display text at times: [{"t":1.4,"status":"APPROVED"}].

Renders are content-addressed over spec, template, master, this file and the
Blender version. A still is cached as <key>.png; a sequence as <key>/frames.
Editing one shot therefore misses only that shot's key. `--check` samples five
times through the shot and fails when the terminal, card or packet leaves the
camera frame or the card penetrates the terminal body.
"""

import hashlib
import json
import os
import shutil
import sys
import time

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "templates", "cf_studio_v1.blend")
MASTER = os.path.join(ROOT, "assets", "models", "terminal_master.blend")
ASSET_COLL = "ASSET_Terminal"
CACHE = os.path.join(ROOT, "render", "cache")
SEQUENCES = os.path.join(ROOT, "render", "sequences")

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


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    check = "--check" in argv
    still = None
    if "--still" in argv:
        still = float(argv[argv.index("--still") + 1])
    rest = [a for a in argv if not a.startswith("--")]
    if still is not None:
        rest = [a for a in rest if a != str(still)]
    if not rest:
        raise SystemExit("usage: blender -b -P tools/shot_render.py -- <shot.json> [--check|--still <s>]")
    return os.path.abspath(rest[0]), check, still


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def lerp(a, b, u):
    if isinstance(a, (list, tuple)):
        return [x + (y - x) * u for x, y in zip(a, b)]
    return a + (b - a) * u


def channel(spec, name, t, default=None):
    ch = spec.get("channels", {}).get(name)
    if not ch or not ch.get("keys"):
        return default
    keys = ch["keys"]
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            u = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
            if ch.get("ease", "smooth") == "smooth":
                u = u * u * (3 - 2 * u)
            return lerp(v0, v1, u)
    return keys[-1][1]


def emissive(name, rgb, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    bsdf.inputs["Emission Color"].default_value = tuple(rgb) + (1.0,)
    bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def to_props(ob):
    props = bpy.data.collections.get("PROPS")
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    props.objects.link(ob)


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


def base_card_pos(spec):
    contact = spec.get("contactless", {})
    if contact.get("enabled"):
        return (0, contact.get("y", 0.030), 0.0645 + contact.get("height", 0.03))
    return (0, -0.109 - 0.045 + 0.09 * spec.get("card", {}).get("insert", 0), 0.022)


def add_card(spec, inst):
    t = spec.get("card", {})
    contact = spec.get("contactless", {})
    if not t.get("enabled") and not (contact.get("enabled") and contact.get("card", True)):
        return None
    bpy.ops.mesh.primitive_cube_add(size=1, location=base_card_pos(spec))
    card = bpy.context.object
    card.name = "PROP_Card"
    s = contact.get("scale", 1.0)
    card.scale = (0.037 * s, 0.027 * s, 0.00038)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    centre = sum((Vector(c) for c in card.bound_box), Vector()) / 8.0
    if centre.length > 1e-5:
        raise SystemExit(f"FAIL: card mesh not local-centred after apply ({tuple(round(v, 4) for v in centre)})")
    bev = card.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.0025
    bev.segments = 3
    mat = bpy.data.materials.new("CardPlastic")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.55, 0.56, 0.58, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.35
    card.data.materials.append(mat)
    to_props(card)
    card.parent = inst
    card.rotation_euler[0] = contact.get("tilt_x_deg", 0.0) * 3.14159265 / 180.0
    card.rotation_euler[2] = contact.get("rot_z_deg", 0.0) * 3.14159265 / 180.0
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    chip = bpy.context.object
    chip.name = "PROP_CardChip"
    chip.scale = (0.012, 0.009, 0.0006)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    chip.location = (-0.014, 0.002, 0.0006)
    gold = bpy.data.materials.new("CardChipGold")
    gold.use_nodes = True
    gb = gold.node_tree.nodes["Principled BSDF"]
    gb.inputs["Base Color"].default_value = (0.85, 0.65, 0.25, 1.0)
    gb.inputs["Metallic"].default_value = 1.0
    gb.inputs["Roughness"].default_value = 0.30
    chip.data.materials.append(gold)
    to_props(chip)
    chip.parent = card
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
    ring.data.materials.append(emissive("FieldEmit", (0.25, 0.85, 1.0), 6.0))
    to_props(ring)
    ring.parent = inst


def add_screen(spec, inst):
    s = spec.get("screen")
    if not s:
        return None, None, None
    mat = emissive("ScreenEmit", s.get("color", (0.75, 1.0, 0.85)), s.get("strength", 3.0))
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
        return ob

    amount = line("SCREEN_Amount", s.get("amount", "12.40"), 0.010, 0.045)
    status = line("SCREEN_Status", s.get("status", "APPROVED"), 0.004, 0.036)
    return amount, status, mat


def add_network(spec, inst, cam):
    net = spec.get("network")
    if not net:
        return None
    nodes = net.get("nodes", [])
    radius = net.get("node_radius", 0.010)
    objs = []
    for i, node in enumerate(nodes):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=node["pos"])
        sphere = bpy.context.object
        sphere.name = f"NET_Node_{i}"
        sphere.data.materials.append(emissive(f"NodeEmit_{i}", node.get("color", (0.3, 0.8, 1.0)), 2.5))
        to_props(sphere)
        sphere.parent = inst
        objs.append(sphere)
        bpy.ops.object.text_add(location=(node["pos"][0], node["pos"][1], node["pos"][2] + radius * 1.9))
        label = bpy.context.object
        label.name = f"NET_Label_{i}"
        label.data.body = node["label"]
        label.data.size = net.get("label_size", 0.012)
        label.data.align_x = "CENTER"
        label.data.materials.append(emissive(f"LabelEmit_{i}", (0.85, 0.95, 1.0), 2.0))
        to_props(label)
        label.parent = inst
        track = label.constraints.new("TRACK_TO")
        track.target = cam
        track.track_axis = "TRACK_Z"
        track.up_axis = "UP_Y"
    for a, b in net.get("edges", []):
        start, end = Vector(nodes[a]["pos"]), Vector(nodes[b]["pos"])
        mid, span = (start + end) / 2, end - start
        bpy.ops.mesh.primitive_cylinder_add(radius=net.get("edge_radius", 0.0006), depth=span.length, location=mid)
        edge = bpy.context.object
        edge.name = "NET_Edge"
        edge.rotation_euler = Vector((0, 0, 1)).rotation_difference(span).to_euler()
        edge.data.materials.append(emissive("EdgeEmit", (0.20, 0.55, 0.75), 1.2))
        to_props(edge)
        edge.parent = inst
        objs.append(edge)
    packet = None
    if net.get("packet"):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=net["packet"].get("radius", 0.004), location=nodes[0]["pos"])
        packet = bpy.context.object
        packet.name = "NET_Packet"
        packet.data.materials.append(emissive("PacketEmit", net["packet"].get("color", (1.0, 0.9, 0.5)), 8.0))
        to_props(packet)
        packet.parent = inst
    return packet


def apply_time(spec, handles, t):
    inst = handles["inst"]
    term = spec.get("terminal", {})
    inst.location = Vector(channel(spec, "terminal_pos", t, term.get("location", (0, 0, 0))))
    rot = channel(spec, "terminal_rot_z", t, term.get("rotation_z_deg", 0))
    inst.rotation_euler[2] = rot * 3.14159265 / 180.0
    inst.scale = (term.get("scale", 1.0),) * 3

    cam = handles["cam"]
    cam.location = Vector(channel(spec, "camera_location", t, spec.get("camera_location", tuple(cam.location))))
    marker = handles["marker"]
    marker.location = Vector(channel(spec, "marker", t, spec.get("marker", (0, 0, 0.05))))

    card = handles["card"]
    if card:
        card.location = Vector(channel(spec, "card_pos", t, base_card_pos(spec)))

    amount, status, mat = handles["screen"]
    if status:
        event = None
        for ev in spec.get("screen_events", []):
            if ev["t"] <= t:
                event = ev
        if event:
            if "amount" in event:
                amount.data.body = event["amount"]
            if "status" in event:
                status.data.body = event["status"]
            if "color" in event and mat:
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                bsdf.inputs["Emission Color"].default_value = tuple(event["color"]) + (1.0,)

    packet = handles["packet"]
    if packet:
        packet.location = Vector(channel(spec, "packet_pos", t, packet.location))


def build_scene(spec):
    bpy.ops.wm.open_mainfile(filepath=TEMPLATE)
    scene = bpy.context.scene
    coll, inst = load_asset()

    card = add_card(spec, inst)
    add_field_ring(spec, inst)
    amount, status, screen_mat = add_screen(spec, inst)

    cam = bpy.data.objects[spec.get("camera", "CAM_Macro_85")]
    scene.camera = cam
    if spec.get("lens"):
        cam.data.lens = spec["lens"]
    if spec.get("f_stop"):
        cam.data.dof.aperture_fstop = spec["f_stop"]

    marker = bpy.data.objects["SubjectMarker"]
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
    if "counter_roughness" in spec:
        mat = bpy.data.materials.get("CounterPlastic")
        if mat and mat.use_nodes:
            mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = spec["counter_roughness"]

    packet = add_network(spec, inst, cam)
    handles = {"inst": inst, "coll": coll, "cam": cam, "marker": marker, "card": card,
               "screen": (amount, status, screen_mat), "packet": packet}
    apply_time(spec, handles, 0.0)
    return scene, handles


def terminal_points(handles):
    """World-space bbox corners of every mesh in the linked collection."""
    inst = handles["inst"]
    points = []
    for obj in handles["coll"].objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            points.append(inst.matrix_world @ obj.matrix_world @ Vector(corner))
    return points


def bbox_world(obj):
    if obj.type == "MESH":
        corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    else:
        corners = [obj.matrix_world.translation]
    return corners


def run_check(spec, scene, handles, duration):
    cam = handles["cam"]
    failures = []
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        t = duration * frac
        apply_time(spec, handles, t)
        bpy.context.view_layer.update()
        points = [("terminal", p) for p in terminal_points(handles)]
        if handles["card"]:
            points += [("card", p) for p in bbox_world(handles["card"])]
        if handles["packet"]:
            points += [("packet", p) for p in bbox_world(handles["packet"])]
        for label, p in points:
            co = world_to_camera_view(scene, cam, p)
            if not (0.0 <= co.x <= 1.0 and 0.0 <= co.y <= 1.0 and co.z > 0):
                failures.append(f"t={t:.2f} {label} out of frame at {tuple(round(v, 3) for v in p)}")
        card = handles["card"]
        if card:
            local = handles["inst"].matrix_world.inverted() @ card.matrix_world.translation
            inside_body = (-0.05 < local.x < 0.05 and -0.107 < local.y < 0.103 and 0.0 < local.z < 0.058)
            hovering = local.z > 0.058
            entering = local.y < -0.095 and 0.015 < local.z < 0.030
            if inside_body and not (hovering or entering):
                failures.append(f"t={t:.2f} card penetrates body at {tuple(round(v, 3) for v in local)}")
        print(f"CHECK t={t:.2f} frame_points={len(points)}")
    for f in failures:
        print("CHECK FAIL " + f)
    print(f"CHECK VERDICT {'FAIL' if failures else 'PASS'}")
    return not failures


def cache_key(spec):
    key_src = {k: v for k, v in spec.items() if k != "output"}
    return hashlib.sha256(
        json.dumps(key_src, sort_keys=True).encode()
        + sha256_file(TEMPLATE).encode()
        + sha256_file(MASTER).encode()
        + sha256_file(os.path.abspath(__file__)).encode()
        + bpy.app.version_string.encode()
    ).hexdigest()[:16]


def main():
    spec_path_abs, check, still_t = parse_args()
    spec = json.load(open(spec_path_abs, encoding="utf-8"))
    key = cache_key(spec)
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(SEQUENCES, exist_ok=True)
    anim = spec.get("animation")
    duration = anim["duration_s"] if anim else 0.0
    fps = anim.get("fps", 24) if anim else 24
    frame_count = int(round(duration * fps)) if anim else 0

    scene, handles = build_scene(spec)
    if check:
        ok = run_check(spec, scene, handles, duration or 1.0)
        sys.exit(0 if ok else 1)

    w, h = spec.get("resolution", [1080, 1920])
    samples = spec.get("samples", 32)
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.eevee.taa_render_samples = samples
    started = time.time()

    if still_t is not None:
        out = os.path.join(ROOT, "render", "stills", "preview_" + os.path.splitext(os.path.basename(spec_path_abs))[0] + ".png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        apply_time(spec, handles, still_t)
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print(f"STILL {key} t={still_t} {out}")
        return

    if not anim:
        out = os.path.join(ROOT, spec["output"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cached = os.path.join(CACHE, key + ".png")
        if os.path.isfile(cached):
            shutil.copyfile(cached, out)
            print(f"CACHE HIT {key} {out}")
            return
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        shutil.copyfile(out, cached)
        seconds = round(time.time() - started, 2)
        sidecar = {"spec": os.path.relpath(spec_path_abs, ROOT), "cache_key": key,
                   "seconds": seconds, "resolution": [w, h], "samples": samples,
                   "camera": handles["cam"].name, "lens": handles["cam"].data.lens,
                   "f_stop": handles["cam"].data.dof.aperture_fstop,
                   "template_sha256": sha256_file(TEMPLATE), "asset": "receipt-pos-terminal-cc0"}
        json.dump(sidecar, open(os.path.splitext(out)[0] + ".json", "w", encoding="utf-8"), indent=2)
        print(f"RENDER {key} {seconds}s {out}")
        return

    frames_dir = os.path.join(CACHE, key, "frames")
    meta_path = os.path.join(CACHE, key, "meta.json")
    pointer = os.path.join(ROOT, spec["output"])
    if os.path.isfile(meta_path):
        meta = json.load(open(meta_path))
        if meta.get("frames") == frame_count:
            os.makedirs(os.path.dirname(pointer), exist_ok=True)
            json.dump({"frames_dir": os.path.relpath(frames_dir, ROOT), "frames": frame_count,
                       "fps": fps, "duration_s": duration, "cache_key": key},
                      open(pointer, "w", encoding="utf-8"), indent=2)
            print(f"CACHE HIT {key} {frame_count} frames {frames_dir}")
            return

    os.makedirs(frames_dir, exist_ok=True)
    for i in range(frame_count):
        t = i / fps
        apply_time(spec, handles, t)
        scene.render.filepath = os.path.join(frames_dir, f"f{i:04d}.png")
        bpy.ops.render.render(write_still=True)
    seconds = round(time.time() - started, 2)
    meta = {"spec": os.path.relpath(spec_path_abs, ROOT), "cache_key": key, "frames": frame_count,
            "fps": fps, "duration_s": duration, "seconds": seconds, "resolution": [w, h],
            "samples": samples, "template_sha256": sha256_file(TEMPLATE)}
    json.dump(meta, open(meta_path, "w", encoding="utf-8"), indent=2)
    os.makedirs(os.path.dirname(pointer), exist_ok=True)
    json.dump({"frames_dir": os.path.relpath(frames_dir, ROOT), "frames": frame_count,
               "fps": fps, "duration_s": duration, "cache_key": key},
              open(pointer, "w", encoding="utf-8"), indent=2)
    print(f"SEQUENCE {key} {frame_count}f {seconds}s {frames_dir}")


main()
