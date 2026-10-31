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
# Geometry-only mode walks the animation and asserts screen/collision safety
# without rendering. A trajectory defect is a geometry fact; finding it by
# rendering 24 frames costs a minute and states nothing you can regression-test.
GEOMETRY_ONLY = os.environ.get("CF_GEOMETRY_ONLY", "0") == "1"
# Controlled-experiment switch: zero the scripted emission ramps but leave all
# geometry and lighting alone. Running the sequence twice — once with the ramps,
# once without — is what separates "the coil is why the card region brightened"
# from "the card region brightened, and the coil is a plausible excuse".
EMISSION_GAIN = 0.0 if os.environ.get("CF_NO_EMISSION", "0") == "1" else 1.0
# Opt-in camera-language probe: depth of field, 180-degree shutter and a contrast
# look, so lens discipline can be judged on a still before any sequence exists.
# Unset, the baseline render is unchanged.
LENS_PROBE = os.environ.get("CF_LENS_PROBE", "0") == "1"

OUT_DIR = cf_qa.report_dir(__file__)
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


# -------------------------------------------------------------- helpers ---
def material(name, base, rough, metallic=0.0, coat=0.0, emit=None, emit_str=0.0, spec=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*base, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if spec is not None:
        # Dielectric reflection level. A display with an anti-reflective coating
        # returns far less than the default 0.5, which is the only reliable way
        # to stop a large light painting a white sheet across a flat panel.
        for k in ("Specular IOR Level", "Specular"):
            if k in b.inputs:
                b.inputs[k].default_value = spec
                break
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


# --- terminal ---------------------------------------------------------------
# A countertop reader built from the parts a viewer can name: a body, a tilted
# display in a glossy bezel, a keypad with coloured cancel and enter keys, a
# card slot, and a status LED on the reader lip.
#
# The previous version was a slab with a bright rectangle on it, and it read as
# stacked rounded boxes for one reason: shell, head and screen were all the same
# cool grey within 12 % of each other, so nothing told the eye where the display
# ended and the housing began. Separation here is done with value and specular
# contrast — near-black gloss bezel, dark glass, mid graphite shell, coloured
# keys — not with more light. That is also the fix for focal hierarchy: the eye
# goes card, chip, screen, then rests on a deliberately quiet housing.
SHELL = material("Shell", (0.028, 0.028, 0.031), 0.46, metallic=0.05, coat=0.10)
# Bezels at 0.18 roughness behave as mirrors under a small key light and render
# as a white line around the display — the frame read brighter than the screen.
# Near-black on purpose. At the shell's value the bezel had no edge, so the
# display appeared to float on the housing with no frame around it.
BEZEL = material("Bezel", (0.004, 0.004, 0.005), 0.35, coat=0.35, spec=0.25)
KEYPAD = material("Key", (0.030, 0.031, 0.034), 0.42, coat=0.15)
KEY_CANCEL = material("KeyCancel", (0.220, 0.030, 0.028), 0.40, coat=0.20)
KEY_ENTER = material("KeyEnter", (0.020, 0.140, 0.075), 0.40, coat=0.20)
SLOT = material("CardSlot", (0.003, 0.003, 0.004), 0.28, coat=0.40)

term_base = rounded("TermBase", (0.098, 0.108, 0.016), (0, 0.004, 0.008),
                    bevel=0.007, segments=12)
term_base.data.materials.append(SHELL)

# Tilt is POSITIVE: a reader's display faces up and toward the user. The old
# negative tilt turned the screen away from camera, which foreshortened it into
# exactly the coloured slab CF-136 describes.
HEAD_TILT = 0.20
term_head = rounded("TermHead", (0.092, 0.052, 0.036), (0, 0.020, 0.032),
                    bevel=0.008, segments=14, rot=(HEAD_TILT, 0, 0))
term_head.data.materials.append(SHELL)


def on_head(name, dims, local, mat, bevel=0.0008, segments=3):
    """Attach a part to the reader head in head-local space."""
    ob = rounded(name, dims, (0, 0, 0), bevel=bevel, segments=segments)
    ob.data.materials.append(mat)
    ob.parent = term_head
    ob.matrix_parent_inverse = mathutils.Matrix.Identity(4)
    ob.location = local
    return ob


# Head half-height is 0.018, so these stack outward from the top face.
on_head("ScreenBezel", (0.080, 0.042, 0.0016), (0, 0.0, 0.0184), BEZEL, bevel=0.0012, segments=4)
# Dark glass, almost no emission of its own. The old screen glowed as one flat
# teal slab, which reads as a sticker. A display is dark glass with lit content.
# Matte, not glass. Two passes proved the point: at roughness 0.06, and again at
# 0.22 with a coat, the panel mirrored the key light as a single white sheet and
# every display element under it vanished. A display reads as bright content on
# near-black; the surface itself must return almost nothing. Dropping the coat
# and raising roughness to 0.38 removed the sheet without touching the lights.
screen_mat = material("ScreenGlass", (0.002, 0.005, 0.007), 0.45, coat=0.0,
                      emit=(0.02, 0.16, 0.16), emit_str=0.10, spec=0.10)
screen = on_head("Screen", (0.070, 0.032, 0.0010), (0, 0.0, 0.0194), screen_mat,
                 bevel=0.0010, segments=4)

# Display content: an amount line and a status glyph. Geometry, not a texture —
# there is no font available and text at this size would be illegible at 360 px
# anyway. A bar says "an amount is here"; a check that lights up says "approved".
# Emission strengths here are low because AgX desaturates anything bright: at
# 3.2 the cyan bar clipped to white and the display lost its colour entirely.
INK = material("ScreenInk", (0.10, 0.55, 0.55), 0.30, emit=(0.30, 0.90, 0.95), emit_str=0.9)
on_head("ScreenAmount", (0.034, 0.0048, 0.0002), (-0.012, 0.0085, 0.0201), INK)

# The approval tick: two arms sharing a vertex at (0.0140, 0.0062). Laid out by
# solving for that shared point; the first attempt placed both by eye, they
# crossed, and the result read as a white star rather than a tick. Its emission
# is the only channel that animates, so the flip to green needs no colour keys.
TICK = material("ScreenTick", (0.05, 0.55, 0.28), 0.30, emit=(0.20, 1.0, 0.55), emit_str=0.0)
_TICK_VERTEX = (0.0140, 0.0062)
for _name, _length, _angle in (("ScreenTickShort", 0.0040, -50.0),
                               ("ScreenTickLong", 0.0075, 50.0)):
    _a = math.radians(_angle)
    _dx, _dy = math.cos(_a), math.sin(_a)
    _sign = 1.0 if _angle > 0 else -1.0
    _cx = _TICK_VERTEX[0] + _sign * _length / 2 * _dx
    _cy = _TICK_VERTEX[1] + _sign * _length / 2 * _dy
    _arm = on_head(_name, (_length, 0.0016, 0.0003), (_cx, _cy, 0.0203), TICK,
                   bevel=0.0002, segments=2)
    _arm.rotation_euler = (0, 0, _a)

# Keypad on the base deck, in front of the head. Four rows of three, with the
# bottom row carrying cancel / zero / enter — the layout every reader has, and
# the only colour on the housing.
# Row pitch is wider than key depth on purpose: at the earlier pitch the gaps
# closed up under the bevel and twelve keys rendered as one ribbed block.
KEY_ROW = (-0.0130, -0.0216, -0.0302, -0.0388)
KEY_COL = (-0.022, 0.0, 0.022)
for _r, _y in enumerate(KEY_ROW):
    for _c, _x in enumerate(KEY_COL):
        _mat = KEYPAD
        if _r == 3:
            _mat = KEY_CANCEL if _c == 0 else (KEY_ENTER if _c == 2 else KEYPAD)
        rounded(f"Key_{_r}{_c}", (0.017, 0.0062, 0.0022), (_x, _y, 0.0164),
                bevel=0.0009, segments=3).data.materials.append(_mat)

# Card slot: a dark recess along the front edge of the body.
rounded("CardSlot", (0.058, 0.0030, 0.0018), (0, -0.0498, 0.0105),
        bevel=0.0006, segments=3).data.materials.append(SLOT)

# Status LED on the reader lip: the "the reader saw the card" beat. Small on
# purpose — the screen and the coil carry the beat at readable size, this is an
# accent, and claiming more for it would be describing a pixel.
ind_mat = material("Indicator", (0.02, 0.5, 0.45), 0.2, emit=(0.15, 1.0, 0.85), emit_str=0.0)
indicator = on_head("Indicator", (0.0075, 0.0030, 0.0006), (0.0335, -0.0215, 0.0186),
                    ind_mat, bevel=0.0004, segments=3)

# --- card -------------------------------------------------------------------
CARD_W, CARD_H, CARD_T = 0.0856, 0.0540, 0.00076
# The card is held over the reader's front lip, not over the display. Centred on
# the screen — the earlier position — an 86 mm card at 9 mm above it hid the
# whole panel from a camera looking down, which is why every attempt to make the
# screen "read as a display" failed: nothing was visible to read.
CARD_X, CARD_Y = 0.004, -0.046
# Thin bevel: at 0.0012 the edge caught a hard specular all the way round and
# the card rendered with a white LED border instead of a rounded edge.
card = rounded("Card", (CARD_W, CARD_H, CARD_T), (CARD_X, CARD_Y, 0.086),
               bevel=0.0004, segments=3, rot=(0.10, -0.06, 0.16))
card.data.materials.append(material("CardBody", (0.010, 0.018, 0.050), 0.45, coat=0.10, spec=0.30))
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
# Dark base, bright emission. A light base colour plus emission summed to white
# under AgX and the request read as a paper disc instead of a cyan signal.
pkt_mat = material("Packet", (0.02, 0.20, 0.18), 0.25, emit=(0.05, 0.95, 0.80), emit_str=0.0)
packet.data.materials.append(pkt_mat)


# --------------------------------------------------------------- camera ---
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


# 65 mm, not 85. At 85 mm the framed height was 26 cm, so the departing request
# left the top of frame within six frames and the third beat was invisible.
# A wider lens shows the whole terminal plus the air above it, which is where
# the story's payoff happens.
# Camera elevation is a composition constraint, not a taste: from 17 degrees
# above the subject a card held 10 mm over the display still projects across it.
# 23 degrees plus a forward tap point is what actually separates card and screen.
CAM_START = mathutils.Vector((0.115, -0.420, 0.278))
# End framing pulls back 15 mm and aims at the card rather than at x=0. At the
# previous end pose the card's left edge crossed the frame boundary for the
# last ~10 frames, which reads as an accident rather than a crop.
CAM_END = mathutils.Vector((0.078, -0.335, 0.232))
# Aim below the card, not above it. Aiming at 0.088-0.100 put the subject in
# the bottom third and left two-thirds of the frame empty; the packet needs that
# headroom, the terminal does not.
TGT_START = mathutils.Vector((0.0, 0.012, 0.074))
TGT_END = mathutils.Vector((0.010, 0.028, 0.082))

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
    # Larger and dimmer per unit area than the original 0.13 m / 5.2 W: the same
    # illuminance spread over a wider source, so a flat panel reflects a soft
    # gradient instead of a hot disc.
    area_light("Key", (0.300, -0.300, 0.340), 0.220, 11.0, (1.00, 0.97, 0.93)),
    area_light("Fill", (-0.320, -0.180, 0.170), 0.220, 0.55, (0.86, 0.91, 1.00)),
    area_light("Rim", (-0.120, 0.380, 0.360), 0.090, 1.0, (0.78, 0.90, 1.00)),
    area_light("Back", (0.060, 0.300, 0.180), 0.140, 1.2, (0.85, 0.95, 1.00)),
]
for _lt in _lights:
    _lt.parent = rig_root
    _lt.matrix_parent_inverse = rig_root.matrix_world.inverted()

