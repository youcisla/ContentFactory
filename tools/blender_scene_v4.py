"""ContentFactory V4 scene — contactless payment, three beats.

The Rig A baseline (`blender_scene_proof.py`) is preserved unchanged. This is a
different scene built to answer a different question: can the frame TEACH?

Three beats, 24 frames:
  1. the card descends toward the reader
  2. the card's antenna coil energises - it is being powered by the reader's field
  3. the reader confirms, and an authorisation request departs upward

The three floating torus rings from the proof scene are gone. They were
decorative, they could be mistaken for the technology itself, and they taught
nothing. The coil, the indicator and the departing packet are the story.

Run:
  blender.exe -b -P tools/blender_scene_v4.py
  CF_PREVIEW_RES=50 CF_PREVIEW_SAMPLES=8 CF_FRAMES=24 CF_TAG=v4seq ...
"""

import json
import math
import os
import sys
import time

import bpy
import mathutils
from bpy_extras.object_utils import world_to_camera_view

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cf_qa  # noqa: E402

# ---------------------------------------------------------------- config ---
RES_PCT = int(os.environ.get("CF_PREVIEW_RES", "100"))
SAMPLES = int(os.environ.get("CF_PREVIEW_SAMPLES", "32"))
FRAMES = int(os.environ.get("CF_FRAMES", "1"))
STILL_FRAME = int(os.environ.get("CF_STILL_FRAME", "0"))
SHOT = os.environ.get("CF_SHOT", "product_still")
TAG = os.environ.get("CF_TAG", "v4")
EXPECTED = os.environ.get("CF_EXPECTED_CURVE", "")  # comma-separated luma targets

OUT_DIR = cf_qa.report_dir(__file__)
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


