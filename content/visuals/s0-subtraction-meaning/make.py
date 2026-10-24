"""Diagrams for s0-subtraction-meaning. Run from repo root.

New helpers (crossed-out objects, ten-frames, two rows to compare, number-line hops)
live here, not in tools/draw.py. Each one counts what it actually drew and returns
that count as meta, so the verifier can compare it with the topic's checks.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, MUTED, PAD, POINT, STROKE, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent
R = 10  # counter radius


def _counter(x, y, body):
    body.append(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{R}" style="fill:{FILL};stroke:{STROKE};stroke-width:1.2"/>')


def _cross(x, y, body):
    """A thick X over a counter. Returns 1 so callers can count what was drawn."""
    d = R + 1
    for x1, y1, x2, y2 in ((x - d, y - d, x + d, y + d), (x - d, y + d, x + d, y - d)):
        body.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" '
                    f'style="stroke:{STROKE};stroke-width:3;stroke-linecap:round"/>')
    return 1


# ---------------------------------------------------------------- take away: a row with some crossed out
def crossed_row(total: int, crossed: int, title: str):
    """One row of `total` counters; the LAST `crossed` of them get an X."""
    step = 30
    x0 = W / 2 - (total - 1) * step / 2
    y = PAD + 16
    body, drawn, xs = [], 0, 0
    for k in range(total):
        x = x0 + k * step
        _counter(x, y, body)
        drawn += 1
        if k >= total - crossed:
            xs += _cross(x, y, body)
    return _svg(PAD * 2 + 32, body, title), {"objects": drawn, "crossed": xs, "left": drawn - xs}


# ---------------------------------------------------------------- ten-frames
def ten_frames(frames: list[dict], title: str):
    """frames: [{"filled": 10, "crossed": [5,6,7,8,9]}]. Boxes fill row by row, 5 per row."""
    box, gap = 26, 20
    fw = 5 * box
    total_w = len(frames) * fw + (len(frames) - 1) * gap
    left = W / 2 - total_w / 2
    top = PAD
    body, meta_frames = [], []
    for i, fr in enumerate(frames):
        fx = left + i * (fw + gap)
        boxes = counters = crosses = 0
        for k in range(10):
            col, row = k % 5, k // 5
            bx, by = fx + col * box, top + row * box
            body.append(f'<rect x="{_f(bx)}" y="{_f(by)}" width="{box}" height="{box}" '
                        f'style="fill:{EMPTY};stroke:{STROKE};stroke-width:1.5"/>')
            boxes += 1
            if k < fr["filled"]:
                cx, cy = bx + box / 2, by + box / 2
                body.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="9" style="fill:{FILL};stroke:{STROKE};stroke-width:1.2"/>')
                counters += 1
                if k in fr.get("crossed", []):
                    d = 9
                    for x1, y1, x2, y2 in ((cx - d, cy - d, cx + d, cy + d), (cx - d, cy + d, cx + d, cy - d)):
                        body.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" '
                                    f'style="stroke:{STROKE};stroke-width:3;stroke-linecap:round"/>')
                    crosses += 1
        meta_frames.append({"boxes": boxes, "counters": counters, "crossed": crosses,
                            "empty_boxes": boxes - counters})
    counters = sum(m["counters"] for m in meta_frames)
    crossed = sum(m["crossed"] for m in meta_frames)
    meta = {"frames": meta_frames, "counters": counters, "crossed": crossed, "left": counters - crossed}
    return _svg(PAD * 2 + 2 * box, body, title), meta


# ---------------------------------------------------------------- difference: two rows matched in pairs
def compare_rows(top: int, bottom: int, title: str):
    """Top row and bottom row line up column by column. Each matched pair is joined by
    a dashed line. Counters with no partner sit inside a dashed box."""
    step = 28
    n = max(top, bottom)
    x0 = W / 2 - (n - 1) * step / 2
    y_top, y_bot = PAD + 14, PAD + 14 + 52
    body, pairs = [], 0
    for k in range(min(top, bottom)):
        x = x0 + k * step
        body.append(f'<line x1="{_f(x)}" y1="{_f(y_top + R + 2)}" x2="{_f(x)}" y2="{_f(y_bot - R - 2)}" '
                    f'style="stroke:{MUTED};stroke-width:1.5;stroke-dasharray:4 3"/>')
        pairs += 1
    rows = []
    for y, count in ((y_top, top), (y_bot, bottom)):
        drawn = 0
        for k in range(count):
            _counter(x0 + k * step, y, body)
            drawn += 1
        rows.append(drawn)
    extra = abs(rows[0] - rows[1])
    if extra:
        y = y_top if rows[0] > rows[1] else y_bot
        bx = x0 + pairs * step - step / 2 + 2
        body.append(f'<rect x="{_f(bx)}" y="{_f(y - R - 5)}" width="{_f(extra * step - 4)}" height="{_f(2 * R + 10)}" '
                    f'rx="8" style="fill:none;stroke:{POINT};stroke-width:2.5;stroke-dasharray:5 4"/>')
    meta = {"top_row": rows[0], "bottom_row": rows[1], "pairs": pairs, "extra": extra,
            "extra_in": "top" if rows[0] > rows[1] else ("bottom" if extra else None)}
    return _svg(PAD * 2 + 28 + 52, body, title), meta


# ---------------------------------------------------------------- number line with hops
def _hops(y, start, end, origin, hops, body):
    """Hops of 1 from `origin`: negative = back, positive = forward. Returns meta
    with the landing point read back from where the last arc ends."""
    x0, x1 = PAD + 10, W - PAD - 10
    unit = F(x1 - x0) / (end - start)
    to_x = lambda v: x0 + (F(v) - start) * unit  # noqa: E731
    sign = 1 if hops > 0 else -1
    v, drawn, end_x = F(origin), 0, None
    for _ in range(abs(hops)):
        a, b = to_x(v), to_x(v + sign)
        mid = (a + b) / 2
        body.append(f'<path d="M{_f(a)},{_f(y - 6)} Q{_f(mid)},{_f(y - 30)} {_f(b)},{_f(y - 6)}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2"/>')
        # small arrow head at the end of each hop
        body.append(f'<path d="M{_f(b)},{_f(y - 6)} L{_f(b - sign * 7)},{_f(y - 12)} L{_f(b - sign * 2)},{_f(y - 14)} Z" '
                    f'style="fill:{POINT};stroke:{POINT};stroke-width:1"/>')
        drawn += 1
        end_x = b
        v += sign
    meta = {"hops": drawn, "direction": "back" if sign < 0 else "forward"}
    if end_x is not None:
        land = start + (end_x - x0) / unit
        # filled landing dot, drawn exactly as in s0-addition-meaning
        body.append(f'<circle cx="{_f(end_x)}" cy="{_f(y)}" r="7" style="fill:{FILL};stroke:{STROKE};stroke-width:1.5"/>')
        meta["lands_on"] = str(land)
    return meta


def hop_lines(lines: list[dict], title: str):
    """lines: [{"start": 0, "end": 10, "from": 9, "hops": -3}]. hops 0 = only the dot."""
    body, metas = [], []
    gap = 90
    for i, ln in enumerate(lines):
        y = F(PAD + 34 + i * gap)
        m = draw._number_line(y, F(ln["start"]), F(ln["end"]), 1, "wholes", F(ln["from"]), body)
        m = {"start": m["start"], "end": m["end"], "spaces_per_unit": m["spaces_per_unit"], "from": m["point"]}
        if ln["hops"]:
            m.update(_hops(y, F(ln["start"]), F(ln["end"]), ln["from"], ln["hops"], body))
        else:
            m["hops"] = 0
        metas.append(m)
    h = PAD + 34 + (len(lines) - 1) * gap + 44
    return _svg(h, body, title), {"lines": metas}


# ---------------------------------------------------------------- the diagrams
draw.save(OUT, "sm-take-away", *crossed_row(8, 3, "8 mangoes, 3 crossed out"))
draw.save(OUT, "sm-compare", *compare_rows(7, 4, "A row of 7 and a row of 4 matched in pairs"))
draw.save(OUT, "sm-hops", *hop_lines([
    {"start": 0, "end": 10, "from": 9, "hops": -3},
    {"start": 0, "end": 10, "from": 4, "hops": 3},
], "Count back 3 from 9; count on from 4 to 7"))
draw.save(OUT, "sm-check-12", *ten_frames([
    {"filled": 10, "crossed": [5, 6, 7, 8, 9]},
    {"filled": 2},
], "Two ten-frames: 12 counters, 5 crossed out"))
draw.save(OUT, "sm-order", *crossed_row(3, 0, "3 laddoos"))
# practice
draw.save(OUT, "sm-p1", *crossed_row(6, 2, "6 birds, 2 crossed out"))
draw.save(OUT, "sm-p2", *ten_frames([{"filled": 9, "crossed": [5, 6, 7, 8]}], "Ten-frame: 9 counters, 4 crossed out"))
draw.save(OUT, "sm-p3", *compare_rows(9, 6, "A row of 9 and a row of 6 matched in pairs"))
draw.save(OUT, "sm-p4", *hop_lines([{"start": 5, "end": 15, "from": 12, "hops": 0}], "Number line 5 to 15, dot at 12"))
# quiz
draw.save(OUT, "sm-q1", *crossed_row(10, 7, "10 laddoos, 7 crossed out"))
draw.save(OUT, "sm-q2", *compare_rows(8, 3, "A row of 8 and a row of 3 matched in pairs"))
draw.save(OUT, "sm-q3", *hop_lines([{"start": 0, "end": 10, "from": 6, "hops": 0}], "Number line 0 to 10, dot at 6"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-subtraction-meaning")
