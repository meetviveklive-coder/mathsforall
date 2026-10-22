"""Diagrams for s0-mixed-numbers. Run from repo root."""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402

OUT = Path(__file__).resolve().parent
EQ = lambda n: [1] * n  # noqa: E731
draw.save(OUT, "mx-bars-7-thirds", *draw.bars([
    {"weights": EQ(3), "shaded": [0, 1, 2]},
    {"weights": EQ(3), "shaded": [0, 1, 2]},
    {"weights": EQ(3), "shaded": [0]},
], "Seven thirds: two full bars and one third of a bar"))
draw.save(OUT, "mx-nl-thirds", *draw.number_line(0, 3, 3, "Number line from 0 to 3 in thirds, dot at 7/3",
                                                 labels="all", point=F(7, 3)))
draw.save(OUT, "mx-p6", *draw.number_line(0, 2, 4, "Number line from 0 to 2 in quarters with a dot",
                                          point=F(7, 4)))
draw.save(OUT, "mx-q5", *draw.number_line(0, 3, 4, "Number line from 0 to 3 in quarters with a dot",
                                          point=F(11, 4)))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-mixed-numbers")
