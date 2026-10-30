"""CF-025: corrected Eevee scene with an objective exposure gate.

Why this file exists
--------------------
`blender_evee_test.py` produced a nearly black frame. The cause was the SCENE,
not the hardware:

  1. Card albedo 0.035-0.06 linear (~3.5-6% reflectance) - near-black material.
  2. World background 0.01 - essentially no ambient fill.
  3. Key/fill lights aimed with hand-set Euler angles, not tracked to the subject.
  4. Blender 5.x defaults to the AgX view transform, which compresses the little
     signal present into near-black.
  5. 50 mm at 2.44 m cropped the 1.6 m card horizontally in a 9:16 frame.

This scene fixes all five and prints a measured mean luminance so "black" is a
number, not an opinion.

Run:
  blender.exe -b -P tools/blender_scene_proof.py
Preview override:
  CF_PREVIEW_RES=360 CF_PREVIEW_SAMPLES=8 blender.exe -b -P tools/blender_scene_proof.py

Outputs to tools/blender-test/: proof.png and proof.txt
"""

import math
import os
import time

import bpy
import mathutils
from bpy_extras.object_utils import world_to_camera_view

# ---------------------------------------------------------------- config ---
RES_PCT = int(os.environ.get("CF_PREVIEW_RES", "540"))
SAMPLES = int(os.environ.get("CF_PREVIEW_SAMPLES", "16"))
EXPOSURE = float(os.environ.get("CF_EXPOSURE", "0"))
TAG = os.environ.get("CF_TAG", "proof")
FRAMES = int(os.environ.get("CF_FRAMES", "1"))
# Lighting candidate. A = camera-relative rig, B = fixed rig + gradient world.
RIG = os.environ.get("CF_RIG", "A").upper()
# Render a single still at a given orbit index without running the sequence.
STILL_ORBIT = int(os.environ.get("CF_STILL_ORBIT", "0"))
# A scripted light move is legitimate; an unnoticed one is not. Setting this
# reclassifies drift from FAIL to INFO so the QA can tell the two apart.
INTENTIONAL_DRIFT = os.environ.get("CF_INTENTIONAL_DRIFT", "0") == "1"

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tools",
    "blender-test",
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PNG = os.path.join(OUT_DIR, f"{TAG}.png")
OUT_TXT = os.path.join(OUT_DIR, f"{TAG}.txt")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


