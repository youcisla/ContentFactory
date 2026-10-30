"""Deterministic structural checks for the R1 SVG frames.

Run: python prototypes/r1/validate_r1.py
Exit code 0 = all checks passed. Non-zero = failure list printed.
Reads only files in this directory. No network, no writes.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRAMES = ["frame-01-hook.svg", "frame-02-process.svg", "frame-03-takeaway.svg"]

ALLOWED_FONTS = {"Segoe UI", "Inter", "Arial", "sans-serif"}
PALETTE = {
    "#0B1020", "#121A2B", "#22304A", "#E6EDF7",
    "#9FB0C7", "#4C8DFF", "#22D3EE", "#F5B547",
}
SAFE_TOP = 230
SAFE_BOTTOM = 1574
MIN_FONT_PX = 26

errors = []


def local(tag):
    return tag.split("}", 1)[-1]


for name in FRAMES:
    path = HERE / name
    if not path.exists():
        errors.append(f"{name}: missing")
        continue

    raw = path.read_text(encoding="utf-8")

    # No external references of any kind. The SVG namespace URI is not a fetch.
    no_ns = raw.replace('xmlns="http://www.w3.org/2000/svg"', "")
    if re.search(r"(href|src)\s*=\s*[\"']https?://", no_ns, re.IGNORECASE):
        errors.append(f"{name}: contains an external href/src reference")
    if re.search(r"url\(\s*[\"']?https?://", no_ns, re.IGNORECASE):
        errors.append(f"{name}: contains an external url() reference")
    if re.search(r"@import", no_ns, re.IGNORECASE):
        errors.append(f"{name}: contains a CSS @import")

    # Reject DTDs/entities before parsing: blocks XXE and billion-laughs.
    # (defusedxml is not installed and this phase forbids installs.)
    if re.search(r"<!(DOCTYPE|ENTITY)", raw, re.IGNORECASE):
        errors.append(f"{name}: DTD or entity declaration is not allowed")
        continue

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"{name}: XML parse error: {exc}")
        continue

    if root.get("viewBox") != "0 0 1080 1920":
        errors.append(f"{name}: viewBox is {root.get('viewBox')!r}")

    text_count = 0
    for el in root.iter():
        tag = local(el.tag)

        if tag == "text":
            text_count += 1
            y = el.get("y")
            if y is None:
                errors.append(f"{name}: <text> without y: {el.text!r}")
            else:
                try:
                    yv = float(y)
                except ValueError:
                    errors.append(f"{name}: non-numeric y={y!r}")
                else:
                    if not (SAFE_TOP <= yv <= SAFE_BOTTOM):
                        errors.append(
                            f"{name}: text baseline y={yv} outside safe area "
                            f"[{SAFE_TOP},{SAFE_BOTTOM}] -> {el.text!r}"
                        )

        if tag in ("image", "use"):
            errors.append(f"{name}: {tag} element is not allowed")

    # Fonts: every font-family declaration must use the system stack only.
    for fam in re.findall(r"font-family:([^;}\"]+)", raw):
        names = {p.strip().strip("'\"") for p in fam.split(",")}
        if not names <= ALLOWED_FONTS:
            errors.append(f"{name}: disallowed font {sorted(names - ALLOWED_FONTS)}")

    # Colours: every hex colour must be in the palette.
    for colour in set(re.findall(r"#[0-9A-Fa-f]{6}", raw)):
        if colour.upper() not in PALETTE:
            errors.append(f"{name}: off-palette colour {colour}")

    # Minimum font size.
    for size in re.findall(r"font-size:(\d+)px", raw):
        if int(size) < MIN_FONT_PX:
            errors.append(f"{name}: font-size {size}px below {MIN_FONT_PX}px")

    print(f"{name}: text elements={text_count}")

if errors:
    print("\nFAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("\nPASS: 3 frames, structure and design tokens valid")
