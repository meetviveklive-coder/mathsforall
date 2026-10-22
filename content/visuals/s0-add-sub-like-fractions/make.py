"""Diagrams for s0-add-sub-like-fractions. Run from repo root.

Uses tools/draw.py where it fits (bars). Three small helpers live here:
two-colour bar (adding), take-away bar (subtracting) and number-line jumps.
Their meta is read back from the shapes drawn, like draw.py.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, PAD, POINT, STROKE, TEXT, W, _f, _frac_label, _svg  # noqa: E402

OUT = Path(__file__).resolve().parent
BAR_H = 40


def _bar_cells(parts):
    x0, x1 = F(PAD), F(W - PAD)
    w = (x1 - x0) / parts
    return [(x0 + k * w, w) for k in range(parts)]


def two_colour_bar(parts, first, second, title):
    """One bar: `first` parts in FILL, the next `second` parts in POINT, rest empty.
    A fraction label sits under each coloured group."""
    y = PAD
    body, kinds, widths = [], [], []
    cells = _bar_cells(parts)
    for k, (x, w) in enumerate(cells):
        kind = "first" if k < first else "second" if k < first + second else "empty"
        colour = {"first": FILL, "second": POINT, "empty": EMPTY}[kind]
        body.append(f'<rect x="{_f(x)}" y="{y}" width="{_f(w)}" height="{BAR_H}" '
                    f'style="fill:{colour};stroke:{STROKE};stroke-width:1.5"/>')
        kinds.append(kind)
        widths.append(w)
    groups = []
    for kind, n in (("first", first), ("second", second)):
        idx = [k for k, kd in enumerate(kinds) if kd == kind]
        if not idx:
            continue
        gx0 = cells[idx[0]][0]
        gx1 = cells[idx[-1]][0] + cells[idx[-1]][1]
        yb = y + BAR_H + 8
        body.append(f'<path d="M{_f(gx0 + 3)},{yb} L{_f(gx0 + 3)},{yb + 6} L{_f(gx1 - 3)},{yb + 6} L{_f(gx1 - 3)},{yb}" '
                    f'style="fill:none;stroke:{TEXT};stroke-width:1.5"/>')
        body.append(_frac_label((gx0 + gx1) / 2, yb + 24, len(idx), parts, 14))
        groups.append(f"{len(idx)}/{parts}")
    meta = {"parts": len(widths), "equal": len(set(widths)) == 1,
            "first": kinds.count("first"), "second": kinds.count("second"),
            "coloured": kinds.count("first") + kinds.count("second"), "group_labels": groups}
    return _svg(y + BAR_H + 8 + 6 + 50, body, title), meta


def take_away_bar(parts, shaded, crossed, title):
    """One bar with `shaded` parts filled; the last `crossed` filled parts get an X (taken away)."""
    y = PAD
    body, widths = [], []
    n_shaded = n_crossed = 0
    for k, (x, w) in enumerate(_bar_cells(parts)):
        is_shaded = k < shaded
        is_crossed = shaded - crossed <= k < shaded
        body.append(f'<rect x="{_f(x)}" y="{y}" width="{_f(w)}" height="{BAR_H}" '
                    f'style="fill:{FILL if is_shaded else EMPTY};stroke:{STROKE};stroke-width:1.5"/>')
        if is_crossed:
            m = 6
            for (ax, ay, bx, by) in ((x + m, y + m, x + w - m, y + BAR_H - m), (x + w - m, y + m, x + m, y + BAR_H - m)):
                body.append(f'<line x1="{_f(ax)}" y1="{_f(ay)}" x2="{_f(bx)}" y2="{_f(by)}" '
                            f'style="stroke:{STROKE};stroke-width:3;stroke-linecap:round"/>')
        n_shaded += is_shaded
        n_crossed += is_crossed
        widths.append(w)
    meta = {"parts": len(widths), "equal": len(set(widths)) == 1, "shaded": n_shaded,
            "crossed": n_crossed, "left": n_shaded - n_crossed}
    return _svg(y + BAR_H + PAD, body, title), meta


def jumps(end, spu, start_point, n_jumps, title, labels="wholes"):
    """Number line 0..end with spu spaces per unit. Dot at start_point, then n_jumps arcs
    of one step each, and a second dot where the last jump lands."""
    body = []
    y = F(PAD + 40)
    m = draw._number_line(y, F(0), F(end), spu, labels, start_point, body)
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    unit = (x1 - x0) / end
    step = F(1, spu)
    arcs = []
    v = F(start_point)
    for _ in range(n_jumps):
        a, b = x0 + v * unit, x0 + (v + step) * unit
        body.append(f'<path d="M{_f(a)},{_f(y - 6)} Q{_f((a + b) / 2)},{_f(y - 34)} {_f(b)},{_f(y - 6)}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2"/>')
        # arrowhead: two short strokes back along the curve's end direction (control -> end)
        dx, dy = float(b - (a + b) / 2), float((y - 6) - (y - 34))
        ln = math.hypot(dx, dy)
        ux, uy = dx / ln, dy / ln
        heads = []
        for ang in (0.45, -0.45):
            c, s_ = math.cos(ang), math.sin(ang)
            heads.append((float(b) - 9 * (ux * c - uy * s_), float(y - 6) - 9 * (ux * s_ + uy * c)))
        body.append(f'<path d="M{_f(heads[0][0])},{_f(heads[0][1])} L{_f(b)},{_f(y - 6)} L{_f(heads[1][0])},{_f(heads[1][1])}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2;stroke-linecap:round;stroke-linejoin:round"/>')
        arcs.append([str((a - x0) / unit), str((b - x0) / unit)])  # read back from pixels
        v += step
    land_x = x0 + v * unit
    body.append(f'<circle cx="{_f(land_x)}" cy="{_f(y)}" r="7" style="fill:{FILL};stroke:{STROKE};stroke-width:1.5"/>')
    meta = {"start": m["start"], "end": m["end"], "spaces_per_unit": m["spaces_per_unit"],
            "labels": m["labels"], "start_point": m["point"], "jumps": len(arcs),
            "jump_size": str(F(arcs[0][1]) - F(arcs[0][0])) if arcs else None,
            "lands_at": str((land_x - x0) / unit)}
    tall = 50 if labels == "wholes" else 56
    return _svg(float(y) + tall, body, title), meta


draw.save(OUT, "al-add-bar", *two_colour_bar(5, 1, 2, "One fifth and two fifths make three fifths"))
draw.save(OUT, "al-nl-jumps", *jumps(2, 4, F(3, 4), 2, "Start at three quarters and jump two quarters", labels="all"))
draw.save(OUT, "al-take-away", *take_away_bar(6, 5, 2, "Five sixths, take away two sixths"))
draw.save(OUT, "al-over-one", *draw.bars([
    {"weights": [1] * 4, "shaded": [0, 1, 2, 3], "label": "1"},
    {"weights": [1] * 4, "shaded": [0], "label": "1/4"},
], "Five quarters fill one whole bar and one quarter of another"))
draw.save(OUT, "al-p1", *jumps(1, 6, F(1, 6), 4, "Start at one sixth and jump four sixths"))
draw.save(OUT, "al-q6", *take_away_bar(7, 6, 4, "Six sevenths, take away four sevenths"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-add-sub-like-fractions")
