"""Diagrams for s0-decimals-meaning. Run from repo root.

Adds three helpers (kept here, not in tools/draw.py):
- tenths_line: a 0-to-1 number line in tenths, fractions above the marks and decimals below.
- hundred_grids: one or more 10 x 10 grids with some cells shaded, filled column by column.
- place_chart: a place-value chart (Ones . Tenths Hundredths Thousandths) with digits.

They follow draw.py's rule: the meta is read back from what was actually drawn.
The grid meta is parsed from the finished SVG text, not copied from the request.
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, PAD, POINT, STROKE, TEXT, W, _f, _frac_label, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent


def _dec(value: F) -> str:
    """Write a fraction with denominator 10, 100 or 1000 as a decimal string ('0.3', '1')."""
    for places in range(0, 4):
        if (value * 10 ** places).denominator == 1:
            if places == 0:
                return str(value.numerator)
            n = value * 10 ** places
            whole, frac = divmod(int(n), 10 ** places)
            return f"{whole}.{frac:0{places}d}"
    raise ValueError(value)


# ---------------------------------------------------------------- tenths number line
def tenths_line(title: str) -> tuple[str, dict]:
    """0 to 1 in 10 equal spaces. Fractions 1/10..9/10 above the marks, decimals 0..1 below."""
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    y = F(PAD + 48)
    body = [f'<line x1="{_f(x0)}" y1="{_f(y)}" x2="{_f(x1)}" y2="{_f(y)}" style="stroke:{STROKE};stroke-width:2"/>']
    tick_xs, top, bottom = [], [], []
    for k in range(11):
        value = F(k, 10)
        x = x0 + (x1 - x0) * value
        whole = value.denominator == 1
        h = 10 if whole else 7
        body.append(f'<line x1="{_f(x)}" y1="{_f(y - h)}" x2="{_f(x)}" y2="{_f(y + h)}" '
                    f'style="stroke:{STROKE};stroke-width:{2 if whole else 1.5}"/>')
        tick_xs.append(x)
        if not whole:
            body.append(_frac_label(x, y - 40, k, 10, 12))
            top.append(f"{k}/10")
        lab = _dec(value)
        body.append(_text(x, y + 28, lab, 13, weight="700" if whole else "400",
                          color=TEXT if whole else POINT))
        bottom.append(lab)
    gaps = {tick_xs[i + 1] - tick_xs[i] for i in range(10)}
    # every top fraction must sit above the decimal of the same value
    paired = all(F(t) == F(b) for t, b in zip(top, bottom[1:10]))
    meta = {"start": "0", "end": "1", "spaces_per_unit": 10 if len(gaps) == 1 else None,
            "top_labels": top, "bottom_labels": bottom, "labels_match": paired}
    return _svg(y + 40, body, title), meta


# ---------------------------------------------------------------- 10 x 10 grids
GRID_RECT = re.compile(r'<rect class="cell" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" '
                       r'style="fill:([^;]+);')


def _grid_meta(svg_part: str) -> dict:
    """Read a grid's facts back from its drawn cells."""
    cells = GRID_RECT.findall(svg_part)
    xs = sorted({float(c[0]) for c in cells})
    ys = sorted({float(c[1]) for c in cells})
    sizes = {(c[2], c[3]) for c in cells}
    shaded = [(float(c[0]), float(c[1])) for c in cells if c[4] == FILL]
    full_cols = sum(1 for x in xs if sum(1 for s in shaded if s[0] == x) == len(ys))
    cells_n = len(cells)
    return {"columns": len(xs), "rows": len(ys), "cells": cells_n, "equal": len(sizes) == 1,
            "shaded": len(shaded), "full_columns": full_cols,
            "shaded_fraction": f"{len(shaded)}/{cells_n}",
            "decimal": _dec(F(len(shaded), cells_n))}