# Kept for the declared exposure curve. An area light's falloff is not exactly
# inverse-square, but over the 0.35-0.55 m range this shot works in the error is
# under a percent, and the curve is a prediction whose accuracy is reported.
LIGHT_POWER = [(_lt, _lt.data.energy) for _lt in _lights]

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

# Opt-in asset probe: swap the procedural gradient for a CC0 studio HDRI that is
# already recorded in assets/manifest.json. This exists to prove the HDR parses
# headless and changes reflections; with CF_ASSET_HDRI unset the world above is
# used unchanged.
ASSET_HDRI = os.environ.get("CF_ASSET_HDRI", "")
if ASSET_HDRI:
    _env = _wn.nodes.new("ShaderNodeTexEnvironment")
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _env.image = bpy.data.images.load(os.path.join(_root, ASSET_HDRI), check_existing=True)
    _wn.links.new(_env.outputs["Color"], _bg.inputs["Color"])
    _bg.inputs["Strength"].default_value = float(os.environ.get("CF_HDRI_STRENGTH", "0.3"))


# ------------------------------------------------------------ animation ---
STORY_FRAMES = int(os.environ.get("CF_STORY_FRAMES", "24"))


def _vec_env(name, default):
    raw = os.environ.get(name, "").strip()
    if not raw:
        return mathutils.Vector(default)
    return mathutils.Vector(tuple(float(v) for v in raw.split(",")))