# -------------------------------------------------------------- helpers ---
def material(name, base, rough, metallic=0.0, coat=0.0, emit=None, emit_str=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*base, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if coat:
        for k in ("Coat Weight", "Clearcoat"):
            if k in b.inputs:
                b.inputs[k].default_value = coat
                break
    if emit is not None:
        for k in ("Emission Color", "Emission"):
            if k in b.inputs:
                b.inputs[k].default_value = (*emit, 1.0)
                break
        if "Emission Strength" in b.inputs:
            b.inputs["Emission Strength"].default_value = emit_str
    return m


def emit_strength_socket(mat):
    b = mat.node_tree.nodes.get("Principled BSDF")
    return b.inputs.get("Emission Strength")


def rounded(name, dims, loc, bevel=0.002, segments=6, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = dims
    ob.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = ob.modifiers.new("Bevel", "BEVEL")
    mod.width = bevel
    mod.segments = segments
    mod.limit_method = "ANGLE"
    return ob


def track_to(ob, target):
    con = ob.constraints.new("TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    return con


# ------------------------------------------------------------- geometry ---
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "Floor"
# Matte. A glossy floor was the noisiest region in every earlier test and it
# dominated the bottom third of frame.
floor.data.materials.append(material("Floor", (0.008, 0.009, 0.011), 0.55))

# No backdrop geometry. A plane produced a hard horizontal seam where its edge
# met the floor. The world gradient below does the same job with no seam, and
# it gives the metallic chip something to reflect without any extra geometry.


# --- terminal: base slab + raised reader head -------------------------------
term_base = rounded("TermBase", (0.098, 0.104, 0.014), (0, 0.006, 0.007), bevel=0.006, segments=12)
shell = material("Shell", (0.070, 0.073, 0.080), 0.46, metallic=0.10)
term_base.data.materials.append(shell)

term_head = rounded("TermHead", (0.090, 0.048, 0.034), (0, 0.016, 0.030), bevel=0.009, segments=14, rot=(-0.22, 0, 0))
term_head.data.materials.append(shell)

# Parented to the head so it sits flush on the sloped face. Positioned in
# world space it protruded through the housing as a bright wedge.
screen = rounded("Screen", (0.070, 0.030, 0.0014), (0, 0, 0), bevel=0.0012, segments=4)
screen.parent = term_head
screen.matrix_parent_inverse = mathutils.Matrix.Identity(4)
screen.location = (0, 0.0, 0.0176)
screen_mat = material("Screen", (0.006, 0.045, 0.042), 0.10, emit=(0.04, 0.45, 0.40), emit_str=0.35)
screen.data.materials.append(screen_mat)

# NFC indicator on the reader face: the visual "the reader saw the card" beat.
indicator = rounded("Indicator", (0.010, 0.010, 0.0012), (0.034, 0.012, 0.0168),
                    bevel=0.0012, segments=4)
ind_mat = material("Indicator", (0.02, 0.5, 0.45), 0.2, emit=(0.15, 1.0, 0.85), emit_str=0.0)
indicator.data.materials.append(ind_mat)

# --- card -------------------------------------------------------------------
CARD_W, CARD_H, CARD_T = 0.0856, 0.0540, 0.00076
card = rounded("Card", (CARD_W, CARD_H, CARD_T), (0.004, 0.004, 0.086),
               bevel=0.0012, segments=3, rot=(0.10, -0.06, 0.16))
card.data.materials.append(material("CardBody", (0.016, 0.030, 0.082), 0.20, coat=0.8))
bpy.context.view_layer.update()
CARD_M = card.matrix_world.copy()


def on_card(name, dims, offset, mat, bevel=0.0003, segments=2):
    """Attach a detail to the card in card-local space.

    Parenting with an identity parent-inverse gives world = card.matrix_world @
    T(offset), so the detail follows the card when the card animates. Baking the
    matrix once — the earlier approach — left the chip and coil floating where
    the card started while the card descended away from them.
    """
    ob = rounded(name, dims, (0, 0, 0), bevel=bevel, segments=segments)
    ob.data.materials.append(mat)
    ob.parent = card
    ob.matrix_parent_inverse = mathutils.Matrix.Identity(4)
    ob.location = offset
    return ob


chip = on_card("Chip", (0.012, 0.0095, 0.0004), (-0.021, 0.009, 0.00050),
               material("Chip", (0.80, 0.60, 0.26), 0.22, metallic=1.0), bevel=0.0004)
on_card("Stripe", (CARD_W * 0.94, 0.0075, 0.00016), (0.0, -0.016, 0.00048),
        material("Stripe", (0.006, 0.007, 0.009), 0.80))

# Antenna coil: four thin bars inset from the card edge, forming the rectangular
# loop a real ISO 14443 card carries. Accuracy here is the whole point - this is
# the part that actually couples to the reader.
# Etched copper, not chrome. At metallic 1.0 / roughness 0.35 the coil caught a
# broad white specular and dominated the frame as a bright wire outline.
coil_mat = material("Coil", (0.20, 0.11, 0.05), 0.55, metallic=0.55,
                    emit=(0.25, 1.0, 0.80), emit_str=0.0)
INSET, THICK = 0.0035, 0.0009
COIL_L = CARD_W - 2 * INSET
COIL_H = CARD_H - 2 * INSET
on_card("CoilTop", (COIL_L, THICK, 0.00018), (0.0, COIL_H / 2, 0.00046), coil_mat, bevel=0.00008)
on_card("CoilBottom", (COIL_L, THICK, 0.00018), (0.0, -COIL_H / 2, 0.00046), coil_mat, bevel=0.00008)
on_card("CoilLeft", (THICK, COIL_H, 0.00018), (-COIL_L / 2, 0.0, 0.00046), coil_mat, bevel=0.00008)
on_card("CoilRight", (THICK, COIL_H, 0.00018), (COIL_L / 2, 0.0, 0.00046), coil_mat, bevel=0.00008)

# --- the departing request --------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0060, location=(0.0, 0.02, 0.05))
packet = bpy.context.object
packet.name = "Packet"
bpy.ops.object.shade_smooth()
pkt_mat = material("Packet", (0.3, 1.0, 0.9), 0.25, emit=(0.30, 1.0, 0.85), emit_str=0.0)
packet.data.materials.append(pkt_mat)


# --------------------------------------------------------------- camera ---
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


# 55 mm, not 85. At 85 mm the framed height was 26 cm, so the departing request
# left the top of frame within six frames and the third beat was invisible.
# A wider lens shows the whole terminal plus the air above it, which is where
# the story's payoff happens.
CAM_START = mathutils.Vector((0.215, -0.470, 0.255))
CAM_END = mathutils.Vector((0.150, -0.350, 0.205))
TGT_START = mathutils.Vector((0.0, 0.012, 0.088))
TGT_END = mathutils.Vector((0.0, 0.028, 0.100))

bpy.ops.object.camera_add(location=CAM_START)
cam = bpy.context.object
cam.data.lens = 65
track_to(cam, target)
scene.camera = cam


# --------------------------------------------------------------- lights ---
def area_light(name, loc, size, power, color=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    lt = bpy.context.object
    lt.name = name
    lt.data.shape = "DISK"
    lt.data.size = size
    lt.data.energy = power
    lt.data.color = color
    track_to(lt, target)
    return lt


rig_root = bpy.data.objects.new("LightRig", None)
scene.collection.objects.link(rig_root)

_lights = [
    area_light("Key", (0.300, -0.300, 0.340), 0.130, 5.2, (1.00, 0.97, 0.93)),
    area_light("Fill", (-0.320, -0.180, 0.170), 0.220, 0.55, (0.86, 0.91, 1.00)),
    area_light("Rim", (-0.120, 0.380, 0.360), 0.090, 3.0, (0.78, 0.90, 1.00)),
    area_light("Back", (0.060, 0.300, 0.180), 0.140, 1.2, (0.85, 0.95, 1.00)),
]
for _lt in _lights:
    _lt.parent = rig_root
    _lt.matrix_parent_inverse = rig_root.matrix_world.inverted()

# Studio gradient world: dark below, cool grey above. View-independent fill, so
# it does not drift as the camera moves, and metal has a gradient to mirror.
world = bpy.data.worlds.new("W")
world.use_nodes = True
_wn = world.node_tree
_bg = _wn.nodes["Background"]
_co = _wn.nodes.new("ShaderNodeTexCoord")
_se = _wn.nodes.new("ShaderNodeSeparateXYZ")
_rp = _wn.nodes.new("ShaderNodeValToRGB")
_co.location, _se.location, _rp.location = (-900, 0), (-700, 0), (-500, 0)
_wn.links.new(_co.outputs["Generated"], _se.inputs["Vector"])
_wn.links.new(_se.outputs["Z"], _rp.inputs["Fac"])
_rp.color_ramp.elements[0].position = 0.42
_rp.color_ramp.elements[0].color = (0.004, 0.005, 0.008, 1.0)
_rp.color_ramp.elements[1].position = 0.95
_rp.color_ramp.elements[1].color = (0.200, 0.215, 0.240, 1.0)
_wn.links.new(_rp.outputs["Color"], _bg.inputs["Color"])
_bg.inputs["Strength"].default_value = 0.85
scene.world = world


# ------------------------------------------------------------ animation ---
STORY_FRAMES = int(os.environ.get("CF_STORY_FRAMES", "24"))


def at(f):
    """0..1 progress across the shot.

    Uses the story length, not the render length, so a single still rendered at
    frame 12 shows the same beat the sequence would reach at frame 12.
    """
    return 0.0 if STORY_FRAMES <= 1 else (f - 1) / (STORY_FRAMES - 1)


def story(f):
    """Place every animated element for frame f."""
    p = at(f)

    # Camera: eased dolly, not a constant-speed orbit.
    e = smoothstep(p)
    cam.location = CAM_START.lerp(CAM_END, e)
    target.location = TGT_START.lerp(TGT_END, e)

    # The light rig translates with the camera, so the subject's lighting does
    # not change as the camera moves. Rotation is not involved: this shot dollies.
    delta = cam.location - CAM_START
    rig_root.location = (delta.x, delta.y, 0.0)

    # Beat 1: the card descends.
    descend = smoothstep(min(p / 0.34, 1.0))
    card.location = (0.004, 0.004, 0.086 - 0.026 * descend)

    # Beat 2: the coil energises as the card enters the field.
    coil = smoothstep(min(max((p - 0.16) / 0.22, 0.0), 1.0))
    key_emission_at(coil_mat, 14.0 * coil)
    screen_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.35 + 0.55 * coil

    # Beat 3: the reader confirms, then the request departs.
    confirm = smoothstep(min(max((p - 0.42) / 0.14, 0.0), 1.0))
    key_emission_at(ind_mat, 9.0 * confirm)

    depart = smoothstep(min(max((p - 0.55) / 0.45, 0.0), 1.0))
    if depart <= 0.0:
        packet.location = (0.0, 0.042, 0.058)
        packet.scale = (0.001, 0.001, 0.001)
    else:
        # End point is chosen to stay inside the framed height: the request
        # must be seen leaving, not leave the frame immediately.
        # Start behind the reader head so the packet never passes through the
        # card, and end inside the vertical half-FOV (checked by geometry, not
        # by re-rendering).
        a = mathutils.Vector((0.0, 0.042, 0.058))
        b = mathutils.Vector((0.006, 0.078, 0.168))
        c = mathutils.Vector((0.004, 0.080, 0.086))
        # Quadratic Bezier: the request leaves the reader and arcs away, rather
        # than travelling in a straight line that reads as a UI animation.
        pos = (1 - depart) ** 2 * a + 2 * (1 - depart) * depart * c + depart ** 2 * b
        packet.location = pos
        grow = smoothstep(min(depart / 0.18, 1.0))
        fade = 1.0 - smoothstep(max((depart - 0.82) / 0.18, 0.0))
        s = 0.15 + 0.85 * grow * fade
        packet.scale = (s, s, s)
    key_emission_at(pkt_mat, 22.0 * smoothstep(min(depart / 0.12, 1.0)) * (1.0 - smoothstep(max((depart - 0.85) / 0.15, 0.0))))


def key_emission_at(mat, value):
    sock = emit_strength_socket(mat)
    if sock is not None:
        sock.default_value = value


def keyframe_story(frames):
    scene.frame_start = 1
    scene.frame_end = frames
    for f in range(1, frames + 1):
        story(f)
        cam.keyframe_insert("location", frame=f)
        target.keyframe_insert("location", frame=f)
        rig_root.keyframe_insert("location", frame=f)
        card.keyframe_insert("location", frame=f)
        packet.keyframe_insert("location", frame=f)
        packet.keyframe_insert("scale", frame=f)
        for mat, mult in ((coil_mat, 14.0), (ind_mat, 9.0)):
            sock = emit_strength_socket(mat)
            if sock:
                sock.keyframe_insert("default_value", frame=f)
        sock = emit_strength_socket(pkt_mat)
        if sock:
            sock.keyframe_insert("default_value", frame=f)
        sock = emit_strength_socket(screen_mat)
        if sock:
            sock.keyframe_insert("default_value", frame=f)


# -------------------------------------------------------- render settings ---
for engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try:
        scene.render.engine = engine
        break
    except TypeError:
        continue
else:
    raise SystemExit("No Eevee engine identifier accepted")

scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = RES_PCT
scene.render.film_transparent = False
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.eevee.taa_render_samples = SAMPLES
for attr, val in (("use_shadow_jitter", True), ("shadow_ray_count", 4), ("shadow_step_count", 12)):
    try:
        setattr(scene.eevee, attr, val)
    except Exception:
        pass

scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "None"
scene.view_settings.exposure = 0.0

print("VERSION", bpy.app.version_string)
print("ENGINE", scene.render.engine)
print("SHOT", SHOT)

def project_rect(ob, radius, margin=1.30):
    """Screen rect that both follows and scales with an object.

    Following alone is not enough. On a dolly the subject grows, so a fixed-size
    box that tracked position still filled up with subject and its rising mean
    read as exposure drift. Sizing the box from the projected radius keeps the
    subject-to-background ratio constant, which is what makes the remaining
    change actual exposure.
    """
    bpy.context.view_layer.update()
    ndc = world_to_camera_view(scene, cam, ob.matrix_world.translation)
    sx = scene.render.resolution_x * RES_PCT / 100.0
    sy = scene.render.resolution_y * RES_PCT / 100.0
    d = (ob.matrix_world.translation - cam.location).length
    half = radius * (cam.data.lens / 36.0) * sy / max(d, 1e-4) * margin
    return (ndc.x * sx - half, (1.0 - ndc.y) * sy - half, 2 * half, 2 * half)


REGION_TRACK = {"card": [], "chip": [], "terminal": []}

frame_times = []
paths = []

if FRAMES > 1:
    keyframe_story(FRAMES)
    for f in range(1, FRAMES + 1):
        path = os.path.join(OUT_DIR, f"{TAG}_f{f:04d}.png")
        scene.render.filepath = path
        scene.frame_set(f)
        for _n, _o, _r in (("card", card, 0.050), ("chip", chip, 0.007), ("terminal", term_base, 0.062)):
            REGION_TRACK[_n].append(project_rect(_o, _r))
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        dt = time.perf_counter() - t0
        frame_times.append(dt)
        paths.append(path)
        print(f"FRAME {f} SECONDS {dt:.2f}")
else:
    story(max(STILL_FRAME, 1))
    bpy.context.view_layer.update()
    path = os.path.join(OUT_DIR, f"{TAG}.png")
    scene.render.filepath = path
    t0 = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    frame_times = [time.perf_counter() - t0]
    paths = [path]
    print(f"RENDER_SECONDS {frame_times[0]:.2f}")


# ------------------------------------------------------------------- QA ---
def screen_rect(ob, margin=0.03):
    """Screen-space rect around an object, for region QA."""
    bpy.context.view_layer.update()
    ndc = world_to_camera_view(scene, cam, ob.matrix_world.translation)
    sx = scene.render.resolution_x * RES_PCT / 100.0
    sy = scene.render.resolution_y * RES_PCT / 100.0
    cx, cy = ndc.x * sx, (1.0 - ndc.y) * sy
    # margin given as a fraction of the short side
    m = margin * min(sx, sy)
    return (cx - m, cy - m, 2 * m, 2 * m)


stats = cf_qa.measure(paths[-1], SHOT)
lines = [
    f"scene=v4",
    f"shot={SHOT}",
    f"resolution={scene.render.resolution_x}x{scene.render.resolution_y}@{RES_PCT}%",
    f"samples={SAMPLES}",
    f"frames={FRAMES}",
    f"frame_seconds=" + ",".join(f"{t:.2f}" for t in frame_times),
    f"mean_luminance={stats['mean']:.4f}",
    f"p99_luminance={stats['p99']:.4f}",
    f"dark_fraction={stats['dark_fraction']:.4f}",
    f"frame_gate={stats['frame_gate']}",
    f"frame_gate_reason={stats['frame_gate_reason']}",
]

if FRAMES > 1:
    regions = REGION_TRACK
    curve = [float(x) for x in EXPECTED.split(",") if x.strip()] or None
    qa = cf_qa.sequence_qa(paths, SHOT, regions=regions, expected=curve)
    whole = qa["whole"]
    lines += [
        f"seq_max_deviation={whole['max_deviation']:.4f}",
        f"seq_drift={whole['drift']:+.4f}",
        f"seq_flicker_index={whole['flicker_index']:.5f}",
        f"seq_luma_first={whole['first']:.4f}",
        f"seq_luma_last={whole['last']:.4f}",
    ]
    if "expected_curve_error" in qa:
        lines.append(f"seq_expected_curve_error={qa['expected_curve_error']:.4f}")
    for name, m in qa.get("regions", {}).items():
        lines.append(
            f"region_{name}_deviation={m['max_deviation']:.4f}"
            f" region_{name}_flicker={m['flicker_index']:.5f}"
            f" region_{name}_first={m['first']:.4f}"
            f" region_{name}_last={m['last']:.4f}"
        )
    lines.append(f"seq_verdict={qa['seq_verdict']}")
    per = sorted(frame_times[1:])[len(frame_times[1:]) // 2] if len(frame_times) > 1 else frame_times[0]
    lines.append(f"per_frame_seconds={per:.2f}")
    lines.append(f"est_240_frames_seconds={2.0 + 240 * per:.1f}")

cf_qa.write_report(os.path.join(OUT_DIR, f"{TAG}.txt"), lines)
for ln in lines:
    print("CF " + ln)