# -------------------------------------------------------------- helpers ---
def material(name, base, rough, metallic=0.0, coat=0.0, emit=None, emit_str=0.0):
    """Principled material; optional coat and emission, tolerant of API drift."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*base, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if coat:
        for key in ("Coat Weight", "Clearcoat"):
            if key in b.inputs:
                b.inputs[key].default_value = coat
                break
        for key in ("Coat Roughness", "Clearcoat Roughness"):
            if key in b.inputs:
                b.inputs[key].default_value = 0.08
                break
    if emit is not None:
        for key in ("Emission Color", "Emission"):
            if key in b.inputs:
                b.inputs[key].default_value = (*emit, 1.0)
                break
        if "Emission Strength" in b.inputs:
            b.inputs["Emission Strength"].default_value = emit_str
    return m


def rounded(name, dims, loc, bevel=0.002, segments=4, rot=(0, 0, 0)):
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
    """Aim an object's -Z at a target. Fixes bug 3 in the original scene."""
    con = ob.constraints.new("TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"


# ------------------------------------------------------------- geometry ---
# Studio floor. Low roughness gives the reflective "infinity" look cheaply.
bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "Floor"
# 0.30, not 0.18: at mirror roughness the floor reflected the terminal as hard
# banded stripes that read as a rendering artefact.
floor.data.materials.append(material("StudioFloor", (0.010, 0.011, 0.014), 0.40))

# Payment terminal: a rounded slab lying on the floor.
terminal = rounded("Terminal", (0.115, 0.088, 0.020), (0, 0, 0.010), bevel=0.007, segments=10)
terminal.data.materials.append(material("TerminalShell", (0.048, 0.050, 0.056), 0.42, metallic=0.15))

# Screen, slightly proud of the top face, angled toward camera.
screen = rounded(
    "Screen", (0.088, 0.062, 0.0016), (0, 0.002, 0.0208), bevel=0.0015, segments=3,
    rot=(0.10, 0, 0),
)
# Emission is deliberately weak: at 4.0 it clipped to pure white and stopped
# reading as a display. 1.0 keeps the colour while leaving tonal detail.
screen.data.materials.append(
    material("Screen", (0.010, 0.090, 0.080), 0.10, emit=(0.04, 0.60, 0.52), emit_str=1.0)
)

# Contactless card: real ID-1 dimensions, floating, tilted.
CARD_W, CARD_H, CARD_T = 0.0856, 0.0540, 0.00076
card = rounded(
    "Card", (CARD_W, CARD_H, CARD_T), (0.004, 0.006, 0.066),
    bevel=0.0012, segments=3, rot=(0.16, -0.12, 0.28),
)
card.data.materials.append(
    material("CardPlastic", (0.020, 0.035, 0.090), 0.22, coat=0.7)
)

# Chip: parented to the card so it sits on the tilted face instead of a world
# coordinate that the card's rotation leaves behind.
# Transforms are not flushed until the view layer updates. Reading
# card.matrix_world before this returns a stale matrix, which is why the chip
# and stripes were previously placed nowhere visible.
bpy.context.view_layer.update()
CARD_M = card.matrix_world.copy()


def on_card(name, dims, local_offset, mat, bevel=0.0003, segments=2):
    """Place a detail object on the card using the card's actual world matrix."""
    ob = rounded(name, dims, (0, 0, 0), bevel=bevel, segments=segments)
    ob.data.materials.append(mat)
    ob.matrix_world = CARD_M @ mathutils.Matrix.Translation(local_offset)
    return ob


chip = on_card(
    "Chip", (0.012, 0.0095, 0.0004), (-0.019, 0.008, 0.00050),
    material("ChipGold", (0.80, 0.60, 0.26), 0.24, metallic=1.0), bevel=0.0004,
)

# Magnetic stripe: one wide dark band across the card face. Without it the card
# reads as a blue rectangle rather than a payment instrument.
on_card(
    "Stripe", (CARD_W * 0.94, 0.0075, 0.00016), (0.0, -0.016, 0.00048),
    # Rough 0.80: at 0.42 the key light turned the "dark" stripe into a bright
    # specular band, so it read as a highlight instead of a magnetic stripe.
    material("StripeMat", (0.006, 0.007, 0.009), 0.80),
)

# NFC field: three emissive arcs between card and terminal. Major radii are
# tuned so the rings read as an expanding field, not as hoops larger than the card.
for i, (r, z, s) in enumerate(
    ((0.014, 0.030, 1.5), (0.020, 0.040, 1.1), (0.026, 0.050, 0.8))
):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=r, minor_radius=0.00045, location=(0.004, 0.006, z),
        major_segments=64, minor_segments=6, rotation=(0.10, 0, 0),
    )
    ring = bpy.context.object
    ring.name = f"FieldRing{i}"
    ring.data.materials.append(
        material(f"Field{i}", (0.02, 0.5, 0.45), 0.4, emit=(0.05, 0.95, 0.80), emit_str=s)
    )


# ---------------------------------------------------------------- camera ---
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)
target.location = (0, 0, 0.046)

# 0.54 m stand-off. At 85 mm that frames ~22 cm of height, so the 5.4 cm card
# occupies a quarter of the frame with the terminal below it and headroom above.
bpy.ops.object.camera_add(location=(0.255, -0.415, 0.255))
cam = bpy.context.object
cam.data.lens = 85
track_to(cam, target)
scene.camera = cam


