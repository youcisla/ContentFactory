"""Build the 40 s animatic from validated assets.

This is an ANIMATIC — a timed previsualisation, not final picture. The first
10 s reuse the rendered 3D shot at its native speed. The remaining 30 s are
lightweight SVG diagrams, because the financial-network beats are diagrams, not
spatial mechanisms: building them in 3D would add render cost and still show
nothing the diagram does not.

Segments, 24 fps, 540x960, 960 frames total:
  A   0-10 s  rendered 3D scene (tools/blender-test/v4final_f*.png)
  B  10-17 s  network.svg      + a cyan request travelling down the chain
  C  17-24 s  decision.svg     + a green response travelling back up
  D  24-32 s  hold.svg         slow push-in
  E  32-40 s  settlement.svg   slow push-in

Every duration below is asserted, not assumed: segment A is pinned to
SEG_A_FRAMES and the assembled file must probe as SEG_A_FRAMES + the 2D frames
and TOTAL_SECONDS exactly. An earlier version read whatever frames happened to
exist, so dropping in the planned 960-frame render would have produced a 70 s
film with every caption after 10 s mistimed, exit code 0.

Nothing here renders 3D. Chrome rasterises the SVGs; ffmpeg assembles. Run:

  python tools/build_animatic.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENES = os.path.join(ROOT, "render", "scenes")
OUT = os.path.join(ROOT, "render", "animatic")
FRAMES = os.path.join(ROOT, "tools", "blender-test")
CAPTIONS = os.path.join(ROOT, "render", "captions", "contactless_40s.srt")
OUT_VIDEO = os.path.join(OUT, "contactless_40s_animatic.mp4")

W, H, FPS = 540, 960, 24
SEG_A_FRAMES = 240
TOTAL_SECONDS = 40.0

CHROME_CANDIDATES = [
    os.path.join(os.environ.get("PROGRAMFILES", ""), "Google", "Chrome", "Application", "chrome.exe"),
    os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Google", "Chrome", "Application", "chrome.exe"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
]

DOT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">
  <circle cx="{c}" cy="{c}" r="{c}" fill="{fill}" opacity="0.22"/>
  <circle cx="{c}" cy="{c}" r="{inner}" fill="{fill}"/>
</svg>
"""

# One entry per 2D segment. `motion` is ('dot', y0, y1) or ('push', zoom_end).
SEGMENTS = [
    {"name": "B", "svg": "network.svg", "seconds": 7, "motion": ("dot", 200, 660), "dot": "#22D3EE"},
    {"name": "C", "svg": "decision.svg", "seconds": 7, "motion": ("dot", 660, 200), "dot": "#34D399"},
    {"name": "D", "svg": "hold.svg", "seconds": 8, "motion": ("push", 1.14), "dot": None},
    {"name": "E", "svg": "settlement.svg", "seconds": 8, "motion": ("push", 1.12), "dot": None},
]


def run(cmd, label, **kw):
    """Run a command from the repo root; name the step that failed."""
    kw.setdefault("cwd", ROOT)
    kw.setdefault("timeout", 600)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, **kw)
    except subprocess.TimeoutExpired:
        raise SystemExit(f"{label}: timed out after {kw['timeout']} s")
    if proc.returncode != 0:
        sys.stderr.write((proc.stderr or "")[-1500:])
        raise SystemExit(f"{label}: failed (exit {proc.returncode})")
    return proc


