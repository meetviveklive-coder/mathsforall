"""Diagrams for s0-divide-fractions. Run from repo root.

New helper `hops`: a number line with equal hops drawn as arcs from 0, showing
"how many times does this fraction fit into that number". The meta (hop sizes,
number of full hops, size of the last part-hop) is read back from the drawn
arc end points, not copied from the request.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import PAD, POINT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent
EQ = lambda n: [1] * n  # noqa: E731


def hops(end, spu, hop, title, labels="wholes", line_end=None):
    """Number line 0..end with spu spaces per unit, a dot at `end`, and hops of size `hop`
    from 0. Full hops are solid arcs numbered 1, 2, 3...; a last part-hop (if the hop does
    not fit exactly) is a dashed arc."""
    end, hop = F(end), F(hop)
    line_end = F(line_end) if line_end is not None else end
    body: list[str] = []
    y = F(PAD + 52)
    line_meta = draw._number_line(y, F(0), line_end, spu, labels, end, body)
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    unit_px = (x1 - x0) / line_end
    # arc end points in pixels
    xs = [x0]
    v = F(0)
    while v + hop <= end:
        v += hop
        xs.append(x0 + v * unit_px)
    full_px = len(xs) - 1
    if v < end:
        xs.append(x0 + end * unit_px)
    sizes = []  # read back from the drawn pixels
    for i in range(len(xs) - 1):
        a, b = xs[i], xs[i + 1]
        size = (b - a) / unit_px
        sizes.append(size)
        full = i < full_px
        mid = (a + b) / 2
        rise = 30 if full else 30 * size / hop
        body.append(f'<path d="M{_f(a)},{_f(y - 3)} Q{_f(mid)},{_f(y - 3 - 2 * rise)} {_f(b)},{_f(y - 3)}" '
                    f'style="fill:none;stroke:{POINT};stroke-width:2;'
                    f'{"" if full else "stroke-dasharray:4 3"}"/>')
        if full:
            body.append(_text(mid, y - 3 - rise - 6, str(i + 1), 14, weight="600", color=POINT))
    hop_px = sizes[0] if sizes else None
    n_full = sum(1 for s in sizes if s == hop_px)
    part = (sizes[-1] / hop_px) if sizes and sizes[-1] != hop_px else F(0)
    meta = {"start": line_meta["start"], "end": line_meta["end"],
            "spaces_per_unit": line_meta["spaces_per_unit"], "labels": line_meta["labels"],
            "point": line_meta.get("point"), "hop": str(hop_px), "full_hops": n_full,
            "part_hop": str(part)}
    return _svg(y + 48, body, title), meta


draw.save(OUT, "dv-hops-3-halves", *hops(3, 2, F(1, 2), "Hops of one half from 0 to 3"))
draw.save(OUT, "dv-hops-34-half", *hops(F(3, 4), 4, F(1, 2), "Hops of one half from 0 to three quarters",
                                          labels="all", line_end=1))
draw.save(OUT, "dv-hops-3-twothirds", *hops(3, 3, F(2, 3), "Hops of two thirds from 0 to 3"))
def tinted_bars(rows: list[dict], title: str):
    """Like draw.bars, but each row may also list `tinted` parts, drawn in a light shade.
    Draws with draw.bars (all parts empty), then sets each part's fill in drawing order.
    The meta (dark parts as `shaded`, light parts as `tinted`) is read back from the final SVG."""
    from draw import EMPTY, FILL, STROKE
    svg, _ = draw.bars([{**r, "shaded": []} for r in rows], title)
    empty = f"fill:{EMPTY};stroke:{STROKE}"
    dark_style = f"fill:{FILL};stroke:{STROKE}"
    light_style = f"fill:{FILL};fill-opacity:0.32;stroke:{STROKE}"
    styles = []
    for r in rows:
        for k in range(len(r["weights"])):
            if k in r.get("shaded", []):
                styles.append(dark_style)
            elif k in r.get("tinted", []):
                styles.append(light_style)
            else:
                styles.append(empty)
    parts = svg.split(empty)
    assert len(parts) == len(styles) + 1
    svg = parts[0] + "".join(st + rest for st, rest in zip(styles, parts[1:]))
    cells = [c.split("/>")[0] for c in svg.split("<rect ")[1:]]
    meta_bars, i0 = [], 0
    for r in rows:
        row = cells[i0:i0 + len(r["weights"])]
        i0 += len(row)
        widths = {c.split('width="')[1].split('"')[0] for c in row}
        meta_bars.append({"parts": len(row), "equal": len(widths) == 1,
                          "shaded": sum(dark_style in c for c in row),
                          "tinted": sum(light_style in c for c in row)})
    return svg, {"bars": meta_bars}


draw.save(OUT, "dv-share-half", *tinted_bars([
    {"weights": EQ(2), "shaded": [0], "label": "1/2"},
    {"weights": EQ(6), "shaded": [0], "tinted": [1, 2], "label": "1/6"},
], "One half shared into 3 equal pieces"))
draw.save(OUT, "dv-p1", *hops(2, 4, F(1, 4), "Hops of one quarter from 0 to 2"))
draw.save(OUT, "dv-q1", *hops(2, 3, F(2, 3), "Hops of two thirds from 0 to 2"))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-divide-fractions")
