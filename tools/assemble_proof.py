"""Smallest useful assembly proof: three stills -> captioned 9:16 MP4.

Run: python tools/assemble_proof.py

Uses only installed FFmpeg and the three rendered shot templates. No narration
and no music: no TTS engine or licensed track exists on this host, so the output
is captioned-only and must be labelled that way. Prints ffprobe facts and the
wall-clock assembly time.
"""

import json
import os
import shutil
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "render", "assembly", "assembly_proof.mp4")
SHOTS = [
    ("render/stills/t01_product_macro.png", "A payment terminal reads the card"),
    ("render/stills/t02_object_interaction.png", "The chip talks to the terminal"),
    ("render/stills/t03_cutaway.png", "The network approves the payment"),
]
FONT = "C:/Windows/Fonts/arialbd.ttf"
SEG, FADE = 4.0, 0.5


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    # ffmpeg's filter parser cannot take a Windows drive path for fontfile even
    # with the colon escaped, so stage the system font under the repo and use a
    # relative path. The copy lives in render/ and is regenerable.
    font = os.path.join(ROOT, "render", "assembly", "font.ttf")
    shutil.copyfile(FONT, font)
    inputs = []
    for rel, _cap in SHOTS:
        inputs += ["-loop", "1", "-t", str(SEG), "-i", os.path.join(ROOT, rel)]
    chains = [f"[{i}:v]scale=540:960,setsar=1,fps=24[v{i}]" for i in range(len(SHOTS))]
    chains.append("[v0][v1]xfade=transition=fade:duration=%s:offset=%s[x1]" % (FADE, SEG - FADE))
    chains.append("[x1][v2]xfade=transition=fade:duration=%s:offset=%s[x2]" % (FADE, 2 * SEG - 2 * FADE))
    caps = []
    for i, (_rel, cap) in enumerate(SHOTS):
        start = i * (SEG - FADE) + 0.2
        end = start + SEG - FADE - 0.3
        caps.append(
            "drawtext=fontfile=render/assembly/font.ttf:text=%s:fontsize=26:fontcolor=white:"
            "box=1:boxcolor=black@0.55:boxborderw=14:x=(w-text_w)/2:y=h-150:"
            "enable=between(t\\,%.2f\\,%.2f)" % (cap, start, end)
        )
    chains.append("[x2]" + ",".join(caps) + ",format=yuv420p[out]")
    cmd = (
        ["ffmpeg", "-y", "-loglevel", "error"]
        + inputs
        + ["-filter_complex", ";".join(chains), "-map", "[out]", "-r", "24",
           "-c:v", "libx264", "-crf", "20", "-movflags", "+faststart", OUT]
    )
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode:
        raise SystemExit("ffmpeg failed:\n" + proc.stderr[-2000:])
    return time.time() - t0


def probe():
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_name,width,height,nb_frames,r_frame_rate",
         "-of", "json", OUT], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


seconds = build()
facts = probe()
stream = facts["streams"][0]
print("OUTPUT", OUT)
print("ASSEMBLY_SECONDS", round(seconds, 2))
print("DURATION_S", round(float(facts["format"]["duration"]), 3))
print("SIZE_MB", round(int(facts["format"]["size"]) / 1e6, 2))
print("VIDEO", stream)
