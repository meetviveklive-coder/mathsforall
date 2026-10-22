"""Diagrams for s0-equivalent-fractions. Run from repo root."""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402

OUT = Path(__file__).resolve().parent
EQ = lambda n: [1] * n  # noqa: E731
draw.save(OUT, "eq-half-bars", *draw.bars([
    {"weights": EQ(2), "shaded": [0], "label": "1/2"},
    {"weights": EQ(4), "shaded": [0, 1], "label": "2/4"},
    {"weights": EQ(8), "shaded": [0, 1, 2, 3], "label": "4/8"},
], "One half, two quarters and four eighths"))
draw.save(OUT, "eq-nl", *draw.stacked_number_lines([
    {"spu": 2, "labels": "all", "point": F(1, 2)},
    {"spu": 4, "labels": "all", "point": F(2, 4)},
], "Halves and quarters number lines"))
draw.save(OUT, "eq-p1", *draw.bars([
    {"weights": EQ(3), "shaded": [0]},
    {"weights": EQ(6), "shaded": [0, 1]},
], "One third and two sixths"))
draw.save(OUT, "eq-q4", *draw.stacked_number_lines([
    {"spu": 3, "point": F(2, 3)},
    {"spu": 6, "point": F(4, 6)},
], "Thirds and sixths number lines"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-equivalent-fractions")