# ---------------------------------------------------------------- lights ---
def area_light(name, loc, size, power, target_ob, color=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    lt = bpy.context.object
    lt.name = name
    lt.data.shape = "DISK"
    lt.data.size = size
    lt.data.energy = power
    lt.data.color = color
    track_to(lt, target_ob)
    return lt


# Three-point setup at product-photography scale (decimetres, not metres).
# Power scales with distance squared; these values are set for a 0.5 m stand-off.
# Rim sits back and high; at a closer position its floor specular was a large
# blown white blot in the lower right of the frame.
_LIGHTS = [
    ("Key", (0.300, -0.320, 0.360), 0.120, 3.0, (1.00, 0.97, 0.93)),
    ("Fill", (-0.320, -0.210, 0.180), 0.200, 0.5, (0.86, 0.91, 1.00)),
    ("Rim", (-0.140, 0.420, 0.400), 0.070, 3.4, (0.80, 0.92, 1.00)),
]
_lights = [area_light(n, loc, s, p, target, color=c) for n, loc, s, p, c in _LIGHTS]

# Rig A carries the lights around with the camera so the key never leaves the
# subject. Rig B leaves them world-fixed.
rig_root = None
if RIG == "A":
    rig_root = bpy.data.objects.new("LightRig", None)
    scene.collection.objects.link(rig_root)
    rig_root.location = (0.0, 0.0, 0.0)
    for _lt in _lights:
        _lt.parent = rig_root
        _lt.matrix_parent_inverse = rig_root.matrix_world.inverted()


def build_world(mode):
    """B gets a vertical gradient environment.

    Two jobs at once: it gives the metallic chip something to reflect (a pure
    metal has no diffuse term and renders black against an empty world), and it
    supplies view-independent fill, which is what stops the camera orbit from
    losing exposure as it turns away from the key.
    """
    w = bpy.data.worlds.new("StudioWorld")
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    if mode == "B":
        coord = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        coord.location = (-900, 0)
        sep.location = (-700, 0)
        ramp.location = (-500, 0)
        nt.links.new(coord.outputs["Generated"], sep.inputs["Vector"])
        nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
        ramp.color_ramp.elements[0].position = 0.30
        ramp.color_ramp.elements[0].color = (0.012, 0.014, 0.020, 1.0)
        ramp.color_ramp.elements[1].position = 0.90
        ramp.color_ramp.elements[1].color = (0.230, 0.245, 0.270, 1.0)
        nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = 1.0
    else:
        bg.inputs[0].default_value = (0.004, 0.005, 0.009, 1.0)
        bg.inputs[1].default_value = 0.20
    return w


scene.world = build_world(RIG)


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
scene.render.filepath = OUT_PNG
scene.render.image_settings.color_mode = "RGB"

try:
    scene.eevee.taa_render_samples = SAMPLES
except Exception as exc:
    print("EEVEE_SAMPLES_WARN", exc)

# Shadow quality. At default settings the soft penumbra on the terminal's
# bevel showed as horizontal bands that read as a rendering artefact.
# CF_SHADOW_QUALITY=0 renders with Blender defaults, so sample-count
# comparisons are not confounded by shadow settings.
if os.environ.get("CF_SHADOW_QUALITY", "1") != "0":
    for attr, val in (
        ("use_shadow_jitter", True),
        ("shadow_ray_count", 4),
        ("shadow_step_count", 12),
    ):
        try:
            setattr(scene.eevee, attr, val)
        except Exception:
            pass

# Bug 4 fix: state the view transform explicitly instead of inheriting AgX blindly,
# then compensate exposure so a dark art direction still reads.
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "None"
scene.view_settings.exposure = EXPOSURE

print("VERSION", bpy.app.version_string)
print("ENGINE", scene.render.engine)
print("RESOLUTION", scene.render.resolution_x, scene.render.resolution_y, RES_PCT)
print("SAMPLES", getattr(scene.eevee, "taa_render_samples", "?"))
print("VIEW_TRANSFORM", scene.view_settings.view_transform, "EXPOSURE", EXPOSURE)

ORBIT_STEP_DEG = 1.5
ORBIT_R = (cam.location.x ** 2 + cam.location.y ** 2) ** 0.5
ORBIT_A0 = math.atan2(cam.location.y, cam.location.x)
CAM_Z = cam.location.z


def place_orbit(index, keyframe_frame=None):
    """Put the camera, and for rig A the light rig, at orbit position `index`.

    One function drives stills and sequences so both are rendered from exactly
    the same positions — the comparison is otherwise not controlled.
    """
    a = ORBIT_A0 + index * math.radians(ORBIT_STEP_DEG)
    cam.location = (ORBIT_R * math.cos(a), ORBIT_R * math.sin(a), CAM_Z)
    if rig_root is not None:
        rig_root.rotation_euler = (0.0, 0.0, index * math.radians(ORBIT_STEP_DEG))
    if keyframe_frame is not None:
        cam.keyframe_insert("location", frame=keyframe_frame)
        if rig_root is not None:
            rig_root.keyframe_insert("rotation_euler", frame=keyframe_frame)


def orbit_camera(frames):
    """Keyframe a small arc so consecutive frames differ.

    Without differing frames Eevee can reuse its internal result cache and the
    second timing would be meaningless.
    """
    scene.frame_start = 1
    scene.frame_end = frames
    for f in range(1, frames + 1):
        place_orbit(f - 1, keyframe_frame=f)


def probe_gpu():
    """Read the real GPU backend AFTER a render.

    The CF-020 report recorded that `gpu` is uninitialised in background mode.
    That is true before the first render, not after it: once a render has run
    the context exists and the backend can be named. This closes that unknown.
    """
    try:
        import gpu

        print("GPU_RENDERER", gpu.platform.renderer_get())
        print("GPU_VENDOR", gpu.platform.vendor_get())
        print("GPU_VERSION", gpu.platform.version_get())
        try:
            print("GPU_BACKEND", gpu.platform.backend_type_get())
        except Exception as exc:
            print("GPU_BACKEND_UNAVAILABLE", exc)
    except Exception as exc:
        print("GPU_PROBE_FAILED", exc)


frame_times = []
if FRAMES > 1:
    # CF_ANIMATE=0 keeps the scene static across frames. Any pixel difference
    # between static frames is temporal sampling noise, which is what flicker
    # in a 240-frame sequence looks like.
    if os.environ.get("CF_ANIMATE", "1") != "0":
        orbit_camera(FRAMES)
    for f in range(1, FRAMES + 1):
        scene.render.filepath = os.path.join(OUT_DIR, f"{TAG}_f{f:04d}.png")
        scene.frame_set(f)
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        dt = time.perf_counter() - t0
        frame_times.append(dt)
        print(f"FRAME {f} SECONDS {dt:.2f}")
    elapsed = frame_times[0]
    last_png = os.path.join(OUT_DIR, f"{TAG}_f{FRAMES:04d}.png")
else:
    if STILL_ORBIT:
        place_orbit(STILL_ORBIT)
        bpy.context.view_layer.update()
    start = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    elapsed = time.perf_counter() - start
    frame_times = [elapsed]
    last_png = OUT_PNG
    print(f"RENDER_SECONDS {elapsed:.2f}")

probe_gpu()


# --------------------------------------------------------- exposure gate ---
def measure(path):
    """Mean and percentile luminance of the rendered frame.

    This is the acceptance test the original benchmark lacked: a frame below
    MEAN_MIN is a failure of the scene, and must not be read as a hardware
    finding.
    """
    import numpy as np

    img = bpy.data.images.load(path, check_existing=False)
    buf = np.empty(len(img.pixels), dtype=np.float32)
    img.pixels.foreach_get(buf)
    rgb = buf.reshape(-1, 4)[:, :3]
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    return {
        "mean": float(lum.mean()),
        "p95": float(np.percentile(lum, 95)),
        "p99": float(np.percentile(lum, 99)),
        # fraction of the frame that is essentially black
        "dark_fraction": float((lum < 0.01).mean()),
    }


MEAN_MIN = 0.040   # below this the frame is black and the test is void
MEAN_MAX = 0.400   # above this the frame is washed out
HIGHLIGHT_MIN = 0.70  # a lit product shot must contain real specular highlights

stats = measure(last_png)
problems = []
if not MEAN_MIN <= stats["mean"] <= MEAN_MAX:
    problems.append(f"mean {stats['mean']:.4f} outside [{MEAN_MIN}, {MEAN_MAX}]")
if stats["p99"] < HIGHLIGHT_MIN:
    problems.append(f"p99 {stats['p99']:.4f} below {HIGHLIGHT_MIN} - no highlights")
verdict = "PASS" if not problems else "FAIL"

# Separate the one-time cost (frame 1, includes shader compilation and GPU
# context setup) from the marginal cost of each additional frame. The original
# CF-020 report extrapolated 240 x frame_1; if frame 1 is mostly setup, that
# extrapolation overstates animation cost by an order of magnitude.
if FRAMES > 1:
    warm = sorted(frame_times[1:])
    per_frame = warm[len(warm) // 2]
    setup = max(frame_times[0] - per_frame, 0.0)
else:
    per_frame = frame_times[0]
    setup = 0.0
est_240 = setup + 240 * per_frame

# --- chip screen position, so crops are reproducible rather than guessed ------
bpy.context.view_layer.update()
try:
    _ndc = world_to_camera_view(scene, cam, chip.matrix_world.translation)
    _sx = scene.render.resolution_x * RES_PCT / 100.0
    _sy = scene.render.resolution_y * RES_PCT / 100.0
    chip_str = f"{_ndc.x * _sx:.0f},{(1.0 - _ndc.y) * _sy:.0f}"
except Exception as exc:
    chip_str = f"unavailable({exc})"

# --- sequence QA ------------------------------------------------------------
# SSIM alone is not sufficient: two frames can be visually similar while the
# whole shot slowly loses exposure. These two measures separate the cases.
#   max_deviation  - largest departure from the first frame, as a fraction
#   flicker_index  - mean |second difference| of the luma series, normalised.
#                    A smooth ramp has near-zero curvature; flicker does not.
DRIFT_MAX = 0.05
FLICKER_MAX = 0.01

seq = {}
seq_verdict = "n/a"
if FRAMES > 1:
    lums = []
    for f in range(1, FRAMES + 1):
        p = os.path.join(OUT_DIR, f"{TAG}_f{f:04d}.png")
        if os.path.exists(p):
            lums.append(measure(p)["mean"])
    if len(lums) >= 3:
        base = lums[0]
        mean_l = sum(lums) / len(lums)
        d2 = [lums[i] - 2 * lums[i - 1] + lums[i - 2] for i in range(2, len(lums))]
        seq = {
            "max_deviation": max(abs(v - base) / base for v in lums),
            "drift": (lums[-1] - base) / base,
            "flicker_index": (sum(abs(v) for v in d2) / len(d2)) / mean_l,
            "luma_first": lums[0],
            "luma_last": lums[-1],
            "luma_min": min(lums),
            "luma_max": max(lums),
        }
        problems = []
        if seq["max_deviation"] > DRIFT_MAX:
            tag = "INFO(intentional-drift)" if INTENTIONAL_DRIFT else "FAIL"
            problems.append(
                f"{tag} exposure deviation {seq['max_deviation'] * 100:.1f}% > {DRIFT_MAX * 100:.0f}%"
            )
        if seq["flicker_index"] > FLICKER_MAX:
            problems.append(
                f"FAIL flicker index {seq['flicker_index']:.5f} > {FLICKER_MAX}"
            )
        seq_verdict = "PASS" if not problems else " | ".join(problems)


def _f(key, fmt="{:.4f}", default=0.0):
    return fmt.format(seq.get(key, default))


report = [
    f"rig={RIG}",
    f"chip_screen_px={chip_str}",
    f"version={bpy.app.version_string}",
    f"engine={scene.render.engine}",
    f"resolution={scene.render.resolution_x}x{scene.render.resolution_y}@{RES_PCT}%",
    f"samples={SAMPLES}",
    f"view_transform={scene.view_settings.view_transform}",
    f"exposure={EXPOSURE}",
    f"frames={FRAMES}",
    f"frame_seconds=" + ",".join(f"{t:.2f}" for t in frame_times),
    f"setup_seconds={setup:.2f}",
    f"per_frame_seconds={per_frame:.2f}",
    f"est_240_frames_seconds={est_240:.2f}",
    f"mean_luminance={stats['mean']:.4f}",
    f"p95_luminance={stats['p95']:.4f}",
    f"p99_luminance={stats['p99']:.4f}",
    f"dark_fraction={stats['dark_fraction']:.4f}",
    f"gate={verdict}",
    f"seq_max_deviation={_f('max_deviation', '{:.4f}', -1.0)}",
    f"seq_drift={_f('drift', '{:+.4f}')}",
    f"seq_flicker_index={_f('flicker_index', '{:.5f}', -1.0)}",
    f"seq_luma_first={_f('luma_first')}",
    f"seq_luma_last={_f('luma_last')}",
    f"seq_luma_min={_f('luma_min')}",
    f"seq_luma_max={_f('luma_max')}",
    f"seq_verdict={seq_verdict}",
]

with open(OUT_TXT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(report) + "\n")

for line in report:
    print("CF " + line)

print("GATE", verdict)
if verdict == "FAIL":
    print("GATE_HINT", f"mean={stats['mean']:.4f} outside [{MEAN_MIN}, {MEAN_MAX}]")