# Packet Bezier control points, overridable so the geometry test can replay a
# known-bad trajectory as a negative control. A gate that has never failed has
# not been shown to work.
# Launch point sits above the card plane (z 0.060) and behind the card's y
# extent. At the old z it was screened by the card's far edge for its first
# frame — in frame, in the open, and still invisible, which only the ray cast
# could see.
PKT_A = _vec_env("CF_PACKET_A", (0.0, 0.048, 0.068))
# Apex lowered with the camera: closing the framing 20 % pushed the old endpoint
# through the top edge at frames 23-24. The geometry gate found it before a
# render did, which is the point of having one.
PKT_B = _vec_env("CF_PACKET_B", (0.006, 0.068, 0.150))
PKT_C = _vec_env("CF_PACKET_C", (0.004, 0.080, 0.086))


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
    card.location = (CARD_X, CARD_Y, 0.086 - 0.030 * descend)

    # Beat 2: the coil energises as the card enters the field.
    coil = smoothstep(min(max((p - 0.16) / 0.22, 0.0), 1.0))
    # 14 clipped the coil to white, so the antenna read as a LED border on the
    # card rather than as copper carrying current. 4.0 keeps it cyan.
    key_emission_at(coil_mat, 4.0 * coil * EMISSION_GAIN)

    # Beat 3: the reader confirms, then the request departs. The approval tick
    # is what makes the screen read as a display rather than a lamp, so it
    # lights with the LED instead of the glass brightening as a whole.
    confirm = smoothstep(min(max((p - 0.42) / 0.14, 0.0), 1.0))
    key_emission_at(ind_mat, 3.0 * confirm * EMISSION_GAIN)
    key_emission_at(TICK, 2.2 * confirm * EMISSION_GAIN)

    depart = smoothstep(min(max((p - 0.55) / 0.45, 0.0), 1.0))
    if depart <= 0.0:
        packet.location = (0.0, 0.042, 0.058)
        packet.scale = (0.001, 0.001, 0.001)
    else:
        # The request must be seen leaving: start behind the reader head so it
        # never crosses the card, and end inside the frame. Both properties are
        # asserted by `packet_geometry`, which walks this curve without
        # rendering — the earlier path was tuned by eye across several renders.
        # Quadratic Bezier: the request arcs away from the reader rather than
        # travelling in a straight line that reads as a UI animation.
        pos = ((1 - depart) ** 2 * PKT_A
               + 2 * (1 - depart) * depart * PKT_C
               + depart ** 2 * PKT_B)
        packet.location = pos
        # No fade-out. The request used to shrink to a dot and go dark over the
        # last three frames, which reads as "it vanished" rather than "it left".
        # It now stays lit and in frame, and the next shot carries it onward.
        grow = smoothstep(min(depart / 0.18, 1.0))
        s = 0.15 + 0.85 * grow
        packet.scale = (s, s, s)
    # 22 clipped to white under AgX, so the packet read as a paper disc rather
    # than an energised request. 6.0 keeps the cyan hue inside the gamut.
    key_emission_at(pkt_mat, 1.2 * smoothstep(min(depart / 0.12, 1.0)))


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
        for mat in (coil_mat, ind_mat, TICK, pkt_mat):
            sock = emit_strength_socket(mat)
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

