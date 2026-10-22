"""Diagrams for s0-comparing-fractions. Run from repo root."""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402

OUT = Path(__file__).resolve().parent
EQ = lambda n: [1] * n  # noqa: E731


def points_line(spu: int, points: list, title: str):
    """Number line 0 to 1 with several labelled dots. Meta is read back from the drawn dots."""
    body: list[str] = []
    y = F(draw.PAD + 44)
    meta = draw._number_line(y, F(0), F(1), spu, "wholes", None, body)
    x0, x1 = F(draw.PAD + 10), F(draw.W - draw.PAD - 10)
    unit_px = x1 - x0
    drawn = []
    for p in points:
        p = F(p)
        px = x0 + p * unit_px
        body.append(f'<circle cx="{draw._f(px)}" cy="{draw._f(y)}" r="7" '
                    f'style="fill:{draw.POINT};stroke:{draw.EMPTY};stroke-width:2"/>')
        body.append(draw._frac_label(px, y - 34, p.numerator, p.denominator, 14))
        drawn.append((px, f"{p.numerator}/{p.denominator}", (px - x0) / unit_px))
    drawn.sort()
    meta = {"start": meta["start"], "end": meta["end"], "spaces_per_unit": meta["spaces_per_unit"],
            "labels": meta["labels"],
            "points_left_to_right": [str(v) for _, _, v in drawn],
            "point_labels_left_to_right": [lab for _, lab, _ in drawn]}
    return draw._svg(y + 50, body, title), meta


draw.save(OUT, "cf-same-den", *draw.bars([
    {"weights": EQ(8), "shaded": [0, 1, 2], "label": "3/8"},
    {"weights": EQ(8), "shaded": [0, 1, 2, 3, 4], "label": "5/8"},
], "Three eighths and five eighths"))
draw.save(OUT, "cf-unit", *draw.bars([
    {"weights": EQ(4), "shaded": [0], "label": "1/4"},
    {"weights": EQ(8), "shaded": [0], "label": "1/8"},
], "One quarter and one eighth"))
draw.save(OUT, "cf-twelfths", *draw.bars([
    {"weights": EQ(3), "shaded": [0, 1], "label": "2/3"},
    {"weights": EQ(12), "shaded": list(range(8)), "label": "8/12"},
    {"weights": EQ(4), "shaded": [0, 1, 2], "label": "3/4"},
    {"weights": EQ(12), "shaded": list(range(9)), "label": "9/12"},
], "Two thirds, eight twelfths, three quarters and nine twelfths"))
draw.save(OUT, "cf-order-nl", *points_line(8, [F(5, 8), F(1, 4), F(1, 2)],
                                          "One quarter, one half and five eighths on a number line"))
draw.save(OUT, "cf-p1", *draw.bars([
    {"weights": EQ(5), "shaded": [0, 1]},
    {"weights": EQ(5), "shaded": [0, 1, 2, 3]},
], "Two fifths and four fifths"))
draw.save(OUT, "cf-q2", *draw.bars([
    {"weights": EQ(3), "shaded": [0, 1]},
    {"weights": EQ(5), "shaded": [0, 1]},
], "Two thirds and two fifths"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-comparing-fractions")
