"""Diagrams for s0-add-sub-decimals. Run from repo root.

Adds a column-layout helper (kept here, not in tools/draw.py). It follows draw.py's
rule: every digit, point and mark is first placed as a record with its x and y, the
SVG is written from those records, and the meta is read back from the same records
(rows are rebuilt by sorting drawn characters by x; point alignment is measured from
the drawn x positions). Nothing in the meta is copied from the request.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import MUTED, PAD, POINT, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

PLACE_NAMES = {2: "Hundreds", 1: "Tens", 0: "Ones", -1: "Tenths", -2: "Hundredths"}
DIGIT_SIZE = 22
ROW_H = 36
SIGN_W = 26
POINT_W = 16


def _split(s: str) -> tuple[str, str]:
    return (s.split(".") + [""])[:2] if "." in s else (s, "")


def _rebuild(chars: list[dict]) -> str:
    """Join the drawn characters of one row, left to right."""
    return "".join(c["ch"] for c in sorted(chars, key=lambda c: c["x"]))


def column_layout(top: str, bottom: str, op: str, title: str, result: str | None = None,
                  fill_zeros: bool = False, carries: dict | None = None,
                  aligned: bool = True, headers: str = "places", caption: str | None = None):
    """Two numbers written one under the other, with a line and (optionally) the answer.

    aligned=True : place-value columns; decimal points share one column.
    aligned=False: the mistake. Characters are right-aligned in equal slots, so the
                   last digits line up and the points do not.
    fill_zeros   : empty decimal places are drawn as a 0 inside a dashed box.
    carries      : {place: "1"} small digit drawn above the top row in that column.
    headers      : "places" (Tens, Ones, Tenths ...), "money" (Rupees / Paise) or None.
    """
    rows = [top, bottom] + ([result] if result is not None else [])
    recs: list[dict] = []   # every drawn character: {"row", "x", "y", "ch", "filled"}
    body: list[str] = []
    header_h = {"places": 30, "money": 40, None: 0}[headers if aligned else None]
    carry_h = 22 if carries else 0
    y_first = PAD + header_h + carry_h + DIGIT_SIZE
    y_last = y_first + (len(rows) - 1) * ROW_H + (10 if len(rows) == 3 else 0)
    guide_top = PAD + header_h - 4
    guide_h = y_last + 10 - guide_top

    if aligned:
        int_len = max(len(_split(r)[0]) for r in rows)
        dec_len = max(len(_split(r)[1]) for r in rows)
        places = list(range(int_len - 1, -1, -1)) + list(range(-1, -dec_len - 1, -1))
        if headers == "places":
            widths = {p: max(46, len(PLACE_NAMES[p]) * 8 + 6) for p in places}
        else:
            widths = {p: 46 for p in places}
        total = SIGN_W + sum(widths.values()) + POINT_W
        x = F(W - total, 2) + SIGN_W
        centre = {}
        for p in places:
            if p == -1:
                point_x = x + F(POINT_W, 2)
                x += POINT_W
            centre[p] = x + F(widths[p], 2)
            x += widths[p]
        if dec_len == 0:
            point_x = x + F(POINT_W, 2)
        left_edge = F(W - total, 2)
        right_edge = left_edge + total
        # column guides (light) so each place is a visible column
        for p in places:
            gx0 = centre[p] - F(widths[p], 2) + 3
            body.append(f'<rect x="{_f(gx0)}" y="{_f(guide_top)}" width="{_f(widths[p] - 6)}" '
                        f'height="{_f(guide_h)}" rx="6" '
                        f'style="fill:none;stroke:{MUTED};stroke-width:1;stroke-dasharray:3 4"/>')
        drawn_headers = []
        if headers == "places":
            for p in places:
                body.append(_text(centre[p], PAD + 12, PLACE_NAMES[p], 14, weight="600"))
                drawn_headers.append(PLACE_NAMES[p])
        elif headers == "money":
            groups = [("Rupees", [p for p in places if p >= 0]), ("Paise", [p for p in places if p < 0])]
            for name, ps in groups:
                if not ps:
                    continue
                gx0 = centre[ps[0]] - F(widths[ps[0]], 2) + 4
                gx1 = centre[ps[-1]] + F(widths[ps[-1]], 2) - 4
                body.append(_text((gx0 + gx1) / 2, PAD + 12, name, 14, weight="600"))
                body.append(f'<path d="M{_f(gx0)},{_f(PAD + 24)} L{_f(gx0)},{_f(PAD + 19)} L{_f(gx1)},{_f(PAD + 19)} '
                            f'L{_f(gx1)},{_f(PAD + 24)}" style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
                drawn_headers.append(name)
        for i, r in enumerate(rows):
            y = y_first + i * ROW_H + (10 if i == 2 else 0)
            ip, dp = _split(r)
            for k, ch in enumerate(reversed(ip)):
                recs.append({"row": i, "x": centre[k], "y": y, "ch": ch, "filled": False})
            if "." in r or (fill_zeros and dec_len):
                recs.append({"row": i, "x": point_x, "y": y, "ch": ".", "filled": not ("." in r)})
            for k in range(dec_len):
                if k < len(dp):
                    recs.append({"row": i, "x": centre[-(k + 1)], "y": y, "ch": dp[k], "filled": False})
                elif fill_zeros:
                    recs.append({"row": i, "x": centre[-(k + 1)], "y": y, "ch": "0", "filled": True})
        drawn_carries = []
        for p, d in (carries or {}).items():
            cy = PAD + header_h + 14
            body.append(_text(centre[p], cy, d, 14, weight="700", color=POINT))
            drawn_carries.append({"place": PLACE_NAMES[p], "digit": d})
    else:
        slot = 34
        n = max(len(r) for r in rows)
        total = SIGN_W + n * slot
        left_edge = F(W - total, 2)
        right_edge = left_edge + total
        drawn_headers, drawn_carries = [], []
        for k in range(n):
            gx0 = right_edge - slot * (k + 1) + 3
            body.append(f'<rect x="{_f(gx0)}" y="{_f(guide_top + 4)}" width="{slot - 6}" height="{_f(guide_h - 4)}" '
                        f'rx="6" style="fill:none;stroke:{MUTED};stroke-width:1;stroke-dasharray:3 4"/>')
        for i, r in enumerate(rows):
            y = y_first + i * ROW_H + (10 if i == 2 else 0)
            for k, ch in enumerate(reversed(r)):
                x = right_edge - slot * k - F(slot, 2)
                recs.append({"row": i, "x": x, "y": y, "ch": ch, "filled": False})

    # draw characters
    for c in recs:
        if c["ch"] == ".":
            body.append(f'<circle cx="{_f(c["x"])}" cy="{_f(c["y"] - 2)}" r="3.2" style="fill:{TEXT}"/>')
        else:
            if c["filled"]:
                body.append(f'<rect x="{_f(c["x"] - 12)}" y="{_f(c["y"] - DIGIT_SIZE + 1)}" width="24" '
                            f'height="{DIGIT_SIZE + 6}" rx="5" style="fill:none;stroke:{POINT};stroke-width:1.6;'
                            f'stroke-dasharray:4 3"/>')
            body.append(_text(c["x"], c["y"], c["ch"], DIGIT_SIZE, weight="600",
                              color=POINT if c["filled"] else TEXT))
    # operator, line
    y_op = y_first + ROW_H
    sign = {"+": "+", "-": "−"}[op]
    body.append(_text(left_edge + SIGN_W / 2, y_op, sign, DIGIT_SIZE, weight="700"))
    y_line = y_op + 12
    body.append(f'<line x1="{_f(left_edge)}" y1="{_f(y_line)}" x2="{_f(right_edge)}" y2="{_f(y_line)}" '
                f'style="stroke:{STROKE};stroke-width:2"/>')
    bottom_y = max(y_last, y_line) + 10
    if caption:
        body.append(_text(W / 2, bottom_y + 22, caption, 14, weight="600"))
        bottom_y += 30

    # ---- meta, read back from the drawn records
    def row_chars(i):
        return [c for c in recs if c["row"] == i]
    rebuilt = [_rebuild(row_chars(i)) for i in range(3)]
    point_xs = [c["x"] for c in recs if c["ch"] == "."]
    rows_with_point = {c["row"] for c in recs if c["ch"] == "."}
    vals = [F(s) if s else None for s in rebuilt]
    meta = {
        "op": op,
        "top": rebuilt[0],
        "bottom": rebuilt[1],
        "result": rebuilt[2] or None,
        "points_aligned": len(rows_with_point) == len(rows) and len(set(point_xs)) == 1,
        "headers": drawn_headers,
        "filled_zeros": sum(1 for c in recs if c["filled"] and c["ch"] != "."),
        "carries": drawn_carries,
    }
    # what sits in each drawn column, top to bottom, e.g. ["5", "7", "2"] (read back by x; "" = empty)
    xs = sorted({c["x"] for c in recs})
    meta["columns"] = [[next((c["ch"] for c in recs if c["x"] == x and c["row"] == i), "")
                        for i in range(len(rows))] for x in xs]
    if vals[2] is not None:
        meta["answer_correct"] = (vals[0] + vals[1] if op == "+" else vals[0] - vals[1]) == vals[2]
    if aligned:
        # each digit's place value, measured from its x distance to the point
        ok = True
        for c in recs:
            if c["ch"] == ".":
                continue
            px = point_x
            places_left = [p for p in centre if p >= 0 and centre[p] == c["x"]]
            places_right = [p for p in centre if p < 0 and centre[p] == c["x"]]
            if (c["x"] < px and not places_left) or (c["x"] > px and not places_right):
                ok = False
        meta["digits_in_columns"] = ok
    return _svg(bottom_y + PAD, body, title), meta


draw.save(OUT, "ad-add-columns", *column_layout(
    "12.5", "3.75", "+", "12.5 plus 3.75 in place-value columns", result="16.25", carries={0: "1"}))
draw.save(OUT, "ad-wrong-line-up", *column_layout(
    "12.5", "3.75", "+", "12.5 and 3.75 with the last digits lined up", aligned=False,
    caption="Points not lined up"))
draw.save(OUT, "ad-sub-zero", *column_layout(
    "7.4", "2.65", "-", "7.40 minus 2.65 with a zero filled in", result="4.75", fill_zeros=True))
draw.save(OUT, "ad-money-change", *column_layout(
    "500", "236.75", "-", "500.00 rupees minus 236.75 rupees", result="263.25", fill_zeros=True,
    headers="money"))
draw.save(OUT, "ad-p1", *column_layout(
    "3.6", "1.25", "+", "3.6 plus 1.25 in place-value columns, answer row empty"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-add-sub-decimals")