def png_size(path):
    """Width and height from a PNG's IHDR, without an imaging library."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"not a PNG: {path}")
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def chrome():
    for path in CHROME_CANDIDATES:
        if path and os.path.exists(path):
            return path
    raise SystemExit("Chrome not found (checked Program Files, Program Files (x86), LOCALAPPDATA)")


def rasterise(svg_name, width=W, height=H, transparent=False):
    """Screenshot an SVG at exactly the requested size, or reuse a valid raster.

    Chrome sizes the capture from --window-size, not from the SVG, and paints an
    opaque white page unless told otherwise. It can also exit 0 without writing
    anything when another instance owns the default profile. So the old raster
    is deleted first and the new one is verified by dimensions — trusting the
    exit code alone once shipped a 540x960 white plate as the "moving dot".
    """
    svg = os.path.join(SCENES, svg_name)
    png = svg[:-4] + ".png"
    if not os.path.exists(svg):
        raise SystemExit(f"missing scene source: {svg}")

    if os.path.exists(png) and os.path.getmtime(png) >= os.path.getmtime(svg):
        try:
            if png_size(png) == (width, height):
                return png
        except SystemExit:
            pass  # corrupt raster: fall through and rebuild it

    if os.path.exists(png):
        os.remove(png)
    cmd = [chrome(), "--headless", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=1", f"--window-size={width},{height}",
           f"--user-data-dir={tempfile.mkdtemp(prefix='cf-chrome-')}"]
    if transparent:
        cmd.append("--default-background-color=00000000")
    cmd += [f"--screenshot={png}", "file:///" + svg.replace("\\", "/")]
    run(cmd, f"rasterise {svg_name}")

    if not os.path.exists(png):
        raise SystemExit(f"rasterise {svg_name}: Chrome wrote no file")
    if png_size(png) != (width, height):
        raise SystemExit(f"rasterise {svg_name}: got {png_size(png)}, wanted {(width, height)}")
    return png


def make_dot(hex_colour, name):
    """A soft dot, rasterised once at its true size and reused."""
    size = 26
    svg = os.path.join(SCENES, f"{name}.svg")
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(DOT_SVG.format(s=size, c=size / 2, inner=size / 5, fill=hex_colour))
    return rasterise(f"{name}.svg", size, size, transparent=True)


def encode(cmd, out, label, frames):
    """Encode to a temp file, verify it, then replace the target atomically."""
    tmp = out + ".tmp.mp4"
    run(cmd + ["-frames:v", str(frames), "-c:v", "libx264", "-preset", "slow",
               "-crf", "18", "-pix_fmt", "yuv420p", tmp], label)
    got = probe_frames(tmp)
    if got != frames:
        raise SystemExit(f"{label}: wrote {got} frames, wanted {frames}")
    os.replace(tmp, out)
    return out


def segment_3d():
    out = os.path.join(OUT, "seg_a.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
           "-i", os.path.join(FRAMES, "v4final_f%04d.png"),
           "-vf", f"scale={W}:{H},setsar=1,format=yuv420p"]
    return encode(cmd, out, "segment A", SEG_A_FRAMES)


def segment_2d(spec):
    bg = rasterise(spec["svg"])
    out = os.path.join(OUT, f"seg_{spec['name'].lower()}.mp4")
    frames = spec["seconds"] * FPS
    kind = spec["motion"][0]

    if kind == "dot":
        dot = make_dot(spec["dot"], f"dot_{spec['dot'].lstrip('#')}")
        y0, y1 = spec["motion"][1], spec["motion"][2]
        yexpr = f"{y0}+(t/{spec['seconds']})*({y1}-{y0})"
        graph = (f"[0:v]scale={W}:{H},setsar=1[bg];"
                 f"[1:v]format=rgba[dot];"
                 f"[bg][dot]overlay=x={(W - 26) // 2}:y='{yexpr}':eval=frame,"
                 f"format=yuv420p[v]")
        inputs = ["-loop", "1", "-framerate", str(FPS), "-i", bg,
                  "-loop", "1", "-framerate", str(FPS), "-i", dot]
    else:
        z = spec["motion"][1]
        graph = (f"[0:v]zoompan=z='min(1.0+{z - 1.0:.4f}*on/{frames}, {z})'"
                 f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                 f":d={frames}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v]")
        inputs = ["-loop", "1", "-framerate", str(FPS), "-i", bg]

    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
           ["-filter_complex", graph, "-map", "[v]"])
    return encode(cmd, out, f"segment {spec['name']}", frames)


def concat(parts, out):
    listing = os.path.join(OUT, "concat.txt")
    with open(listing, "w", encoding="utf-8") as fh:
        for p in parts:
            fh.write("file '" + p.replace("\\", "/") + "'\n")
    tmp = out + ".tmp.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", listing, "-c", "copy", tmp], "concat")
    os.replace(tmp, out)
    return out


def burn(src, srt, out):
    # 11 px at the SRT's 288-unit reference is ~37 px on a 960-tall frame. At 13
    # a two-line caption ran into the diagram; at MarginV 58 it sat over the
    # lower content. 11/30 keeps it in the lower third and clear of the art.
    style = ("FontSize=11,Alignment=2,PrimaryColour=&H00F7EDE6,"
             "OutlineColour=&H00000000,BorderStyle=1,Outline=0,Shadow=0,MarginV=30")
    tmp = out + ".tmp.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.relpath(src, ROOT),
         "-vf", f"subtitles={os.path.relpath(srt, ROOT).replace(chr(92), '/')}"
                f":force_style='{style}'",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp], "burn captions")
    os.replace(tmp, out)
    return out


def probe_frames(path):
    proc = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                "-count_packets", "-show_entries", "stream=nb_read_packets",
                "-of", "csv=p=0", path], "probe frames")
    return int(proc.stdout.strip().splitlines()[0])


def probe_duration(path):
    proc = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", path], "probe duration")
    return float(proc.stdout.strip())


def segment_windows():
    """Absolute start/end of every segment, derived from the same table."""
    wins, t = [], 0.0
    wins.append(("A", 0.0, SEG_A_FRAMES / FPS))
    t = SEG_A_FRAMES / FPS
    for spec in SEGMENTS:
        wins.append((spec["name"], t, t + spec["seconds"]))
        t += spec["seconds"]
    return wins


def srt_cues(path):
    """(start, end, text) for every cue. Enough SRT for this file."""
    cues, block = [], []
    for line in open(path, encoding="utf-8").read().splitlines() + [""]:
        if line.strip():
            block.append(line)
            continue
        if len(block) >= 2 and "-->" in block[1]:
            a, b = block[1].split("-->")
            cues.append((_secs(a), _secs(b), " ".join(block[2:])))
        block = []
    return cues


def _secs(stamp):
    hms, ms = stamp.strip().split(",")
    h, m, s = (int(x) for x in hms.split(":"))
    return h * 3600 + m * 60 + s + int(ms) / 1000.0


def check_captions(path, windows):
    """Every cue must sit wholly inside one segment, else it is mistimed."""
    problems = []
    for start, end, text in srt_cues(path):
        if not any(s <= start and end <= e for _n, s, e in windows):
            problems.append(f"cue {start:.2f}-{end:.2f} crosses a segment boundary: {text}")
        if end <= start:
            problems.append(f"cue has non-positive duration: {text}")
    return problems


def main():
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            raise SystemExit(f"{tool} not on PATH")
    chrome()  # fail before spending an encode on a build that cannot finish
    if not os.path.exists(CAPTIONS):
        raise SystemExit(f"missing captions: {CAPTIONS}")
    os.makedirs(OUT, exist_ok=True)

    windows = segment_windows()
    problems = check_captions(CAPTIONS, windows)
    if problems:
        raise SystemExit("caption timing invalid:\n  " + "\n  ".join(problems))
    print("captions:", len(srt_cues(CAPTIONS)), "cues, all inside segment windows")

    parts = [segment_3d()]
    for spec in SEGMENTS:
        parts.append(segment_2d(spec))
        print(f"built {spec['name']} ({spec['seconds']} s)")

    silent = concat(parts, os.path.join(OUT, "contactless_40s_animatic_silent.mp4"))
    burn(silent, CAPTIONS, OUT_VIDEO)

    frames = probe_frames(OUT_VIDEO)
    duration = probe_duration(OUT_VIDEO)
    expected = SEG_A_FRAMES + sum(s["seconds"] for s in SEGMENTS) * FPS
    if frames != expected or abs(duration - TOTAL_SECONDS) > 0.001:
        raise SystemExit(
            f"contract broken: {frames} frames / {duration:.3f} s, "
            f"wanted {expected} / {TOTAL_SECONDS:.3f}")
    print(f"ANIMATIC {frames} frames, {duration:.3f} s, {W}x{H}, {FPS} fps")


if __name__ == "__main__":
    main()
