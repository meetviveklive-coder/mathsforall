"""Diagrams for s0-add-sub-unlike-fractions. Run from repo root."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402

OUT = Path(__file__).resolve().parent
EQ = lambda n: [1] * n  # noqa: E731
draw.save(OUT, "ul-half-third", *draw.bars([
    {"weights": EQ(2), "shaded": [0], "label": "1/2"},
    {"weights": EQ(3), "shaded": [0], "label": "1/3"},
], "One half and one third: pieces of different sizes"))
draw.save(OUT, "ul-sixths", *draw.bars([
    {"weights": EQ(6), "shaded": [0, 1, 2], "label": "3/6"},
    {"weights": EQ(6), "shaded": [0, 1], "label": "2/6"},
    {"weights": EQ(6), "shaded": [0, 1, 2, 3, 4], "label": "5/6"},
], "Three sixths plus two sixths makes five sixths"))
draw.save(OUT, "ul-p1", *draw.bars([
    {"weights": EQ(4), "shaded": [0, 1]},
    {"weights": EQ(4), "shaded": [0]},
], "Two quarters and one quarter"))
draw.save(OUT, "ul-not-2-5", *draw.bars([
    {"weights": EQ(2), "shaded": [0], "label": "1/2"},
    {"weights": EQ(5), "shaded": [0, 1], "label": "2/5"},
], "One half and two fifths"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-add-sub-unlike-fractions")
