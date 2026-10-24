"""Diagrams for s0-add-sub-two-digit. Run from repo root.

Two helpers kept here (not in tools/draw.py), both following draw.py's rule: every
stick, square, digit and mark is first placed as a record with its position, the
SVG is written from those records, and the meta is read back from the same records.

- blocks(): base-ten pictures. A ten is a tall stick split into 10 cells; a one is a
  small square. Ones sit in rows of 5 so they are easy to count. Pieces can be "new"
  (made by a trade, drawn in the second colour), "crossed" (taken away), and a ring
  can be drawn round the first 10 ones of a row.
- columns(): a two-digit sum in Tens and Ones columns, with small carried or
  borrowed digits and crossed-out digits.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, MUTED, PAD, POINT, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- base-ten blocks
CELL = 6          # one cell of a ten-stick
STICK_W = 12
TEN_PITCH = 17
ONE = 12
ONE_PITCH = 15
PER_ROW = 5       # ones per row of the ones grid
LABEL_W = 56
ROW_H = 10 * CELL
ROW_GAP = 26


def blocks(rows: list[dict], title: str):
    """rows: [{"label": "38", "tens": 3, "ones": 8, "new_tens": 0, "new_ones": 0,
               "ring": False, "cross_tens": 0, "cross_ones": 0}]
    New pieces are drawn first among the tens (last) and first among the ones, so a
    ring round ones 1-10 circles the 10 new ones after a ten is broken.
    """
    recs: list[dict] = []
    rings: list[dict] = []
    labels: list[dict] = []
    max_tens = max(r["tens"] for r in rows)
    x_tens = PAD + LABEL_W
    x_ones = x_tens + max_tens * TEN_PITCH + 14
    for i, r in enumerate(rows):
        y = PAD + i * (ROW_H + ROW_GAP)
        labels.append({"row": i, "x": PAD, "y": y + ROW_H / 2 + 6, "s": r.get("label", "")})
        nt, no = r["tens"], r["ones"]
        new_t, new_o = r.get("new_tens", 0), r.get("new_ones", 0)
        ct, co = r.get("cross_tens", 0), r.get("cross_ones", 0)
        for k in range(nt):
            recs.append({"kind": "ten", "row": i, "x": x_tens + k * TEN_PITCH, "y": y,
                         "new": k >= nt - new_t, "crossed": k >= nt - ct, "cells": 10})
        for k in range(no):
            col, rr = k % PER_ROW, k // PER_ROW
            recs.append({"kind": "one", "row": i, "x": x_ones + col * ONE_PITCH, "y": y + rr * ONE_PITCH,
                         "new": k < new_o, "crossed": k >= no - co})
        if r.get("ring"):
            rings.append({"row": i, "x0": x_ones - 4, "y0": y - 4,
                          "x1": x_ones + (PER_ROW - 1) * ONE_PITCH + ONE + 4,
                          "y1": y + ONE_PITCH + ONE + 4})

    body: list[str] = []
    for lab in labels:
        body.append(_text(lab["x"], lab["y"], lab["s"], 17, anchor="start", weight="700"))
    for c in recs:
        fill = EMPTY if c["crossed"] else (POINT if c["new"] else FILL)
        if c["kind"] == "ten":
            x, y = c["x"], c["y"]
            body.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{STICK_W}" height="{10 * CELL}" '
                        f'style="fill:{fill};stroke:{STROKE};stroke-width:1.4"/>')
            for j in range(1, c["cells"]):
                yy = y + j * CELL
                body.append(f'<line x1="{_f(x)}" y1="{_f(yy)}" x2="{_f(x + STICK_W)}" y2="{_f(yy)}" '
                            f'style="stroke:{STROKE};stroke-width:0.8"/>')
            w, h = STICK_W, 10 * CELL
        else:
            x, y = c["x"], c["y"]
            body.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{ONE}" height="{ONE}" '
                        f'style="fill:{fill};stroke:{STROKE};stroke-width:1.4"/>')
            w, h = ONE, ONE
        if c["crossed"]:
            body.append(f'<path d="M{_f(x - 1)},{_f(y - 1)} L{_f(x + w + 1)},{_f(y + h + 1)} '
                        f'M{_f(x + w + 1)},{_f(y - 1)} L{_f(x - 1)},{_f(y + h + 1)}" '
                        f'style="fill:none;stroke:{TEXT};stroke-width:1.8"/>')
    for g in rings:
        body.append(f'<rect x="{_f(g["x0"])}" y="{_f(g["y0"])}" width="{_f(g["x1"] - g["x0"])}" '
                    f'height="{_f(g["y1"] - g["y0"])}" rx="6" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2.5"/>')
    h = PAD * 2 + len(rows) * ROW_H + (len(rows) - 1) * ROW_GAP

    # ---- meta, read back from the records
    meta_rows = []
    for i in range(len(rows)):
        rc = [c for c in recs if c["row"] == i]
        tens = [c for c in rc if c["kind"] == "ten"]
        ones = [c for c in rc if c["kind"] == "one"]
        ring = [g for g in rings if g["row"] == i]
        ringed = sum(1 for c in ones for g in ring
                     if g["x0"] <= c["x"] and c["x"] + ONE <= g["x1"] and g["y0"] <= c["y"] and c["y"] + ONE <= g["y1"])
        left_t = sum(1 for c in tens if not c["crossed"])
        left_o = sum(1 for c in ones if not c["crossed"])
        meta_rows.append({
            "label": next(lab["s"] for lab in labels if lab["row"] == i),
            "tens": len(tens), "ones": len(ones),
            "cells_per_ten": sorted({c["cells"] for c in tens}),
            "value": 10 * len(tens) + len(ones),
            "new_tens": sum(1 for c in tens if c["new"]),
            "new_ones": sum(1 for c in ones if c["new"]),
            "crossed_tens": len(tens) - left_t, "crossed_ones": len(ones) - left_o,
            "left": 10 * left_t + left_o,
            "ringed_ones": ringed,
        })
    return _svg(h, body, title), {"rows": meta_rows}


# ---------------------------------------------------------------- column method
COL_W = 62
SIGN_W = 30
BIG = 26
SMALL = 16
PLACE = {1: "Tens", 0: "Ones"}


def columns(top: int, bottom: int, op: str, title: str, result: int | None = None,
            above: dict | None = None, before: dict | None = None, crossed: list | None = None):
    """above: {place: "1"} small digit above the top row (a carry, or a new tens digit).
    before: {place: "1"} small digit written just left of the top digit (10 more ones).
    crossed: [place, ...] top-row digits struck through."""
    total = SIGN_W + 2 * COL_W
    left = (W - total) / 2
    centre = {1: left + SIGN_W + COL_W / 2, 0: left + SIGN_W + COL_W * 1.5}
    y_head = PAD + 12
    y_small = PAD + 44
    y_top = PAD + 44 + 30
    rows = [top, bottom] + ([result] if result is not None else [])
    recs: list[dict] = []
    for i, n in enumerate(rows):
        y = y_top + i * 40 + (10 if i == 2 else 0)
        s = str(n)
        for k, ch in enumerate(reversed(s)):
            recs.append({"row": i, "place": k, "x": centre[k], "y": y, "ch": ch,
                         "crossed": i == 0 and k in (crossed or [])})
    smalls = []
    for p, d in (above or {}).items():
        smalls.append({"pos": "above", "place": p, "x": centre[p], "y": y_small, "ch": d})
    for p, d in (before or {}).items():
        smalls.append({"pos": "before", "place": p, "x": centre[p] - 12, "y": y_top - 8, "ch": d})

    body: list[str] = []
    for p in (1, 0):
        gx = centre[p] - COL_W / 2 + 4
        body.append(f'<rect x="{_f(gx)}" y="{_f(PAD + 22)}" width="{COL_W - 8}" '
                    f'height="{_f(y_top + 40 * (len(rows) - 1) + 22 - PAD - 22)}" rx="6" '
                    f'style="fill:none;stroke:{MUTED};stroke-width:1;stroke-dasharray:3 4"/>')
        body.append(_text(centre[p], y_head, PLACE[p], 15, weight="600"))
    for c in recs:
        body.append(_text(c["x"] + (5 if c["place"] == 0 and before and 0 in before and c["row"] == 0 else 0),
                          c["y"], c["ch"], BIG, weight="600"))
        if c["crossed"]:
            body.append(f'<line x1="{_f(c["x"] - 11)}" y1="{_f(c["y"] + 3)}" x2="{_f(c["x"] + 11)}" '
                        f'y2="{_f(c["y"] - BIG + 2)}" style="stroke:{POINT};stroke-width:2.5"/>')
    for s in smalls:
        body.append(_text(s["x"], s["y"], s["ch"], SMALL, weight="700", color=POINT))
    y_op = y_top + 40
    body.append(_text(left + SIGN_W / 2, y_op, {"+": "+", "-": "−"}[op], BIG, weight="700"))
    y_line = y_op + 12
    body.append(f'<line x1="{_f(left)}" y1="{_f(y_line)}" x2="{_f(left + total)}" y2="{_f(y_line)}" '
                f'style="stroke:{STROKE};stroke-width:2"/>')
    h = y_top + 40 * 2 + 10 + PAD

    # ---- meta, read back from the records
    def num(i):
        rc = sorted((c for c in recs if c["row"] == i), key=lambda c: c["x"])
        return "".join(c["ch"] for c in rc) or None
    vals = [num(i) for i in range(3)]
    meta = {
        "op": op, "top": vals[0], "bottom": vals[1], "result": vals[2],
        "headers": [PLACE[p] for p in (1, 0)],
        "columns": [[next((c["ch"] for c in recs if c["place"] == p and c["row"] == i), "")
                     for i in range(len(rows))] for p in (1, 0)],
        "small_above": [{"place": PLACE[s["place"]], "digit": s["ch"]} for s in smalls if s["pos"] == "above"],
        "small_before": [{"place": PLACE[s["place"]], "digit": s["ch"]} for s in smalls if s["pos"] == "before"],
        "crossed": [{"place": PLACE[c["place"]], "digit": c["ch"]} for c in recs if c["crossed"]],
    }
    if vals[2] is not None:
        a, b, r = int(vals[0]), int(vals[1]), int(vals[2])
        meta["answer_correct"] = (a + b if op == "+" else a - b) == r
    return _svg(h, body, title), meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "rg-47", *blocks([
    {"label": "47", "tens": 4, "ones": 7},
], "47 as 4 tens and 7 ones"))

draw.save(OUT, "rg-add-blocks", *blocks([
    {"label": "38", "tens": 3, "ones": 8},
    {"label": "45", "tens": 4, "ones": 5},
    {"label": "Both", "tens": 7, "ones": 13, "ring": True},
    {"label": "Trade", "tens": 8, "ones": 3, "new_tens": 1},
], "38 plus 45 with tens and ones"))

draw.save(OUT, "rg-add-columns", *columns(
    38, 45, "+", "38 plus 45 in columns", result=83, above={1: "1"}))

draw.save(OUT, "rg-sub-blocks", *blocks([
    {"label": "52", "tens": 5, "ones": 2},
    {"label": "Break", "tens": 4, "ones": 12, "new_ones": 10, "ring": True},
    {"label": "Take", "tens": 4, "ones": 12, "new_ones": 10, "cross_tens": 2, "cross_ones": 7},
], "52 minus 27 with tens and ones"))

draw.save(OUT, "rg-sub-columns", *columns(
    52, 27, "-", "52 minus 27 in columns", result=25, above={1: "4"}, before={0: "1"}, crossed=[1]))

draw.save(OUT, "rg-p1", *blocks([
    {"label": "", "tens": 6, "ones": 14},
], "6 tens and 14 ones"))

draw.save(OUT, "rg-p4", *blocks([
    {"label": "43", "tens": 4, "ones": 3},
], "43 as 4 tens and 3 ones"))

draw.save(OUT, "rg-q5", *blocks([
    {"label": "", "tens": 3, "ones": 15},
], "3 tens and 15 ones"))

print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-add-sub-two-digit")
