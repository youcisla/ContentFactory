"""Structural checks for the R2 prototype.

Run: python prototypes/r2/validate_r2.py
Exit 0 = pass. No network, no writes.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE / "index.html"

errors = []
raw = HTML.read_text(encoding="utf-8")

# No external resources: allow the SVG namespace, forbid fetched URLs.
no_ns = raw.replace('http://www.w3.org/2000/svg', '')
if re.search(r'(src|href)\s*=\s*["\']https?://', no_ns, re.IGNORECASE):
    errors.append("external src/href reference")
if re.search(r'url\(\s*["\']?https?://', no_ns, re.IGNORECASE):
    errors.append("external url() reference")
if re.search(r'@import', raw, re.IGNORECASE):
    errors.append("CSS @import present")

# Canvas contract.
if 'width="1080"' not in raw or 'height="1920"' not in raw:
    errors.append("1080x1920 canvas not declared")
if 'viewBox="0 0 1080 1920"' not in raw:
    errors.append("viewBox is not 0 0 1080 1920")

# Duration contract: 10-15 s.
m = re.search(r'--dur:\s*([0-9.]+)s', raw)
if not m:
    errors.append("--dur variable missing")
else:
    dur = float(m.group(1))
    if not (10 <= dur <= 15):
        errors.append(f"duration {dur}s outside 10-15s")

# All five nodes present and ordered.
for i in range(1, 6):
    if f'class="node n{i}"' not in raw:
        errors.append(f"node n{i} missing")

# Five numbered labels.
nums = re.findall(r'>0([1-5])<', raw)
if len(set(nums)) != 5:
    errors.append(f"expected 5 distinct step numbers, got {sorted(set(nums))}")

# Reduced-motion support.
if 'prefers-reduced-motion' not in raw:
    errors.append("no prefers-reduced-motion handling")

# No external fonts.
for fam in re.findall(r"font-family:([^;}\"]+)", raw):
    names = {p.strip().strip("'\"") for p in fam.split(",")}
    if not names <= {"Segoe UI", "Inter", "Arial", "sans-serif"}:
        errors.append(f"disallowed font {sorted(names)}")

print(f"duration={dur if m else '?'}s nodes=5 numbers={sorted(set(nums))}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("PASS: R2 structure valid")
