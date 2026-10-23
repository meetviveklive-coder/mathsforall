"""Diagrams for s0-ratio. Run from repo root.

Two helpers, kept here (not in tools/draw.py):
- ratio_blocks: one row of equal blocks per person or item ("bar model"). Every
  block in every row has the same size, so a row of 3 blocks is exactly 3 parts.
  Optional text inside each block (the value of one part, like "₹100") and an
  optional total line under the rows.
- parts_bar: ONE bar cut into equal blocks, split into named groups, to show that
  in 2 : 3 the first amount is 2 parts out of 5 (2/5 of the whole), not 2/3.

Both follow draw.py's rule: the meta is read back from the finished SVG text
(rect positions and sizes, text inside blocks), not copied from the request.
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, PAD, POINT, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

BLOCK_RE = re.compile(r'<rect class="blk r(\d+)" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"')
LABEL_RE = re.compile(r'<text class="lab r(\d+)"[^>]*>([^<]*)</text>')
VALUE_RE = re.compile(r'<text class="val r(\d+) b(\d+)"[^>]*>([^<]*)</text>')
TOTAL_RE = re.compile(r'<text class="total"[^>]*>([^<]*)</text>')
GROUP_RE = re.compile(r'<text class="grp g(\d+)"[^>]*>([^<]*)</text>')


def _cls(svg_text: str, cls: str) -> str:
    """Give a <text> element a class so the meta can find it again."""
    return svg_text.replace("<text ", f'<text class="{cls}" ', 1)


def _num(s: str) -> F:
    """The number in a block or total text: '₹100' -> 100, '1 cup' -> 1."""
    m = re.search(r"\d[\d,]*(?:\.\d+)?", s)
    return F(m.group(0).replace(",", ""))


# ---------------------------------------------------------------- bar model, one row each
def ratio_blocks(rows: list[dict], title: str, block_text: str | None = None,
                 total_text: str | None = None) -> tuple[str, dict]:
    """rows: [{"label": "Asha", "blocks": 3}]. All blocks have one size."""
    label_w = max(len(r["label"]) for r in rows) * 9 + 14
    x0 = PAD + label_w
    most = max(r["blocks"] for r in rows)
    bw = min(F(60), F(W - PAD - x0) / most)
    bh, gap = 40, 16
    body: list[str] = []
    for i, r in enumerate(rows):
        y = PAD + i * (bh + gap)
        body.append(_cls(_text(PAD, y + bh / 2 + 5, r["label"], 15, anchor="start", weight="700"), f"lab r{i}"))
        for b in range(r["blocks"]):
            x = x0 + b * bw
            body.append(f'<rect class="blk r{i}" x="{_f(x)}" y="{_f(y)}" width="{_f(bw)}" height="{bh}" '
                        f'style="fill:{FILL if i % 2 == 0 else EMPTY};stroke:{STROKE};stroke-width:1.5"/>')
            if block_text:
                body.append(_cls(_text(x + bw / 2, y + bh / 2 + 5, block_text, 14, weight="700"), f"val r{i} b{b}"))
    y_end = PAD + len(rows) * bh + (len(rows) - 1) * gap
    if total_text:
        body.append(_cls(_text(W / 2, y_end + 28, total_text, 15, weight="700", color=POINT), "total"))
        y_end += 34
    svg = _svg(y_end + PAD, body, title)

    # ---- read the facts back from the SVG text
    blocks = BLOCK_RE.findall(svg)
    labels = {int(i): s for i, s in LABEL_RE.findall(svg)}
    values = VALUE_RE.findall(svg)
    sizes = {(w, h) for _, _, _, w, h in blocks}
    meta_rows = []
    for i in sorted(labels):
        mine = [b for b in blocks if int(b[0]) == i]
        xs = sorted(F(b[1]) for b in mine)
        touching = all(xs[k + 1] - xs[k] == F(mine[0][3]) for k in range(len(xs) - 1))
        row = {"label": labels[i], "blocks": len(mine), "touching": touching}
        vals = {v for r, _, v in values if int(r) == i}
        if vals:
            assert len(vals) == 1
            one = _num(vals.pop())
            row["block_value"] = str(one)
            row["row_value"] = str(one * len(mine))
        meta_rows.append(row)
    meta = {"rows": meta_rows, "equal": len(sizes) == 1, "total_blocks": len(blocks),
            "ratio": " : ".join(str(r["blocks"]) for r in meta_rows)}
    tot = TOTAL_RE.findall(svg)
    if tot:
        meta["total_text"] = tot[0]
    if values:
        meta["sum_of_rows"] = str(sum(_num(r["row_value"]) for r in meta_rows))
    return svg, meta


# ---------------------------------------------------------------- one bar, parts of the whole
def parts_bar(groups: list[dict], title: str) -> tuple[str, dict]:
    """groups: [{"label": "Yellow", "blocks": 2}, ...]. One bar of equal blocks."""
    n = sum(g["blocks"] for g in groups)
    x0, x1 = F(PAD), F(W - PAD)
    bw = (x1 - x0) / n
    bh = 44
    top = F(PAD + 26)
    body = [_text(W / 2, PAD + 10, f"{n} equal parts in all", 15, weight="700", color=POINT)]
    k = 0
    for gi, g in enumerate(groups):
        gx0 = x0 + k * bw
        for _ in range(g["blocks"]):
            x = x0 + k * bw
            body.append(f'<rect class="blk r{gi}" x="{_f(x)}" y="{_f(top)}" width="{_f(bw)}" height="{bh}" '
                        f'style="fill:{FILL if gi % 2 == 0 else EMPTY};stroke:{STROKE};stroke-width:1.5"/>')
            k += 1
        gx1 = x0 + k * bw
        by = top + bh + 10
        # bracket under the group
        body.append(f'<path d="M{_f(gx0 + 3)},{_f(by - 4)} L{_f(gx0 + 3)},{_f(by)} L{_f(gx1 - 3)},{_f(by)} '
                    f'L{_f(gx1 - 3)},{_f(by - 4)}" style="fill:none;stroke:{TEXT};stroke-width:1.5"/>')
        mid = (gx0 + gx1) / 2
        body.append(_cls(_text(mid, by + 20, g["label"], 15, weight="700"), f"lab r{gi}"))
        word = "part" if g["blocks"] == 1 else "parts"
        body.append(_cls(_text(mid, by + 40, f'{g["blocks"]} {word}', 14), f"grp g{gi}"))
    h = top + bh + 10 + 40 + PAD
    svg = _svg(h, body, title)

    blocks = BLOCK_RE.findall(svg)
    labels = {int(i): s for i, s in LABEL_RE.findall(svg)}
    sizes = {(w, hh) for _, _, _, w, hh in blocks}
    xs = sorted(F(b[1]) for b in blocks)
    width_all = sum(F(b[3]) for b in blocks)
    one_bar = all(xs[i + 1] - xs[i] == F(blocks[0][3]) for i in range(len(xs) - 1)) and len({b[2] for b in blocks}) == 1
    metas = []
    for i in sorted(labels):
        mine = [b for b in blocks if int(b[0]) == i]
        metas.append({"label": labels[i], "blocks": len(mine),
                      "fraction_of_whole": str(sum(F(b[3]) for b in mine) / width_all)})
    meta = {"one_bar": one_bar, "equal": len(sizes) == 1, "total_blocks": len(blocks), "groups": metas,
            "ratio": " : ".join(str(g["blocks"]) for g in metas)}
    return svg, meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "rt-rice-dal", *ratio_blocks(
    [{"label": "Rice", "blocks": 2}, {"label": "Dal", "blocks": 1}],
    "Two cups of rice and one cup of dal", block_text="1 cup"))
draw.save(OUT, "rt-paint-parts", *parts_bar(
    [{"label": "Yellow", "blocks": 2}, {"label": "Red", "blocks": 3}],
    "Yellow and red paint in the ratio 2 to 3, as one bar of 5 equal parts"))
draw.save(OUT, "rt-share-500", *ratio_blocks(
    [{"label": "Asha", "blocks": 3}, {"label": "Tenzing", "blocks": 2}],
    "Five hundred rupees shared in the ratio 3 to 2", block_text="₹100",
    total_text="5 equal parts make ₹500"))
draw.save(OUT, "rt-p2", *ratio_blocks(
    [{"label": "Red", "blocks": 4}, {"label": "White", "blocks": 3}],
    "Cups of red and white rangoli powder", block_text="1 cup"))
draw.save(OUT, "rt-p6", *parts_bar(
    [{"label": "Blue", "blocks": 3}, {"label": "White", "blocks": 4}],
    "Blue and white paint in the ratio 3 to 4, as one bar of 7 equal parts"))
draw.save(OUT, "rt-p7", *ratio_blocks(
    [{"label": "Ishita", "blocks": 2}, {"label": "Kunal", "blocks": 1}],
    "Twelve laddoos shared in the ratio 2 to 1", total_text="3 equal parts make 12 laddoos"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-ratio")
