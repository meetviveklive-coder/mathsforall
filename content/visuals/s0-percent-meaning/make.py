"""Diagrams for s0-percent-meaning. Run from repo root.

Adds one helper (kept here, not in tools/draw.py), copied in approach from
s0-decimals-meaning's hundred grid:
- percent_grids: one or more 10 x 10 grids with some cells shaded, either down the
  columns or as a square block in the top-left corner (for a quarter).

It follows draw.py's rule: the meta is read back from what was actually drawn.
The grid facts are parsed from the finished SVG text, not copied from the request.
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, PAD, STROKE, TEXT, W, _f, _frac_label, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

GRID_RECT = re.compile(r'<rect class="cell" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" '
                       r'style="fill:([^;]+);')


def _dec(value: F) -> str:
    """Write a fraction with denominator 1, 10 or 100 as a decimal string ('0.37', '1.5', '1')."""
    for places in range(0, 3):
        if (value * 10 ** places).denominator == 1:
            if places == 0:
                return str(value.numerator)
            n = int(value * 10 ** places)
            whole, frac = divmod(n, 10 ** places)
            s = f"{whole}.{frac:0{places}d}"
            return s
    raise ValueError(value)


def _grid_meta(svg_part: str) -> dict:
    """Read one grid's facts back from its drawn cells."""
    cells = GRID_RECT.findall(svg_part)
    xs = sorted({float(c[0]) for c in cells})
    ys = sorted({float(c[1]) for c in cells})
    sizes = {(c[2], c[3]) for c in cells}
    shaded = [(float(c[0]), float(c[1])) for c in cells if c[4] == FILL]
    full_cols = sum(1 for x in xs if sum(1 for s in shaded if s[0] == x) == len(ys))
    n = len(cells)
    # a block: the shaded cells fill a k x k square in the top-left corner
    sx = sorted({s[0] for s in shaded})
    sy = sorted({s[1] for s in shaded})
    block = (len(shaded) > 0 and len(sx) * len(sy) == len(shaded) and len(sx) == len(sy)
             and sx == xs[:len(sx)] and sy == ys[:len(sy)])
    return {"columns": len(xs), "rows": len(ys), "cells": n, "equal": len(sizes) == 1,
            "shaded": len(shaded), "full_columns": full_cols,
            "square_block": f"{len(sx)}x{len(sy)}" if block else None,
            "percent": str(F(len(shaded), n) * 100),
            "decimal": _dec(F(len(shaded), n))}


def percent_grids(specs: list[dict], title: str, caption: str | None = None) -> tuple[str, dict]:
    """specs: [{"shaded": 37, "pattern": "columns"|"block", "label": "37%", "frac": (1, 2)}].

    "columns": shade down column 1, then column 2, and so on (a full column is 10%).
    "block": shade a k x k square in the top-left corner (k*k must equal shaded).
    """
    n = len(specs)
    gap = 28 if n < 3 else 20
    side = F(min(200, (W - 2 * PAD - (n - 1) * gap) // n))
    cell = side / 10
    total_w = n * side + (n - 1) * gap
    left = (W - total_w) / 2
    top = F(PAD)
    has_label = any(s.get("label") for s in specs)
    has_frac = any(s.get("frac") for s in specs)
    parts, metas = [], []
    for g, s in enumerate(specs):
        gx = left + g * (side + gap)
        k = None
        if s.get("pattern") == "block":
            k = int(round(s["shaded"] ** 0.5))
            assert k * k == s["shaded"]
        part = []
        for c in range(10):
            for r in range(10):
                if k is not None:
                    on = c < k and r < k
                else:
                    on = c * 10 + r < s["shaded"]
                part.append(f'<rect class="cell" x="{_f(gx + c * cell)}" y="{_f(top + r * cell)}" '
                            f'width="{_f(cell)}" height="{_f(cell)}" '
                            f'style="fill:{FILL if on else EMPTY};stroke:{STROKE};stroke-width:{1 if n < 3 else 0.6}"/>')
        part.append(f'<rect x="{_f(gx)}" y="{_f(top)}" width="{_f(side)}" height="{_f(side)}" '
                    f'style="fill:none;stroke:{STROKE};stroke-width:2.5"/>')
        part_svg = "".join(part)
        m = _grid_meta(part_svg)
        if s.get("label"):
            part_svg += _text(gx + side / 2, top + side + 24, s["label"], 16, weight="700")
            m["label"] = s["label"]
        if s.get("frac"):
            num, den = s["frac"]
            part_svg += _frac_label(gx + side / 2, top + side + 46, num, den, 14)
            m["fraction"] = f"{num}/{den}"
        parts.append(part_svg)
        metas.append(m)
    y = top + side + (34 if has_label else 0) + (40 if has_frac else 0)
    if caption:
        parts.append(_text(W / 2, y + 18, caption, 16, weight="700", color=TEXT))
        y += 28
    svg = _svg(y + PAD, parts, title)
    if n == 1:
        meta = metas[0]
    else:
        total = sum(m["shaded"] for m in metas)
        meta = {"grids": metas, "total_shaded": total,
                "total_percent": str(sum(F(m["shaded"], m["cells"]) for m in metas) * 100)}
        if caption:
            meta["caption"] = caption
    return svg, meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "pm-grid-37", *percent_grids([{"shaded": 37}], "A hundred grid with 37 squares shaded"))
draw.save(OUT, "pm-grid-5-50", *percent_grids(
    [{"shaded": 5, "label": "5%"}, {"shaded": 50, "label": "50%"}],
    "Hundred grids for 5% and 50%"))
draw.save(OUT, "pm-benchmarks", *percent_grids(
    [{"shaded": 50, "label": "50%", "frac": (1, 2)},
     {"shaded": 25, "pattern": "block", "label": "25%", "frac": (1, 4)},
     {"shaded": 10, "label": "10%", "frac": (1, 10)}],
    "Hundred grids for 50%, 25% and 10%"))
draw.save(OUT, "pm-150", *percent_grids(
    [{"shaded": 100, "label": "100%"}, {"shaded": 50, "label": "50%"}],
    "Two hundred grids showing 150%", caption="150% = 1.5"))
draw.save(OUT, "pm-p1", *percent_grids([{"shaded": 63}], "A hundred grid with 63 squares shaded"))
draw.save(OUT, "pm-q1", *percent_grids([{"shaded": 9}], "A hundred grid with 9 squares shaded"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-percent-meaning")
