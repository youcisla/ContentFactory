"""Inspect a glTF/GLB asset headlessly and print its importable facts.

Run:
  blender.exe -b -P tools/inspect_model.py -- assets/models/<file>.glb

Prints objects, triangles, materials, embedded images and world-space bounds.
Exits non-zero when the import produced no geometry, which is the only defect
this check can prove; brand marks and visual quality need human eyes.
"""

import os
import sys

import bpy
from mathutils import Vector


def arg_path():
    argv = sys.argv
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        if rest:
            return rest[0]
    raise SystemExit("usage: blender -b -P tools/inspect_model.py -- <model.glb>")


def main():
    path = os.path.abspath(arg_path())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)

    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in meshes)
    if not meshes or tris == 0:
        raise SystemExit("FAIL: import produced no mesh geometry")

    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in meshes:
        for corner in o.bound_box:
            w = o.matrix_world @ Vector(corner)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))

    mats = sorted({m.name for o in meshes for m in o.data.materials if m})
    images = sorted(bpy.path.basename(i.filepath) for i in bpy.data.images if i.filepath)
    print("MODEL", path)
    print("OBJECTS", [(o.name, o.type) for o in bpy.data.objects])
    print("MESHES", len(meshes), "TRIANGLES", tris)
    print("MATERIALS", mats)
    print("IMAGES", images)
    print("BOUNDS_MIN", tuple(round(v, 4) for v in lo))
    print("BOUNDS_MAX", tuple(round(v, 4) for v in hi))
    print("SIZE_M", tuple(round(b - a, 4) for a, b in zip(lo, hi)))


main()