def hundred_grids(shaded_list: list[int], title: str, labels: list[str] | None = None) -> tuple[str, dict]:
    """Draw one grid per entry, side by side. Cells are shaded down column 1, then column 2, and so on.

    A full column is 10 hundredths, which is 1 tenth.
    """
    n = len(shaded_list)
    gap = 28
    side = F(min(200, (W - 2 * PAD - (n - 1) * gap) // n))
    cell = side / 10
    total_w = n * side + (n - 1) * gap
    left = (W - total_w) / 2
    top = F(PAD)
    parts, metas = [], []
    for g, shaded in enumerate(shaded_list):
        gx = left + g * (side + gap)
        part = []
        for c in range(10):
            for r in range(10):
                idx = c * 10 + r
                fill = FILL if idx < shaded else EMPTY
                part.append(f'<rect class="cell" x="{_f(gx + c * cell)}" y="{_f(top + r * cell)}" '
                            f'width="{_f(cell)}" height="{_f(cell)}" '
                            f'style="fill:{fill};stroke:{STROKE};stroke-width:1"/>')
        part.append(f'<rect x="{_f(gx)}" y="{_f(top)}" width="{_f(side)}" height="{_f(side)}" '
                    f'style="fill:none;stroke:{STROKE};stroke-width:2.5"/>')
        part_svg = "".join(part)
        m = _grid_meta(part_svg)
        if labels:
            part_svg += _text(gx + side / 2, top + side + 24, labels[g], 16, weight="700")
            m["label"] = labels[g]
        parts.append(part_svg)
        metas.append(m)
    height = top + side + (34 if labels else 0) + PAD
    svg = _svg(height, parts, title)
    meta = metas[0] if n == 1 else {"grids": metas}
    return svg, meta


# ---------------------------------------------------------------- place-value chart
PLACES = [("Ones", F(1)), ("Tenths", F(1, 10)), ("Hundredths", F(1, 100)), ("Thousandths", F(1, 1000))]
COL_W = [40, 54, 82, 92]  # Ones, Tenths, Hundredths, Thousandths
DOT_W = 12


def place_chart(rows: list[str], title: str) -> tuple[str, dict]:
    """rows: decimals as strings, e.g. '0.5'. Each digit goes in its own column."""
    x = F(PAD)
    col_x = []  # (left, width) per place; the dot column sits between Ones and Tenths
    for i, w in enumerate(COL_W):
        col_x.append((x, F(w)))
        x += w
        if i == 0:
            dot_left = x
            x += DOT_W
    right = x
    head_h, frac_h, row_h = 26, 40, 34
    y0 = F(PAD)
    body = []
    total_h = head_h + frac_h + row_h * len(rows)
    # outer box and column lines
    body.append(f'<rect x="{_f(PAD)}" y="{_f(y0)}" width="{_f(right - PAD)}" height="{_f(total_h)}" '
                f'style="fill:none;stroke:{STROKE};stroke-width:2"/>')
    for i, (cx, cw) in enumerate(col_x):
        if i > 0:
            body.append(f'<line x1="{_f(cx)}" y1="{_f(y0)}" x2="{_f(cx)}" y2="{_f(y0 + total_h)}" '
                        f'style="stroke:{STROKE};stroke-width:1.2"/>')
    body.append(f'<line x1="{_f(dot_left)}" y1="{_f(y0)}" x2="{_f(dot_left)}" y2="{_f(y0 + total_h)}" '
                f'style="stroke:{STROKE};stroke-width:1.2"/>')
    for yy in (y0 + head_h + frac_h,):
        body.append(f'<line x1="{_f(PAD)}" y1="{_f(yy)}" x2="{_f(right)}" y2="{_f(yy)}" '
                    f'style="stroke:{STROKE};stroke-width:2"/>')
    headings, worth = [], []
    for (name, val), (cx, cw) in zip(PLACES, col_x):
        body.append(_text(cx + cw / 2, y0 + 18, name, 13, weight="700"))
        headings.append(name)
        if val == 1:
            body.append(_text(cx + cw / 2, y0 + head_h + 25, "1", 13))
        else:
            body.append(_frac_label(cx + cw / 2, y0 + head_h + 12, 1, val.denominator, 12))
        worth.append(str(val))
    meta_rows = []
    for r, s in enumerate(rows):
        whole, frac = s.split(".")
        digits = [whole] + list(frac)
        yy = y0 + head_h + frac_h + r * row_h
        if r > 0:
            body.append(f'<line x1="{_f(PAD)}" y1="{_f(yy)}" x2="{_f(right)}" y2="{_f(yy)}" '
                        f'style="stroke:{STROKE};stroke-width:1"/>')
        drawn = []
        for d, (cx, cw) in zip(digits, col_x):
            body.append(_text(cx + cw / 2, yy + 23, d, 17, weight="600"))
            drawn.append(d)
        body.append(f'<circle cx="{_f(dot_left + DOT_W / 2)}" cy="{_f(yy + 20)}" r="3.2" style="fill:{POINT}"/>')
        # value read back from the drawn digits and the worth of each column
        value = sum(F(int(d)) * PLACES[i][1] for i, d in enumerate(drawn))
        meta_rows.append({"digits": drawn, "value": _dec(value)})
    meta = {"headings": headings, "worth": worth, "rows": meta_rows}
    return _svg(y0 + total_h + PAD, body, title), meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "dm-tenths-nl", *tenths_line("Number line from 0 to 1 in tenths, as fractions and decimals"))
draw.save(OUT, "dm-grid-35", *hundred_grids([35], "A hundred grid with 35 squares shaded"))
draw.save(OUT, "dm-grid-compare", *hundred_grids([30, 25], "Hundred grids for 0.3 and 0.25", ["0.3", "0.25"]))
draw.save(OUT, "dm-chart", *place_chart(["0.5", "0.05", "1.375"], "Place-value chart for 0.5, 0.05 and 1.375"))
draw.save(OUT, "dm-p1", *draw.number_line(0, 1, 10, "Number line in tenths with a dot", point=F(6, 10)))
draw.save(OUT, "dm-p2", *hundred_grids([47], "A hundred grid with 47 squares shaded"))
draw.save(OUT, "dm-q1", *hundred_grids([8], "A hundred grid with 8 squares shaded"))
draw.save(OUT, "dm-q8", *draw.number_line(0, 2, 10, "Number line from 0 to 2 in tenths with a dot", point=F(13, 10)))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-decimals-meaning")