if LENS_PROBE:
    # Shallow focus on the card, a 180-degree shutter and a contrast look. These
    # are the three cheapest perceived-quality levers measured in the V5
    # treatment; this block exists to prove they render headless on this host.
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = card
    cam.data.dof.aperture_fstop = float(os.environ.get("CF_FSTOP", "2.8"))
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = float(os.environ.get("CF_MBLUR", "0.5"))
    scene.view_settings.look = "AgX - Medium High Contrast"

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


# ------------------------------------------------- camera-space geometry QA ---
FRAME_MARGIN = 0.06      # NDC the packet must keep from every frame edge
CLEARANCE_MIN = 0.0015   # 1.5 mm, about two card thicknesses


def _obb_half(ob):
    """Half-extents of an object's local bounding box."""
    bb = ob.bound_box
    return tuple((max(v[i] for v in bb) - min(v[i] for v in bb)) / 2.0 for i in range(3))


def _obb_distance(ob, p):
    """Distance from a world point to the object's oriented box. 0 when inside."""
    q = ob.matrix_world.inverted() @ p
    h = _obb_half(ob)
    d = [max(abs(q[i]) - h[i], 0.0) for i in range(3)]
    return math.sqrt(sum(v * v for v in d))


def _ndc_radius(p, r):
    """NDC half-size of a sphere of radius r at world point p, and its depth.

    Blender's default AUTO sensor fit applies the 36 mm sensor to the LONGER
    image side. This shot is portrait, so the vertical side gets it — flipping
    the output to landscape would silently invert the two terms below.
    """
    view = (target.location - cam.location).normalized()
    depth = (p - cam.location).dot(view)
    tan_v = 18.0 / cam.data.lens
    tan_h = tan_v * scene.render.resolution_x / scene.render.resolution_y
    return r / (max(depth, 1e-6) * tan_h), r / (max(depth, 1e-6) * tan_v), depth


