"""ContentFactory shared render QA.

Imported by the Blender scene scripts. Runs inside Blender's Python, which
already bundles numpy — no external dependency is added.

Two different questions, deliberately kept apart:

  frame_gate   - is this one frame inside its exposure window?
  seq_verdict  - is the sequence as a whole acceptable?

The earlier scripts reported both under a single `gate` field, which meant a
sequence's quality was judged by whichever frame happened to be rendered last.
That is the defect this module exists to remove.
"""

import os

import numpy as np

# Per-shot threshold sets. A product still and a bright diagram do not share an
# exposure window; forcing them to would either pass a black frame or fail a
# legitimately bright one.
SHOT_THRESHOLDS = {
    "product_still": {"mean_min": 0.040, "mean_max": 0.400, "p99_min": 0.70},
    "product_motion": {"mean_min": 0.040, "mean_max": 0.400, "p99_min": 0.60},
    "diagram": {"mean_min": 0.050, "mean_max": 0.600, "p99_min": 0.55},
}
DEFAULT_SHOT = "product_still"

# Sequence limits. Drift is measured against an expected curve when one is
# supplied; without one, any departure beyond this from frame 1 is a failure.
DRIFT_MAX = 0.05
FLICKER_MAX = 0.01

# Band for a shot that is *supposed* to change exposure, checked against a
# declared curve rather than against frame 1. A dolly-in must brighten: the
# inverse-square term is arithmetic, not drift, so the 5 % orbit criterion would
# reject a correct shot. This band is calibrated, not derived — the AgX view
# transform compresses a 48 % scene-linear rise to roughly 25-35 % measured at
# this exposure, and 0.25 is the tightest value that does not reject a correct
# dolly. It still catches a frame lost to a light swap or a black metal chip.
# It applies only when a curve is supplied, so orbit runs keep the 5 % rule.
CURVE_MAX = 0.25


def thresholds(shot):
    return SHOT_THRESHOLDS.get(shot, SHOT_THRESHOLDS[DEFAULT_SHOT])


def _load_rgb(path):
    import bpy

    img = bpy.data.images.load(path, check_existing=False)
    buf = np.empty(len(img.pixels), dtype=np.float32)
    img.pixels.foreach_get(buf)
    w, h = img.size
    rgb = buf.reshape(h, w, 4)[:, :, :3]
    return rgb[::-1]  # Blender stores bottom-up; flip to top-down


def _luma(rgb):
    return rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def measure(path, shot=DEFAULT_SHOT):
    """Whole-frame exposure statistics."""
    lum = _luma(_load_rgb(path))
    t = thresholds(shot)
    mean = float(lum.mean())
    p99 = float(np.percentile(lum, 99))
    problems = []
    if not t["mean_min"] <= mean <= t["mean_max"]:
        problems.append(f"mean {mean:.4f} outside [{t['mean_min']}, {t['mean_max']}]")
    if p99 < t["p99_min"]:
        problems.append(f"p99 {p99:.4f} below {t['p99_min']} - no highlights")
    return {
        "mean": mean,
        "p95": float(np.percentile(lum, 95)),
        "p99": p99,
        "dark_fraction": float((lum < 0.01).mean()),
        "frame_gate": "PASS" if not problems else "FAIL",
        "frame_gate_reason": "; ".join(problems) or "ok",
    }


def measure_rect(path, rect):
    """Mean and p99 luminance inside (x, y, w, h), top-left origin."""
    x, y, w, h = [int(v) for v in rect]
    rgb = _load_rgb(path)
    h_img, w_img = rgb.shape[:2]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, w_img), min(y + h, h_img)
    if x1 <= x0 or y1 <= y0:
        return {"mean": float("nan"), "p99": float("nan"), "empty": True}
    lum = _luma(rgb[y0:y1, x0:x1])
    return {
        "mean": float(lum.mean()),
        # Median is far less sensitive to how much subject has grown into the
        # rectangle, which is what breaks fixed rects on a dolly.
        "median": float(np.median(lum)),
        "p99": float(np.percentile(lum, 99)),
        "empty": False,
    }


