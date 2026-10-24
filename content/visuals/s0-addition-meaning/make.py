"""Diagrams for s0-addition-meaning. Run from repo root.

draw.dot_groups only draws equal groups, so four small helpers live here:
two groups of counters, number-line hops, a row of counters counted from
each end, and ten-frames. Their meta is read back from the shapes drawn,
like draw.py.

Counters in the first group are solid orange ("plain dots" in the text). Counters in the
second group are green with a centre spot in the background colour ("dots with a spot"), so the
two groups differ by shape as well as colour. The landing point of hops is a filled dot, drawn
the same way as in s0-subtraction-meaning.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, MUTED, PAD, POINT, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent
R = 9  # counter radius


def _counter(x, y, kind):
    """kind 'first' = solid orange, 'second' = green with a background-colour centre."""
    if kind == "first":
        return (f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{R}" '
                f'style="fill:{FILL};stroke:{STROKE};stroke-width:1.2"/>')
    return (f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{R}" style="fill:{POINT};stroke:{STROKE};stroke-width:1.2"/>'
            f'<circle cx="{_f(x)}" cy="{_f(y)}" r="3.5" style="fill:{EMPTY}"/>')


# ---------------------------------------------------------------- two groups
def two_groups(a, b, title, labels=False):
    """Two loops side by side. Left loop: a solid orange counters. Right loop: b green
    counters. Counters sit in rows of up to 5, so they are easy to count."""
    gap = 16
    gw = (W - 2 * PAD - gap) / 2
    rows = max(math.ceil(a / 5), math.ceil(b / 5), 1)
    box_h = 20 + rows * 26
    body, counts = [], []
    for g, (n, kind) in enumerate(((a, "first"), (b, "second"))):
        gx = PAD + g * (gw + gap)
        body.append(f'<rect x="{_f(gx)}" y="{PAD}" width="{_f(gw)}" height="{box_h}" rx="14" '
                    f'style="fill:none;stroke:{MUTED};stroke-width:1.5"/>')
        drawn = 0
        for k in range(n):
            row, col = divmod(k, 5)
            in_row = min(5, n - row * 5)
            x = gx + gw / 2 + (col - (in_row - 1) / 2) * 24
            y = PAD + 23 + row * 26
            body.append(_counter(x, y, kind))
            drawn += 1
        counts.append(drawn)
        if labels:
            body.append(_text(gx + gw / 2, PAD + box_h + 24, str(drawn), 16, weight="700"))
    h = PAD + box_h + (34 if labels else 0) + PAD
    meta = {"groups": counts, "total": sum(counts), "labels": [str(c) for c in counts] if labels else []}
    return _svg(h, body, title), meta


# ---------------------------------------------------------------- hops
def hops(lo, hi, start, n, title, show_land=True):
    """Number line lo..hi, every whole number marked and labelled. Dot at start,
    then n hops of 1, each numbered above its arc. Optional dot where they land."""
    body = []
    y = F(PAD + 50)
    m = draw._number_line(y, F(lo), F(hi), 1, "wholes", start, body)
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    unit = (x1 - x0) / (hi - lo)
    arcs = []
    v = F(start)
    for k in range(n):
        a, b = x0 + (v - lo) * unit, x0 + (v + 1 - lo) * unit
        top = y - 34
        body.append(f'<path d="M{_f(a)},{_f(y - 6)} Q{_f((a + b) / 2)},{_f(top)} {_f(b)},{_f(y - 6)}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2"/>')
        dx, dy = float(b - (a + b) / 2), float((y - 6) - top)
        ln = math.hypot(dx, dy)
        ux, uy = dx / ln, dy / ln
        heads = []
        for ang in (0.45, -0.45):
            c, s_ = math.cos(ang), math.sin(ang)
            heads.append((float(b) - 8 * (ux * c - uy * s_), float(y - 6) - 8 * (ux * s_ + uy * c)))
        body.append(f'<path d="M{_f(heads[0][0])},{_f(heads[0][1])} L{_f(b)},{_f(y - 6)} L{_f(heads[1][0])},{_f(heads[1][1])}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2;stroke-linecap:round;stroke-linejoin:round"/>')
        # hop numbers are small and light, so they are not mistaken for number-line labels
        body.append(_text((a + b) / 2, top - 4, str(k + 1), 12, weight="600", color=POINT))
        arcs.append((lo + (a - x0) / unit, lo + (b - x0) / unit))
        v += 1
    meta = {"start": m["start"], "end": m["end"], "spaces_per_unit": m["spaces_per_unit"],
            "labels": m["labels"], "start_point": m["point"], "hops": len(arcs),
            "hop_size": str(arcs[0][1] - arcs[0][0]) if arcs else None,
            "first_hop_lands": str(arcs[0][1]) if arcs else None,
            "lands_at": str(arcs[-1][1]) if arcs else m["point"]}
    if show_land:
        land_x = x0 + (v - lo) * unit
        body.append(f'<circle cx="{_f(land_x)}" cy="{_f(y)}" r="7" style="fill:{FILL};stroke:{STROKE};stroke-width:1.5"/>')
        meta["land_dot"] = str(lo + (land_x - x0) / unit)
    return _svg(float(y) + 50, body, title), meta


# ---------------------------------------------------------------- one row, counted from each end
def _arrow(xa, xb, y):
    """Horizontal arrow from xa to xb."""
    d = 1 if xb > xa else -1
    return (f'<line x1="{_f(xa)}" y1="{_f(y)}" x2="{_f(xb)}" y2="{_f(y)}" style="stroke:{TEXT};stroke-width:2"/>'
            f'<path d="M{_f(xb - d * 8)},{_f(y - 5)} L{_f(xb)},{_f(y)} L{_f(xb - d * 8)},{_f(y + 5)}" '
            f'style="fill:none;stroke:{TEXT};stroke-width:2;stroke-linejoin:round"/>')


def order_row(a, b, title, totals=True):
    """A row of a orange then b green counters. Above: counting 1.. from the left, with an
    arrow to the right labelled 'a + b'. Below: counting 1.. from the right, with an arrow
    to the left labelled 'b + a'."""
    n = a + b
    step = 30
    xs = [W / 2 + (k - (n - 1) / 2) * step for k in range(n)]
    y_lab_top, y_arrow_top, y_num_top = PAD + 12, PAD + 24, PAD + 50
    y_dot = PAD + 70
    y_num_bot, y_arrow_bot, y_lab_bot = PAD + 104, PAD + 118, PAD + 146
    body = []
    kinds = []
    for k, x in enumerate(xs):
        kind = "first" if k < a else "second"
        kinds.append(kind)
        body.append(_counter(x, y_dot, kind))
    left_counts = [str(k + 1) for k in range(n)]
    right_counts = [str(n - k) for k in range(n)]  # numbers under each counter, read right to left
    for x, s in zip(xs, left_counts):
        body.append(_text(x, y_num_top, s, 14, color=MUTED))
    for x, s in zip(xs, right_counts):
        body.append(_text(x, y_num_bot, s, 14, color=MUTED))
    lab_top = f"{a} + {b}" + (f" = {n}" if totals else "")
    lab_bot = f"{b} + {a}" + (f" = {n}" if totals else "")
    body.append(_text(W / 2, y_lab_top, lab_top, 16, weight="700"))
    body.append(_arrow(xs[0] - 4, xs[-1] + 4, y_arrow_top))
    body.append(_arrow(xs[-1] + 4, xs[0] - 4, y_arrow_bot))
    body.append(_text(W / 2, y_lab_bot, lab_bot, 16, weight="700"))
    meta = {"dots": len(xs), "first": kinds.count("first"), "second": kinds.count("second"),
            "left_count_ends_at": left_counts[-1], "right_count_ends_at": right_counts[0],
            "top_label": lab_top, "bottom_label": lab_bot}
    return _svg(y_lab_bot + PAD - 4, body, title), meta


# ---------------------------------------------------------------- ten-frames
def ten_frames(a, b, title):
    """Fill ten-frames (2 rows of 5 boxes) with a orange counters, then b green counters,
    filling each frame before starting the next. Frames sit one above the other."""
    box = 40
    fw = 5 * box
    fx = (W - fw) / 2
    frame_gap = 22
    total = a + b
    n_frames = max(1, math.ceil(total / 10))
    body, metas = [], []
    k = 0
    for f in range(n_frames):
        fy = PAD + f * (2 * box + frame_gap)
        counts = {"first": 0, "second": 0}
        for cell in range(10):
            row, col = divmod(cell, 5)
            x, y = fx + col * box, fy + row * box
            body.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{box}" height="{box}" '
                        f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
            if k < total:
                kind = "first" if k < a else "second"
                counts[kind] += 1
                body.append(_counter(x + box / 2, y + box / 2, kind).replace(f'r="{R}"', 'r="13"', 1))
                k += 1
        filled = counts["first"] + counts["second"]
        metas.append({"boxes": 10, "filled": filled, "empty": 10 - filled,
                      "first": counts["first"], "second": counts["second"]})
    h = PAD * 2 + n_frames * 2 * box + (n_frames - 1) * frame_gap
    return _svg(h, body, title), {"frames": metas, "total": sum(m["filled"] for m in metas)}


# lesson
draw.save(OUT, "am-groups-3-4", *two_groups(3, 4, "A group of 3 and a group of 4", labels=True))
draw.save(OUT, "am-hops-5-3", *hops(0, 10, 5, 3, "Start at 5 and make 3 hops"))
draw.save(OUT, "am-order-3-5", *order_row(3, 5, "3 + 5 and 5 + 3 use the same 8 dots"))
draw.save(OUT, "am-frame-7-5", *ten_frames(7, 5, "7 + 5 on two ten-frames"))
# practice
draw.save(OUT, "am-p1", *two_groups(4, 2, "A group of 4 and a group of 2"))
draw.save(OUT, "am-p2", *hops(0, 10, 6, 3, "Start at 6 and make 3 hops", show_land=False))
draw.save(OUT, "am-p5", *order_row(2, 6, "2 + 6 and 6 + 2", totals=False))
draw.save(OUT, "am-p6", *two_groups(4, 4, "A group of 4 and another group of 4"))
draw.save(OUT, "am-p7", *ten_frames(8, 4, "8 + 4 on two ten-frames"))
# quiz
draw.save(OUT, "am-q1", *two_groups(5, 3, "A group of 5 and a group of 3"))
draw.save(OUT, "am-q4", *ten_frames(9, 5, "9 + 5 on two ten-frames"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-addition-meaning")