PACKET_RADIUS = 0.0060


def _occluder(origin, p, r):
    """Name of the first solid object between the camera and the packet, or None."""
    dg = bpy.context.evaluated_depsgraph_get()
    d = p - origin
    dist = d.length
    hit, loc, _n, _i, ob, _m = scene.ray_cast(dg, origin, d.normalized(), distance=dist)
    if hit and ob is not packet and (loc - origin).length < dist - r:
        return ob.name
    return None


def packet_geometry(frames):
    """Walk the packet through the shot; assert it is screen-safe and collision-free.

    Returns (rows, problems). A row is one frame: position, whether the packet is
    past the fade-in threshold, and its clearance to the nearest solid object.
    """
    solids = [
        ("card", card), ("chip", chip), ("terminal_base", term_base),
        ("terminal_head", term_head), ("screen", screen), ("indicator", indicator),
    ]
    rows, problems = [], []
    for f in range(1, frames + 1):
        story(f)
        bpy.context.view_layer.update()
        p = packet.matrix_world.translation.copy()
        r = PACKET_RADIUS * packet.scale.x
        moving = packet.scale.x >= 0.10
        nearest = min((_obb_distance(o, p) - r, n) for n, o in solids)
        if nearest[0] < CLEARANCE_MIN:
            problems.append(f"f{f}: {nearest[0] * 1000:.1f} mm from {nearest[1]}")
        if p.z - r <= 0.0:
            problems.append(f"f{f}: below the floor")
        ndc_x = ndc_y = float("nan")
        if moving:
            ndc = world_to_camera_view(scene, cam, p)
            ndc_x, ndc_y = ndc.x, ndc.y
            rx, ry, depth = _ndc_radius(p, r)
            if depth <= 0:
                problems.append(f"f{f}: behind the camera")
            for axis, v, rad in (("x", ndc_x, rx), ("y", ndc_y, ry)):
                if not (FRAME_MARGIN + rad <= v <= 1.0 - FRAME_MARGIN - rad):
                    problems.append(f"f{f}: {axis}={v:.3f}+-{rad:.3f} breaks the margin")
            # In frame is not the same as visible. Cast to the packet and check
            # nothing solid is in front of it: a bright sphere behind the card
            # would satisfy every other test here and still be hidden.
            blocker = _occluder(cam.location, p, r)
            if blocker:
                problems.append(f"f{f}: hidden behind {blocker}")
        rows.append((f, moving, p, nearest[0], nearest[1], ndc_x, ndc_y))
    return rows, problems


