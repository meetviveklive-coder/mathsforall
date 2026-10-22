"""Diagrams for s0-comparing-decimals. Run from repo root.

draw.number_line labels marks as whole numbers or fractions, so this script has
its own small `decimal_line` helper that labels marks as decimals. It reuses
draw.py's colours, _svg and _text, and builds the meta from the drawn positions.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import PAD, W, POINT, STROKE, EMPTY, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent


def dec(x: F) -> str:
    """Exact decimal text for a fraction whose denominator divides a power of 10."""
    x = F(x)
    places = 0
    while (x * 10 ** places).denominator != 1:
        places += 1
        if places > 6:
            raise ValueError(f"{x} is not a short decimal")
    if places == 0:
        return str(x.numerator)
    n = x.numerator * 10 ** places // x.denominator
    s = str(abs(n)).rjust(places + 1, "0")
    return ("-" if n < 0 else "") + s[:-places] + "." + s[-places:]


def decimal_line(start, end, spu, labels, points, title, point_labels=False):
    """Number line from start to end with spu equal spaces per unit.

    labels: the mark values to label below the line (as decimals).
    points: values to mark with a dot; point_labels writes each value above its dot.
    """
    start, end = F(start), F(end)
    y = F(PAD + 34 if point_labels else PAD + 14)
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    unit_px = (x1 - x0) / (end - start)
    body = [f'<line x1="{_f(x0)}" y1="{_f(y)}" x2="{_f(x1)}" y2="{_f(y)}" style="stroke:{STROKE};stroke-width:2"/>']
    label_set = {F(v) for v in labels}
    n_ticks = int((end - start) * spu) + 1
    tick_xs, drawn_labels = [], []
    for k in range(n_ticks):
        value = start + F(k, spu)
        x = x0 + (value - start) * unit_px
        steps = value * spu  # whole number of small steps from 0
        if steps % 10 == 0:
            h, sw = 11, 2
        elif steps % 5 == 0:
            h, sw = 8, 1.5
        else:
            h, sw = 6, 1.2
        body.append(f'<line x1="{_f(x)}" y1="{_f(y - h)}" x2="{_f(x)}" y2="{_f(y + h)}" '
                    f'style="stroke:{STROKE};stroke-width:{sw}"/>')
        tick_xs.append(x)
        if value in label_set:
            lab = dec(value)
            drawn_labels.append(lab)
            body.append(_text(x, y + 31, lab, 14, weight="600"))
    gaps = {tick_xs[i + 1] - tick_xs[i] for i in range(len(tick_xs) - 1)}
    meta = {"start": dec(start), "end": dec(end),
            "spaces_per_unit": int((len(tick_xs) - 1) / (end - start)) if len(gaps) == 1 else None,
            "labels": drawn_labels, "points": []}
    for p in points:
        px = x0 + (F(p) - start) * unit_px
        body.append(f'<circle cx="{_f(px)}" cy="{_f(y)}" r="7" style="fill:{POINT};stroke:{EMPTY};stroke-width:2"/>')
        read_back = start + (px - x0) / unit_px  # value read back from the drawn position
        meta["points"].append(dec(read_back))
        if point_labels:
            body.append(_text(px, y - 16, dec(read_back), 15, weight="700", color=POINT))
    height = y + 50
    return _svg(height, body, title), meta


L = lambda *v: [F(x) for x in v]  # noqa: E731

draw.save(OUT, "cd-jump", *decimal_line("2.3", "2.5", 100, L("2.3", "2.4", "2.5"), L("2.35", "2.4"),
                                        "2.35 and 2.4 on a number line", point_labels=True))
draw.save(OUT, "cd-longer", *decimal_line("0.2", "0.4", 100, L("0.2", "0.3", "0.4"), L("0.25", "0.3"),
                                          "0.25 and 0.3 on a number line", point_labels=True))
draw.save(OUT, "cd-zoom", *decimal_line("2.3", "2.4", 100, L("2.3", "2.4"), L("2.37"),
                                        "2.37 between 2.3 and 2.4", point_labels=True))
draw.save(OUT, "cd-round", *decimal_line("3.6", "3.7", 100, L("3.6", "3.65", "3.7"), L("3.67"),
                                         "3.67 is closer to 3.7", point_labels=True))
# Tenths lines use draw.number_line, so they share one tick style with s0-decimals-meaning.
draw.save(OUT, "cd-p2", *draw.number_line(F(1), F(2), 10, "A dot between 1 and 2", point=F(17, 10)))
draw.save(OUT, "cd-p5", *decimal_line("4.2", "4.3", 100, L("4.2", "4.3"), L("4.28"), "A dot between 4.2 and 4.3"))
draw.save(OUT, "cd-q4", *decimal_line("6.5", "6.6", 100, L("6.5", "6.6"), L("6.53"), "A dot between 6.5 and 6.6"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-comparing-decimals")
