"""Validate assets/manifest.json against ADR-0007 provenance rules.

Fails (exit 1) when an asset row lacks source_url, licence or author, when
commercial_ok is not true, when the file is missing, or when its sha256 no
longer matches the recorded hash. Prints one line per problem.

Usage: python tools/check_assets.py [manifest.json]
"""

import hashlib
import json
import os
import sys

REQUIRED = ("path", "source_url", "author", "licence", "retrieved_at", "commercial_ok", "sha256")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(manifest_path):
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)
    problems = []
    rows = data.get("assets", [])
    if not rows:
        problems.append("manifest has no assets")
    for i, row in enumerate(rows):
        name = row.get("path", f"row {i}")
        for field in REQUIRED:
            if not row.get(field):
                problems.append(f"{name}: missing {field}")
        if row.get("commercial_ok") is not True:
            problems.append(f"{name}: commercial_ok is not true")
        if not str(row.get("source_url", "")).startswith("https://"):
            problems.append(f"{name}: source_url is not https")
        path = os.path.join(ROOT, row.get("path", ""))
        if not os.path.isfile(path):
            problems.append(f"{name}: file missing on disk")
        elif row.get("sha256") and sha256(path) != row["sha256"]:
            problems.append(f"{name}: sha256 mismatch")
    total = sum(r.get("bytes", 0) for r in rows)
    if total > 100 * 1024 * 1024:
        problems.append(f"total size {total} exceeds the 100 MB cap")
    for p in problems:
        print("FAIL " + p)
    print(f"assets={len(rows)} total_mb={total / 1e6:.1f} verdict={'FAIL' if problems else 'PASS'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets", "manifest.json")))
