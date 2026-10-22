"""Diagrams for s0-multiply-fractions. Run from repo root.

Adds an area-model helper (kept here, not in tools/draw.py). It follows draw.py's
rule: the meta is read back from the cells actually drawn, not copied from the request.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, PAD, STROKE, W, _f, _frac_label, _svg  # noqa: E402

OUT = Path(__file__).resolve().parent
LIGHT_OPACITY = "0.32"


def area_model(col_frac: str, row_frac: str, title: str, labels: bool = True) -> tuple[str, dict]:
    """Rectangle cut into columns (denominator of col_frac) and rows (denominator of row_frac).

    The first `numerator` columns and the top `numerator` rows get a light tint.
    Cells in both a shaded column and a shaded row are dark: that overlap is the product.
    Labels (optional): col_frac above the shaded columns, row_frac left of the shaded rows.
    """
    cn, cd = (int(x) for x in col_frac.split("/"))
    rn, rd = (int(x) for x in row_frac.split("/"))
    label_w = 44 if labels else 0
    label_h = 42 if labels else 0
    x0, x1 = F(PAD + label_w), F(W - PAD)
    y0 = F(PAD + label_h)
    height = F(160)
    y1 = y0 + height
    cw, rh = (x1 - x0) / cd, height / rd
    body: list[str] = []
    widths, heights = set(), set()
    dark = light = 0
    dark_cols, dark_rows = set(), set()
    for r in range(rd):
        for c in range(cd):
            in_col, in_row = c < cn, r < rn
            x, y = x0 + c * cw, y0 + r * rh
            widths.add(cw)
            heights.add(rh)
            if in_col and in_row:
                style = f"fill:{FILL}"
                dark += 1
                dark_cols.add(c)
                dark_rows.add(r)
            elif in_col or in_row:
                style = f"fill:{FILL};fill-opacity:{LIGHT_OPACITY}"
                light += 1
            else:
                style = f"fill:{EMPTY}"
            body.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(cw)}" height="{_f(rh)}" '
                        f'style="{style};stroke:{STROKE};stroke-width:1.5"/>')
    # thicker outline of the whole
    body.append(f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(height)}" '
                f'style="fill:none;stroke:{STROKE};stroke-width:2.5"/>')
    drawn_labels = {}
    if labels:
        # bracket above the shaded columns
        bx0, bx1, by = x0, x0 + cn * cw, y0 - 8
        body.append(f'<path d="M{_f(bx0)},{_f(by + 5)} L{_f(bx0)},{_f(by)} L{_f(bx1)},{_f(by)} L{_f(bx1)},{_f(by + 5)}" '
                    f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
        body.append(_frac_label((bx0 + bx1) / 2, PAD + 2, cn, cd, 14))
        # bracket left of the shaded rows
        bx, by0, by1 = x0 - 8, y0, y0 + rn * rh
        body.append(f'<path d="M{_f(bx + 5)},{_f(by0)} L{_f(bx)},{_f(by0)} L{_f(bx)},{_f(by1)} L{_f(bx + 5)},{_f(by1)}" '
                    f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
        body.append(_frac_label(PAD + 12, (by0 + by1) / 2 - 12, rn, rd, 14))
        drawn_labels = {"top": f"{cn}/{cd}", "left": f"{rn}/{rd}"}
    cells = cd * rd
    meta = {
        "columns": cd, "rows": rd,
        "equal": len(widths) == 1 and len(heights) == 1,
        "shaded_columns": cn, "shaded_rows": rn,
        "cells": cells, "dark": dark, "light": light,
        "dark_block": [len(dark_cols), len(dark_rows)],
        "dark_fraction": f"{dark}/{cells}",
        "labels": drawn_labels,
    }
    return _svg(y1 + PAD, body, title), meta


draw.save(OUT, "mf-dots-12", *draw.dot_groups(4, 3, 1, "12 laddoos in 4 equal groups, one group marked"))
draw.save(OUT, "mf-area-hook", *area_model("1/3", "1/2", "Area model for one third of one half"))
draw.save(OUT, "mf-area-ex", *area_model("2/3", "3/4", "Area model for two thirds times three quarters"))
draw.save(OUT, "mf-p1", *draw.dot_groups(3, 4, 2, "12 diyas in 3 equal groups, two groups marked"))
draw.save(OUT, "mf-p3", *area_model("3/5", "1/2", "Area model for three fifths times one half"))
draw.save(OUT, "mf-q2", *area_model("1/4", "2/5", "Area model for one quarter times two fifths"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-multiply-fractions")
