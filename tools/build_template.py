"""Build the reusable ContentFactory studio template (CF-142).

Run with Blender:
  blender.exe -b -P tools/build_template.py

Writes templates/cf_studio_v1.blend and prints a summary. The template holds no
hero prop: it is the set, the light rig, two cameras, the HDRI world and the
render configuration that every shot starts from. Props are appended later.

Why the backdrop is 3 m away: the 2026-10-31 lens probe showed that at tabletop
distance f/2.8-f/5.6 blurs the entire set. Separation only exists when the
background is far enough behind the subject, so the template puts it there.
"""

import json
import os

import bpy
import mathutils

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "templates")
os.makedirs(OUT_DIR, exist_ok=True)
BLEND_PATH = os.path.join(OUT_DIR, "cf_studio_v1.blend")


def load_manifest():
    with open(os.path.join(ROOT, "assets", "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def asset_path(manifest, needle):
    for row in manifest["assets"]:
        if needle in row["path"]:
            return os.path.join(ROOT, row["path"])
    raise SystemExit(f"asset not in manifest: {needle}")


def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def link_only(obj, coll):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)


def image_mat(name, diffuse, rough, normal, metal, tint, scale, roughness=None):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.45
    bsdf.inputs["Metallic"].default_value = 0.0

    def tex(path, colorspace):
        node = nt.nodes.new("ShaderNodeTexImage")
        node.image = bpy.data.images.load(path, check_existing=True)
        node.image.colorspace_settings.name = colorspace
        return node

    col = tex(diffuse, "sRGB")
    rgh = tex(rough, "Non-Color")
    nrm = tex(normal, "Non-Color")
    mtl = tex(metal, "Non-Color") if metal else None
    # The maps tile small on a 1.6 m set, and the raw albedo is too light for a
    # dark studio, so scale the UVs and multiply the colour down.
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (scale, scale, scale)
    uv = nt.nodes.new("ShaderNodeUVMap")
    nt.links.new(uv.outputs["UV"], mapping.inputs["Vector"])
    for n in [col, rgh, nrm] + ([mtl] if mtl else []):
        nt.links.new(mapping.outputs["Vector"], n.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMixRGB")
    mix.blend_type = "MULTIPLY"
    mix.inputs["Fac"].default_value = 1.0
    mix.inputs["Color2"].default_value = tint
    nt.links.new(col.outputs["Color"], mix.inputs["Color1"])
    nt.links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
    if roughness is None:
        nt.links.new(rgh.outputs["Color"], bsdf.inputs["Roughness"])
    else:
        # A glossy map on a tabletop catches the key as a blown specular; the
        # template wants a matte set with texture, not a mirror.
        bsdf.inputs["Roughness"].default_value = roughness
    if mtl:
        nt.links.new(mtl.outputs["Color"], bsdf.inputs["Metallic"])
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(nrm.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    for n, loc in ((col, (-620, 300)), (rgh, (-620, 60)), (nrm, (-620, -180)), (nmap, (-320, -180))):
        n.location = loc
    if mtl:
        mtl.location = (-620, -420)
    return mat


def plane(name, size, loc, mat, coll):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    link_only(ob, coll)
    return ob


def area(name, loc, size, power, color, coll, target=None):
    bpy.ops.object.light_add(type="AREA", location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.data.size = size
    ob.data.energy = power
    ob.data.color = color
    link_only(ob, coll)
    if target is not None:
        c = ob.constraints.new("TRACK_TO")
        c.target = target
        c.track_axis = "TRACK_NEGATIVE_Z"
        c.up_axis = "UP_Y"
    return ob


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
manifest = load_manifest()

# ---------------------------------------------------------------- scene ---
c_cam = collection("CAMERAS")
c_light = collection("LIGHTS")
c_set = collection("SET")
c_props = collection("PROPS")
c_rig = collection("RIGS")

subject = bpy.data.objects.new("SubjectMarker", None)
c_rig.objects.link(subject)
subject.location = (0.0, 0.0, 0.08)

# World: CC0 studio HDRI, low strength, so reflections exist without flattening
world = bpy.data.worlds.new("HDRI")
world.use_nodes = True
ntw = world.node_tree
bg = ntw.nodes["Background"]
env = ntw.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(asset_path(manifest, "brown_photostudio_02"), check_existing=True)
ntw.links.new(env.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 0.30
scene.world = world

# Set: counter under the subject, backdrop 3 m behind it (see module docstring)
plastic = image_mat(
    "CounterPlastic",
    asset_path(manifest, "plastic013a/Plastic013A_1K-JPG_Color"),
    asset_path(manifest, "plastic013a/Plastic013A_1K-JPG_Roughness"),
    asset_path(manifest, "plastic013a/Plastic013A_1K-JPG_NormalGL"),
    None,
    (0.035, 0.040, 0.048, 1.0),
    6.0,
    0.55,
)
metal = image_mat(
    "AccentMetal",
    asset_path(manifest, "metal_plate_diff"),
    asset_path(manifest, "metal_plate_rough"),
    asset_path(manifest, "metal_plate_nor_gl"),
    asset_path(manifest, "metal_plate_metal"),
    (0.22, 0.24, 0.27, 1.0),
    8.0,
)
counter = plane("Counter", 1.6, (0.0, 0.0, 0.0), plastic, c_set)
backdrop = plane("Backdrop", 8.0, (0.0, 3.0, 0.0), plastic, c_set)
backdrop.rotation_euler = (1.5707963, 0.0, 0.0)
trim = plane("TrimMetal", 1.6, (0.0, 0.72, 0.002), metal, c_set)
trim.scale = (1.0, 0.025, 1.0)

# Lights: key 2x subject width at 45 deg, fill 25 %, rim behind. 3:1-4:1 target.
# Powers are measured, not guessed: a 1.0 scale gave mean 0.501 and p95 0.909
# (blown), 0.1 gave mean 0.212 and p95 0.526. These values are the 0.1 scale,
# with fill kept at 1/4 of key so the ratio stays 4:1.
key = area("Key", (0.55, -0.55, 0.85), 0.35, 2.2, (1.0, 0.94, 0.86), c_light, subject)
fill = area("Fill", (-0.70, -0.45, 0.30), 0.60, 0.55, (0.82, 0.90, 1.0), c_light, subject)
rim = area("Rim", (-0.10, 0.75, 0.55), 0.25, 7.0, (0.85, 0.92, 1.0), c_light, subject)

# Cameras: macro 85 mm and wide 35 mm, both aimed at the subject marker
def camera(name, loc, lens, fstop):
    bpy.ops.object.camera_add(location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.data.lens = lens
    ob.data.dof.use_dof = True
    ob.data.dof.focus_object = subject
    ob.data.dof.aperture_fstop = fstop
    c = ob.constraints.new("TRACK_TO")
    c.target = subject
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    link_only(ob, c_cam)
    return ob


cam_macro = camera("CAM_Macro_85", (0.10, -0.42, 0.20), 85.0, 8.0)
cam_wide = camera("CAM_Wide_35", (0.22, -0.70, 0.34), 35.0, 5.6)
scene.camera = cam_wide

# Render configuration
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
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.eevee.taa_render_samples = 32
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 0.0

scene["cf_template"] = "cf_studio_v1"
scene["cf_template_date"] = "2026-10-31"
scene["cf_asset_manifest"] = "assets/manifest.json"
scene["cf_light_ratio"] = "key:fill 4:1 (2.2 W vs 0.55 W); scale measured 2026-10-31"

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print("TEMPLATE", BLEND_PATH)
print("COLLECTIONS", [c.name for c in bpy.context.scene.collection.children])
print("OBJECTS", sorted(o.name for o in bpy.data.objects))
print("CAMERA", scene.camera.name, "fps", scene.render.fps, "samples", scene.eevee.taa_render_samples)
