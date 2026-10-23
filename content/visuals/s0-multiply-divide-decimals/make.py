"""Diagrams for s0-multiply-divide-decimals. Run from repo root.

Adds three helpers (kept here, not in tools/draw.py):
- shift_chart: a place-value chart with a number in the top row and the same number
  times (or divided by) 10, 100 or 1,000 in the bottom row. Arrows show each digit
  moving to its new place. The decimal point column stays fixed.
- decimal_area: a 10 x 10 grid used as an area model for tenths times tenths.
- hops_line: a number line in tenths with equal hops drawn above it.

They follow draw.py's rule: every digit, arrow, cell and hop is first placed as a
record with its position, the SVG is written from those records, and the meta is
read back from the same records. Nothing in the meta is copied from the request.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, MUTED, PAD, POINT, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

PLACE_NAMES = {3: "Thousands", 2: "Hundreds", 1: "Tens", 0: "Ones",
               -1: "Tenths", -2: "Hundredths", -3: "Thousandths"}
DIGIT_SIZE = 22
POINT_W = 16
LABEL_W = 64


def _dec(value: F) -> str:
    """Write a fraction whose denominator is 1, 10, 100 or 1000 as a decimal string."""
    for places in range(0, 4):
        n = value * 10 ** places
        if n.denominator == 1:
            if places == 0:
                return str(n.numerator)
            whole, frac = divmod(int(n), 10 ** places)
            return f"{whole}.{frac:0{places}d}"
    raise ValueError(value)


def _digits_by_place(s: str) -> dict[int, str]:
    ip, dp = (s.split(".") + [""])[:2] if "." in s else (s, "")
    out = {}
    for k, ch in enumerate(reversed(ip)):
        out[k] = ch
    for k, ch in enumerate(dp):
        out[-(k + 1)] = ch
    return out


# ---------------------------------------------------------------- place-value shift chart
def shift_chart(top: str, power: int, title: str) -> tuple[str, dict]:
    """Top row: `top`. Bottom row: top x 10**power (power < 0 divides).

    Only the significant digits move (leading zeros of the top row stay behind).
    In the bottom row, any empty place between the leftmost digit and the ones place,
    or between the ones place and the rightmost digit, is drawn as a filled-in 0.
    """
    top_d = _digits_by_place(top)
    sig = {p: d for p, d in top_d.items()}
    while sig and max(sig) > 0 and sig[max(sig)] == "0":
        del sig[max(sig)]
    bot_d = {p + power: d for p, d in sig.items()}
    lo, hi = min(min(bot_d), 0), max(max(bot_d), 0)
    filled = {p for p in range(lo, hi + 1) if p not in bot_d}
    for p in filled:
        bot_d[p] = "0"
    places = sorted(set(top_d) | set(bot_d) | {0, -1}, reverse=True)
    widths = {p: max(46, len(PLACE_NAMES[p]) * 8 + 6) for p in places}
    total = LABEL_W + sum(widths.values()) + POINT_W
    x = F(W - total, 2) + LABEL_W
    centre = {}
    for p in places:
        if p == -1:
            point_x = x + F(POINT_W, 2)
            x += POINT_W
        centre[p] = x + F(widths[p], 2)
        x += widths[p]
    right_edge = x
    y_head = F(PAD + 12)
    y_rows = [F(PAD + 58), F(PAD + 150)]
    body: list[str] = []
    guide_top, guide_bot = F(PAD + 22), y_rows[1] + 14
    for p in places:
        gx0 = centre[p] - F(widths[p], 2) + 3
        body.append(f'<rect x="{_f(gx0)}" y="{_f(guide_top)}" width="{_f(widths[p] - 6)}" '
                    f'height="{_f(guide_bot - guide_top)}" rx="6" '
                    f'style="fill:none;stroke:{MUTED};stroke-width:1;stroke-dasharray:3 4"/>')
        body.append(_text(centre[p], y_head, PLACE_NAMES[p], 14, weight="600"))
    recs = []  # {"row", "x", "ch", "filled"}
    for i, digits in enumerate((top_d, bot_d)):
        for p, ch in digits.items():
            recs.append({"row": i, "x": centre[p], "ch": ch, "filled": i == 1 and p in filled})
        recs.append({"row": i, "x": point_x, "ch": ".", "filled": False})
    arrows = []  # {"x0", "x1"}
    for p in sig:
        arrows.append({"x0": centre[p], "x1": centre[p + power]})
    # draw digits and points
    for c in recs:
        y = y_rows[c["row"]]
        if c["ch"] == ".":
            body.append(f'<circle cx="{_f(c["x"])}" cy="{_f(y - 2)}" r="3.4" style="fill:{TEXT}"/>')
            continue
        if c["filled"]:
            body.append(f'<rect x="{_f(c["x"] - 12)}" y="{_f(y - DIGIT_SIZE + 1)}" width="24" '
                        f'height="{DIGIT_SIZE + 6}" rx="5" style="fill:none;stroke:{POINT};stroke-width:1.6;'
                        f'stroke-dasharray:4 3"/>')
        body.append(_text(c["x"], y, c["ch"], DIGIT_SIZE, weight="600",
                          color=POINT if c["filled"] else TEXT))
    # draw arrows from each moving digit to its new place
    ya, yb = y_rows[0] + 12, y_rows[1] - DIGIT_SIZE - 6
    for a in arrows:
        x0, x1 = a["x0"], a["x1"]
        body.append(f'<line x1="{_f(x0)}" y1="{_f(ya)}" x2="{_f(x1)}" y2="{_f(yb)}" '
                    f'style="stroke:{POINT};stroke-width:2"/>')
        # arrowhead: a small triangle pointing along the line
        dx, dy = float(x1 - x0), float(yb - ya)
        ln = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / ln, dy / ln
        bx, by = float(x1) - ux * 10, float(yb) - uy * 10
        p1 = (bx - uy * 5, by + ux * 5)
        p2 = (bx + uy * 5, by - ux * 5)
        body.append(f'<path d="M{_f(x1)},{_f(yb)} L{_f(p1[0])},{_f(p1[1])} L{_f(p2[0])},{_f(p2[1])} Z" '
                    f'style="fill:{POINT}"/>')
    op_label = (f"× {10 ** power:,}" if power > 0 else f"÷ {10 ** -power:,}")
    body.append(_text(F(W - total, 2) + LABEL_W / 2, (y_rows[0] + y_rows[1]) / 2 + 2, op_label, 18,
                      weight="700", color=POINT))

    # ---- meta, read back from the drawn records
    xs_to_place = {centre[p]: p for p in places}
    headings = [PLACE_NAMES[p] for p in places]
    rows_meta = []
    for i in range(2):
        cells = {xs_to_place[c["x"]]: c["ch"] for c in recs if c["row"] == i and c["ch"] != "."}
        value = sum(F(int(d)) * F(10) ** p for p, d in cells.items())
        rows_meta.append({"digits": [cells.get(p, "") for p in places], "value": _dec(value)})
    point_xs = {c["x"] for c in recs if c["ch"] == "."}
    shifts = {xs_to_place[a["x1"]] - xs_to_place[a["x0"]] for a in arrows}
    shift = shifts.pop() if len(shifts) == 1 else None
    ratio = F(rows_meta[1]["value"]) / F(rows_meta[0]["value"])
    meta = {
        "headings": headings,
        "rows": rows_meta,
        "point_fixed": len(point_xs) == 1,
        "arrows": len(arrows),
        "shift": {"places": abs(shift), "direction": "left" if shift > 0 else "right"} if shift else None,
        "ratio": str(ratio),
        "filled_zeros": sum(1 for c in recs if c["filled"]),
        "label": op_label,
    }
    height = guide_bot + PAD
    return _svg(height, body, title), meta


# ---------------------------------------------------------------- 10 x 10 area model
LIGHT_OPACITY = "0.32"


def decimal_area(cols: int, rows: int, title: str) -> tuple[str, dict]:
    """10 x 10 grid. The first `cols` columns and the top `rows` rows get a light tint.

    Cells in both are dark: that overlap is (cols/10) x (rows/10).
    Labels: cols/10 as a decimal above the shaded columns, rows/10 left of the shaded rows.
    """
    side = F(200)
    cell = side / 10
    label_w, label_h = 44, 30
    x0 = PAD + label_w + (W - 2 * PAD - label_w - side) / 2
    y0 = F(PAD + label_h)
    cells = []  # {"c", "r", "x", "y", "kind"}
    for r in range(10):
        for c in range(10):
            in_c, in_r = c < cols, r < rows
            kind = "dark" if in_c and in_r else ("light" if in_c or in_r else "empty")
            cells.append({"c": c, "r": r, "x": x0 + c * cell, "y": y0 + r * cell, "kind": kind})
    body = []
    for k in cells:
        style = {"dark": f"fill:{FILL}", "light": f"fill:{FILL};fill-opacity:{LIGHT_OPACITY}",
                 "empty": f"fill:{EMPTY}"}[k["kind"]]
        body.append(f'<rect x="{_f(k["x"])}" y="{_f(k["y"])}" width="{_f(cell)}" height="{_f(cell)}" '
                    f'style="{style};stroke:{STROKE};stroke-width:1"/>')
    body.append(f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(side)}" height="{_f(side)}" '
                f'style="fill:none;stroke:{STROKE};stroke-width:2.5"/>')
    # bracket and label above the shaded columns
    bx0, bx1, by = x0, x0 + cols * cell, y0 - 6
    body.append(f'<path d="M{_f(bx0)},{_f(by + 4)} L{_f(bx0)},{_f(by)} L{_f(bx1)},{_f(by)} L{_f(bx1)},{_f(by + 4)}" '
                f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
    top_label = _dec(F(cols, 10))
    body.append(_text((bx0 + bx1) / 2, by - 6, top_label, 15, weight="700"))
    # bracket and label left of the shaded rows
    lx, ly0, ly1 = x0 - 6, y0, y0 + rows * cell
    body.append(f'<path d="M{_f(lx + 4)},{_f(ly0)} L{_f(lx)},{_f(ly0)} L{_f(lx)},{_f(ly1)} L{_f(lx + 4)},{_f(ly1)}" '
                f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
    left_label = _dec(F(rows, 10))
    body.append(_text(lx - 6, (ly0 + ly1) / 2 + 5, left_label, 15, anchor="end", weight="700"))

    # ---- meta, read back from the drawn cells
    xs = sorted({k["x"] for k in cells})
    ys = sorted({k["y"] for k in cells})
    dark = [k for k in cells if k["kind"] == "dark"]
    lit_cols = {k["x"] for k in cells if k["kind"] != "empty"
                and all(j["kind"] != "empty" for j in cells if j["x"] == k["x"])}
    lit_rows = {k["y"] for k in cells if k["kind"] != "empty"
                and all(j["kind"] != "empty" for j in cells if j["y"] == k["y"])}
    meta = {
        "columns": len(xs), "rows": len(ys), "cells": len(cells), "equal": True,
        "shaded_columns": len(lit_cols), "shaded_rows": len(lit_rows),
        "dark": len(dark), "light": sum(1 for k in cells if k["kind"] == "light"),
        "dark_block": [len({k["x"] for k in dark}), len({k["y"] for k in dark})],
        "dark_decimal": _dec(F(len(dark), len(cells))),
        "labels": {"top": top_label, "left": left_label},
    }
    return _svg(y0 + side + PAD, body, title), meta


# ---------------------------------------------------------------- hops on a tenths line
def hops_line(end_tenths: int, hop_tenths: int, title: str) -> tuple[str, dict]:
    """0 to end_tenths/10, one tick per tenth. Hops of hop_tenths/10 from 0, numbered above."""
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    step = (x1 - x0) / end_tenths
    y = F(PAD + 62)
    body = [f'<line x1="{_f(x0)}" y1="{_f(y)}" x2="{_f(x1)}" y2="{_f(y)}" style="stroke:{STROKE};stroke-width:2"/>']
    ticks = [x0 + k * step for k in range(end_tenths + 1)]
    for k, tx in enumerate(ticks):
        h = 10 if k in (0, end_tenths) else 6
        body.append(f'<line x1="{_f(tx)}" y1="{_f(y - h)}" x2="{_f(tx)}" y2="{_f(y + h)}" '
                    f'style="stroke:{STROKE};stroke-width:{2 if h == 10 else 1.5}"/>')
    hops = []
    k = 0
    while k + hop_tenths <= end_tenths:
        hops.append((ticks[k], ticks[k + hop_tenths]))
        k += hop_tenths
    labels = []
    lab_xs = [hops[0][0]] + [b for _, b in hops]
    for lx in lab_xs:
        v = (lx - x0) / step / 10
        lab = _dec(v)
        labels.append(lab)
        body.append(_text(lx, y + 30, lab, 14, weight="600"))
    for n, (a, b) in enumerate(hops, start=1):
        mid = (a + b) / 2
        body.append(f'<path d="M{_f(a)},{_f(y - 4)} Q{_f(mid)},{_f(y - 46)} {_f(b)},{_f(y - 4)}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2.2"/>')
        body.append(_text(mid, y - 30, str(n), 14, weight="700", color=POINT))
    gaps = {ticks[i + 1] - ticks[i] for i in range(len(ticks) - 1)}
    lengths = {(b - a) / step / 10 for a, b in hops}
    meta = {
        "start": "0", "end": str((x1 - x0) / step / 10),
        "spaces": len(ticks) - 1 if len(gaps) == 1 else None,
        "hops": len(hops),
        "hop_length": str(lengths.pop()) if len(lengths) == 1 else None,
        "last_hop_ends_at": str((hops[-1][1] - x0) / step / 10),
        "labels": labels,
    }
    return _svg(y + 44, body, title), meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "md-x10", *shift_chart("3.45", 1, "3.45 times 10: each digit moves one place left"))
draw.save(OUT, "md-div100", *shift_chart("7", -2, "7 divided by 100: the 7 moves two places right"))
draw.save(OUT, "md-grid", *decimal_area(3, 4, "Area model for 0.3 times 0.4 on a hundred grid"))
draw.save(OUT, "md-hops", *hops_line(12, 3, "Hops of 0.3 from 0 to 1.2"))
draw.save(OUT, "md-p5", *decimal_area(7, 2, "Area model for 0.7 times 0.2 on a hundred grid"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-multiply-divide-decimals")