def series_metrics(values):
    """Drift and flicker for one luminance series."""
    if len(values) < 3:
        return None
    base = values[0]
    mean_v = sum(values) / len(values)
    d2 = [values[i] - 2 * values[i - 1] + values[i - 2] for i in range(2, len(values))]
    return {
        "first": values[0],
        "last": values[-1],
        "min": min(values),
        "max": max(values),
        "max_deviation": max(abs(v - base) / base for v in values),
        "drift": (values[-1] - base) / base,
        # Mean |second difference| normalised. A smooth ramp has near-zero
        # curvature; flicker does not. This is the measure SSIM cannot give.
        "flicker_index": (sum(abs(v) for v in d2) / len(d2)) / mean_v,
    }


def expected_curve_error(values, curve):
    """Max relative error against a declared curve, or None if not comparable.

    Supplying an expected curve is what makes an intentional lighting change
    checkable instead of merely waived.

    Both series are normalised to their first value first. A predicted curve
    comes from scene geometry and has no absolute luminance units, and the
    quantity that matters is the shape of the change, not its offset.
    """
    if not curve or len(curve) != len(values) or not values or not curve:
        return None
    if values[0] <= 0 or curve[0] <= 0:
        return None
    errs = []
    for got, want in zip(values, curve):
        w = want / curve[0]
        if w <= 0:
            continue
        errs.append(abs((got / values[0]) - w) / w)
    return max(errs) if errs else None


def sequence_qa(frame_paths, shot="product_motion", regions=None, expected=None,
                region_expected=None):
    """Whole-frame and per-region temporal analysis.

    regions: {name: rect} in pixels. Rect validity is the caller's problem —
    report the objects' screen positions alongside so a reader can confirm the
    rectangles actually enclosed the subject.

    expected: declared luminance curve for the whole frame, one value per frame.
    region_expected: {name: curve} for the same, per region. Without a curve the
    criterion is the 5 % orbit rule; with one it is agreement with the declared
    curve, because a dolly is meant to change exposure.
    """
    lums = [measure(p, shot)["mean"] for p in frame_paths]
    out = {"frames": len(frame_paths), "whole": series_metrics(lums) or {}}

    problems = []
    whole = out["whole"]
    if whole:
        dev = whole["max_deviation"]
        if expected:
            err = expected_curve_error(lums, expected)
            out["expected_curve_error"] = err
            if err is not None and err > CURVE_MAX:
                problems.append(
                    f"deviates from expected curve by {err * 100:.1f}% > {CURVE_MAX * 100:.0f}%"
                )
        elif dev > DRIFT_MAX:
            problems.append(
                f"unplotted exposure deviation {dev * 100:.1f}% > {DRIFT_MAX * 100:.0f}%"
            )
        if whole["flicker_index"] > FLICKER_MAX:
            problems.append(f"flicker index {whole['flicker_index']:.5f} > {FLICKER_MAX}")

    if regions:
        out["regions"] = {}
        for name, rect in regions.items():
            # rect may be one static rect, or one rect per frame. Per-frame
            # rects follow the object, so a dolly-in no longer reads as drift.
            tracked = isinstance(rect, list) and rect and isinstance(rect[0], (list, tuple))
            series = []
            for i, p in enumerate(frame_paths):
                r = rect[i] if tracked and i < len(rect) else (rect if not tracked else None)
                if r is None:
                    continue
                series.append(measure_rect(p, r)["median"])
            series = [v for v in series if v == v]  # drop NaN
            m = series_metrics(series)
            if m:
                out["regions"][name] = m
                curve = (region_expected or {}).get(name)
                err = expected_curve_error(series, curve) if curve else None
                if err is not None:
                    m["expected_error"] = err
                    if err > CURVE_MAX:
                        problems.append(
                            f"region '{name}' deviates from expected curve by {err * 100:.1f}%"
                        )
                elif m["max_deviation"] > DRIFT_MAX:
                    problems.append(
                        f"region '{name}' deviates {m['max_deviation'] * 100:.1f}%"
                    )

    out["seq_verdict"] = "PASS" if not problems else " | ".join(problems)
    return out


def write_report(path, lines):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def report_dir(script_file):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(script_file))),
                        "tools", "blender-test")
