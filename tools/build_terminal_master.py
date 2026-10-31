"""Build the production master for the CC0 payment terminal (CF-150).

Run:
  blender.exe -b -P tools/build_terminal_master.py

Imports assets/models/receipt-point-of-sale-terminal.glb, normalises the
transform so the model sits at the world origin with its base on z=0, records
the licence in scene metadata, and saves assets/models/terminal_master.blend.
The GLB stays the untouched download; the .blend is the adapted master and the
only file the template links against.
"""

import os

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLB = os.path.join(ROOT, "assets", "models", "receipt-point-of-sale-terminal.glb")
OUT = os.path.join(ROOT, "assets", "models", "terminal_master.blend")
COLL = "ASSET_Terminal"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)

scene = bpy.context.scene
imported = [o for o in scene.collection.objects] + [o for c in scene.collection.children for o in c.objects]
root_objs = [o for o in scene.collection.objects]
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
if not meshes:
    raise SystemExit("FAIL: no meshes imported")

# One collection holds the whole asset so the template can link it as a unit.
coll = bpy.data.collections.new(COLL)
scene.collection.children.link(coll)
for o in list(bpy.data.objects):
    if o.name not in coll.objects:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)

# Centre X/Y on the model, put its base at z=0. Move the top-level objects only;
# children follow their parents.
lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for corner in o.bound_box:
        w = o.matrix_world @ Vector(corner)
        lo = Vector(map(min, lo, w))
        hi = Vector(map(max, hi, w))
offset = Vector((-(lo.x + hi.x) / 2.0, -(lo.y + hi.y) / 2.0, -lo.z))
for o in bpy.data.objects:
    if o.parent is None:
        o.location += offset

# The GLB carries material *names* but every baseColorFactor is the 0.8 grey
# default, so all four surfaces render the same colour. Assign the colour and
# finish each name specifies; this is the whole adaptation the asset needs.
MATERIALS = {
    "Black molded polymer": ((0.012, 0.012, 0.013, 1.0), 0.45, 0.0, 0.0),
    "Charcoal fine-textured powdercoat": ((0.030, 0.031, 0.034, 1.0), 0.58, 0.0, 0.0),
    "Dark inactive display glass": ((0.004, 0.005, 0.007, 1.0), 0.10, 0.0, 0.8),
    "Warm ivory satin cabinet enamel": ((0.68, 0.63, 0.54, 1.0), 0.38, 0.0, 0.0),
}
for name, (color, rough, metal, coat) in MATERIALS.items():
    mat = bpy.data.materials.get(name)
    if mat is None or not mat.use_nodes:
        raise SystemExit(f"FAIL: material missing after import: {name}")
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Coat Weight"].default_value = coat

scene["cf_asset_id"] = "receipt-pos-terminal-cc0"
scene["cf_asset_source"] = "https://www.innerscene.com/tools/library/3d-parts/counter-pay-payment-terminal-74006716"
scene["cf_asset_licence"] = "CC0"
scene["cf_asset_adapted"] = "2026-10-31"
scene["cf_asset_triangles"] = 5100

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("MASTER", OUT)
print("COLLECTION", COLL)
print("OBJECTS", len(bpy.data.objects), "MESHES", len(meshes))
print("OFFSET", tuple(round(v, 4) for v in offset))