def curve_at(target_ob, frames):
    """Declared exposure curve: relative illuminance at a subject, per frame.

    Every light is parented to rig_root, so it translates with the camera. The
    subject moves too — the card descends 26 mm — so the light-to-subject
    distance still changes and a dolly-in genuinely brightens. This measures
    that change from the real light positions. It is a prediction from geometry
    and inverse-square falloff, not a curve fitted to a render.
    """
    out = []
    for f in range(1, frames + 1):
        story(f)
        bpy.context.view_layer.update()
        tp = target_ob.matrix_world.translation
        out.append(sum(pw / max((lt.matrix_world.translation - tp).length_squared, 1e-6)
                       for lt, pw in LIGHT_POWER))
    return [v / out[0] for v in out] if out and out[0] > 0 else out


REGION_TRACK = {"card": [], "chip": [], "terminal": []}

frame_times = []
paths = []

if GEOMETRY_ONLY:
    rows, problems = packet_geometry(max(FRAMES, 2))
    moving = [r for r in rows if r[1]]
    margins = [min(r[5], 1.0 - r[5], r[6], 1.0 - r[6]) for r in moving]
    worst = min(rows, key=lambda r: r[3])
    lines = [
        "scene=v4",
        "mode=geometry_only",
        f"frames={len(rows)}",
        f"packet_moving_frames={len(moving)}",
        f"packet_first_moving={moving[0][0] if moving else '-'}",
        f"packet_last_moving={moving[-1][0] if moving else '-'}",
        f"packet_min_edge_margin={min(margins):.3f}" if margins else "packet_min_edge_margin=-",
        f"packet_last_ndc=({moving[-1][5]:.3f},{moving[-1][6]:.3f})" if moving else "packet_last_ndc=-",
        f"packet_min_clearance_mm={worst[3] * 1000:.2f}",
        f"packet_nearest_object={worst[4]}",
        f"packet_geometry={'PASS' if not problems else 'FAIL'}",
    ]
    lines += [f"packet_problem={p}" for p in problems]
    cf_qa.write_report(os.path.join(OUT_DIR, f"{TAG}_geometry.txt"), lines)
    for ln in lines:
        print("CF " + ln)
    raise SystemExit(0)

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
    # The declared curve comes from geometry unless one is supplied explicitly.
    # The card is the reference subject for the whole frame: it is what the shot
    # is about, and the floor and background are deliberately near-black.
    curve = [float(x) for x in EXPECTED.split(",") if x.strip()] or curve_at(card, FRAMES)
    region_curves = {name: curve_at(ob, FRAMES)
                     for name, ob in (("card", card), ("chip", chip), ("terminal", term_base))}
    qa = cf_qa.sequence_qa(paths, SHOT, regions=regions, expected=curve,
                           region_expected=region_curves)
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
        extra = ""
        if "expected_error" in m:
            extra = f" region_{name}_expected_error={m['expected_error']:.4f}"
        lines.append(
            f"region_{name}_deviation={m['max_deviation']:.4f}"
            f" region_{name}_flicker={m['flicker_index']:.5f}"
            f" region_{name}_first={m['first']:.4f}"
            f" region_{name}_last={m['last']:.4f}" + extra
        )
    # The declared curve is written out so the report can be audited without
    # re-running the scene: these are the numbers the verdict was judged against.
    lines.append("expected_ref=card")
    lines.append("expected_curve=" + ",".join(f"{v:.4f}" for v in curve))
    lines.append(f"seq_verdict={qa['seq_verdict']}")
    per = sorted(frame_times[1:])[len(frame_times[1:]) // 2] if len(frame_times) > 1 else frame_times[0]
    lines.append(f"per_frame_seconds={per:.2f}")
    lines.append(f"est_240_frames_seconds={2.0 + 240 * per:.1f}")

cf_qa.write_report(os.path.join(OUT_DIR, f"{TAG}.txt"), lines)
for ln in lines:
    print("CF " + ln)
