"""CF-020: one-frame Eevee capability test.

Run: blender.exe -b -P tools/blender_evee_test.py
Writes tools/blender-test/frame.png and prints timing + engine.
No external assets. No network.
"""
import os
import time

import bpy

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "blender-test")
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# --- geometry ---
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.04))
floor = bpy.context.object

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.02))
card = bpy.context.object
card.scale = (0.8, 0.5, 0.015)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bev = card.modifiers.new("Bevel", "BEVEL")
bev.width = 0.012
bev.segments = 4

# --- materials ---
def material(name, base, rough, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*base, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return m

card.data.materials.append(material("CardPlastic", (0.035, 0.045, 0.06), 0.32))
floor.data.materials.append(material("Surface", (0.02, 0.024, 0.032), 0.55))

# --- camera ---
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)
target.location = (0, 0, 0.05)

bpy.ops.object.camera_add(location=(0.9, 1.15, 2.0))
cam = bpy.context.object
cam.data.lens = 50
con = cam.constraints.new("TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"
scene.camera = cam

# --- lights ---
bpy.ops.object.light_add(type="AREA", location=(1.4, 1.2, 1.8))
key = bpy.context.object
key.data.energy = 220
key.data.size = 2.0
key.rotation_euler = (0.9, 0.2, -0.7)

bpy.ops.object.light_add(type="AREA", location=(-1.6, 0.6, 0.9))
fill = bpy.context.object
fill.data.energy = 45
fill.data.size = 3.0
fill.rotation_euler = (1.2, -0.2, 1.1)

world = bpy.data.worlds.new("W")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.018, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
scene.world = world

# --- render settings ---
for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        scene.render.engine = engine
        break
    except TypeError:
        continue
else:
    raise SystemExit("No Eevee engine identifier accepted")

scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(OUT_DIR, "frame.png")

try:
    scene.eevee.taa_render_samples = 64
except Exception as exc:  # API name may differ across versions
    print("EEVEE_SETTINGS_WARN", exc)

print("VERSION", bpy.app.version_string)
print("ENGINE", scene.render.engine)
print("OUTPUT", scene.render.filepath)

start = time.perf_counter()
bpy.ops.render.render(write_still=True)
elapsed = time.perf_counter() - start
print(f"RENDER_SECONDS {elapsed:.2f}")
print("EXISTS", os.path.exists(scene.render.filepath))
