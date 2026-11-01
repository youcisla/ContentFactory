"""Assemble the four V5 shots into one captioned 9:16 sequence with FFmpeg.

Run: python tools/assemble_v5.py

Reads shots/v5_sequence.json (order, captions, transition lengths) and each
shot's render/sequences/<name>.json pointer (frames dir, count, fps) written by
tools/shot_render.py. Crossfades are real xfade transitions; captions are burned
with drawtext. Prints ffprobe facts and the assembly wall-clock time.
"""

import json
import os
import shutil
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "shots", "v5_sequence.json")
OUT = os.path.join(ROOT, "render", "assembly", "v5_sequence.mp4")
FONT_SRC = "C:/Windows/Fonts/arialbd.ttf"


def shot_info(rel_spec):
    shot = json.load(open(os.path.join(ROOT, rel_spec), encoding="utf-8"))
    pointer = json.load(open(os.path.join(ROOT, shot["output"]), encoding="utf-8"))
    return {
        "frames_dir": os.path.join(ROOT, pointer["frames_dir"]),
        "frames": pointer["frames"],
        "fps": pointer["fps"],
        "duration": pointer["frames"] / pointer["fps"],
    }


def build(manifest):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    font = os.path.join(ROOT, "render", "assembly", "font.ttf")
    shutil.copyfile(FONT_SRC, font)

    shots = [shot_info(s["spec"]) for s in manifest["shots"]]
    fps = manifest["fps"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in shots:
        cmd += ["-framerate", str(s["fps"]), "-start_number", "0",
                "-i", os.path.join(s["frames_dir"], "f%04d.png")]
    chains = [f"[{i}:v]scale=540:960,setsar=1,fps={fps},format=yuv420p[v{i}]" for i in range(len(shots))]

    # Build the timeline and crossfades; caption windows follow the same maths.
    starts, cursor = [], 0.0
    for i, (meta, entry) in enumerate(zip(shots, manifest["shots"])):
        starts.append(cursor)
        cursor += meta["duration"] - entry.get("transition_s", 0.0)
    chains.append(f"[v0][v1]xfade=transition=fade:duration={manifest['shots'][0]['transition_s']}:offset={starts[1]}[x1]")
    chains.append(f"[x1][v2]xfade=transition=fade:duration={manifest['shots'][1]['transition_s']}:offset={starts[2]}[x2]")
    chains.append(f"[x2][v3]xfade=transition=fade:duration={manifest['shots'][2]['transition_s']}:offset={starts[3]}[x3]")

    caps = []
    for i, entry in enumerate(manifest["shots"]):
        end = starts[i] + shots[i]["duration"] - entry.get("transition_s", 0.0) - 0.15
        cap_file = os.path.join(ROOT, "render", "assembly", f"cap_{i}.txt")
        with open(cap_file, "w", encoding="utf-8") as fh:
            fh.write(entry["caption"])
        caps.append(
            "drawtext=fontfile=render/assembly/font.ttf:textfile=render/assembly/cap_%d.txt:fontsize=22:"
            "fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=14:x=(w-text_w)/2:y=h-150:"
            "enable=between(t\\,%.2f\\,%.2f)" % (i, starts[i] + 0.15, end)
        )
    chains.append("[x3]" + ",".join(caps) + "[out]")
    cmd += ["-filter_complex", ";".join(chains), "-map", "[out]", "-r", str(fps),
            "-c:v", "libx264", "-crf", "20", "-movflags", "+faststart", OUT]

    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode:
        raise SystemExit("ffmpeg failed:\n" + proc.stderr[-2000:])
    return time.time() - t0, shots, starts


def probe():
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_name,width,height,nb_frames,r_frame_rate",
         "-of", "json", OUT], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


manifest = json.load(open(MANIFEST, encoding="utf-8"))
seconds, shots, starts = build(manifest)
facts = probe()
stream = facts["streams"][0]
sidecar = {
    "output": os.path.relpath(OUT, ROOT),
    "assembly_seconds": round(seconds, 2),
    "duration_s": round(float(facts["format"]["duration"]), 3),
    "size_mb": round(int(facts["format"]["size"]) / 1e6, 2),
    "video": stream,
    "shots": [
        {"spec": m["spec"], "frames": s["frames"], "duration_s": s["duration"],
         "timeline_start_s": round(st, 3), "transition_s": m.get("transition_s", 0.0),
         "caption": m["caption"]}
        for m, s, st in zip(manifest["shots"], shots, starts)
    ],
}
json.dump(sidecar, open(os.path.splitext(OUT)[0] + ".json", "w", encoding="utf-8"), indent=2)
print("OUTPUT", OUT)
print("ASSEMBLY_SECONDS", sidecar["assembly_seconds"])
print("DURATION_S", sidecar["duration_s"])
print("SIZE_MB", sidecar["size_mb"])
print("VIDEO", stream)
print("TIMELINE", [(s["spec"].split("/")[-1], s["frames"], s["timeline_start_s"]) for s in sidecar["shots"]])
