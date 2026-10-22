"""Diagrams for s0-fractions-meaning. Run from repo root: python3 content/visuals/s0-fractions-meaning/make.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402

OUT = Path(__file__).resolve().parent
EQ = lambda n: [1] * n  # noqa: E731

draw.save(OUT, "v-equal-unequal", *draw.bars([
    {"weights": EQ(4), "shaded": [], "label": "Equal"},
    {"weights": [1, 2, 3, 6], "shaded": [], "label": "Not equal"},
], "Equal and unequal parts"))
draw.save(OUT, "v-bar-3-4", *draw.bars([{"weights": EQ(4), "shaded": [0, 1, 2]}], "Three quarters shaded"))
draw.save(OUT, "v-half-vs-eighth", *draw.bars([
    {"weights": EQ(2), "shaded": [0], "label": "1/2"},
    {"weights": EQ(8), "shaded": [0], "label": "1/8"},
], "One half and one eighth"))
draw.save(OUT, "v-laddoos-12", *draw.dot_groups(3, 4, 1, "12 laddoos in 3 equal groups"))
draw.save(OUT, "v-bar-1-3", *draw.bars([{"weights": EQ(3), "shaded": [0]}], "Bar in 3 equal parts"))
draw.save(OUT, "v-roti-3-8", *draw.roti(8, 3, "Roti in 8 equal slices"))
draw.save(OUT, "v-unequal-4", *draw.bars([{"weights": [5, 1, 1, 1], "shaded": [0]}], "Bar in 4 unequal parts"))
draw.save(OUT, "v-bar-4-7", *draw.bars([{"weights": EQ(7), "shaded": [0, 1, 2, 3]}], "Bar in 7 equal parts"))
draw.save(OUT, "v-unequal-3", *draw.bars([{"weights": [1, 1, 4], "shaded": [0]}], "Bar in 3 unequal parts"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-fractions-meaning")
