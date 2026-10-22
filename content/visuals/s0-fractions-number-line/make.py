"""Diagrams for s0-fractions-number-line. Run from repo root."""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402

OUT = Path(__file__).resolve().parent
draw.save(OUT, "nl-quarters", *draw.number_line(0, 1, 4, "Number line 0 to 1 in quarters", labels="all"))
draw.save(OUT, "nl-0-2-quarters", *draw.number_line(0, 2, 4, "Number line 0 to 2 in quarters", labels="steps"))
draw.save(OUT, "nl-p1", *draw.number_line(0, 1, 5, "Number line 0 to 1 in 5 spaces", point=F(2, 5)))
draw.save(OUT, "nl-p2", *draw.number_line(0, 1, 8, "Number line 0 to 1 in 8 spaces", point=F(5, 8)))
draw.save(OUT, "nl-p4", *draw.number_line(0, 2, 3, "Number line 0 to 2 in thirds", point=F(4, 3)))
draw.save(OUT, "nl-q1", *draw.number_line(0, 1, 6, "Number line 0 to 1 in 6 spaces", point=F(5, 6)))
draw.save(OUT, "nl-q2", *draw.number_line(0, 1, 10, "Number line 0 to 1 in 10 spaces", point=F(7, 10)))
draw.save(OUT, "nl-q5", *draw.number_line(0, 3, 2, "Number line 0 to 3 in halves", point=F(5, 2)))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-fractions-number-line")
