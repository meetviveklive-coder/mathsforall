"""Diagrams for s0-percent-of-quantity. Run from repo root.

Adds one helper (kept here, not in tools/draw.py):
- percent_bar: one bar is the whole (100%). It is cut into ten equal 10% parts.
  The amount of one part is written under each part, and a caption says "Each part is 10%."
  A bracket above the bar names the whole amount. Part of the bar is shaded
  (whole parts, or a whole number of half parts for 5% steps). A bracket under the
  shaded part names it, or shows "?" when the amount is the question.

It follows draw.py's rule: the meta is read back from what was actually drawn.
Part widths, the shaded width and the amounts are parsed from the finished SVG text,
not copied from the request. The helper also asserts that the labels it wrote agree
with the drawing (the part amounts add up to the whole, and the shaded label equals
the shaded share of the whole).
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, PAD, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

PART_RECT = re.compile(r'<rect class="part" x="([\d.]+)" y="[\d.]+" width="([\d.]+)"')
SHADE_RECT = re.compile(r'<rect class="shade" x="([\d.]+)" y="[\d.]+" width="([\d.]+)"')
GROUP_TEXT = r'<g class="{}">(.*?)</g>'
TEXT_BODY = re.compile(r">([^<]*)</text>")


def _num(v: F) -> str:
    """Write a value with at most 2 decimal places, as a child would ('24', '4.5', '12.25')."""
    for places in range(0, 3):
        if (v * 10 ** places).denominator == 1:
            if places == 0:
                return str(v.numerator)
            n = int(v * 10 ** places)
            whole, frac = divmod(n, 10 ** places)
            return f"{whole}.{frac:0{places}d}"
    raise ValueError(f"{v} needs more than 2 decimal places")


def _amount(v: F, unit: str) -> str:
    """'₹90', '84 km', '14 people'."""
    if unit == "₹":
        return f"₹{_num(v)}"
    return f"{_num(v)} {unit}"


def _parse_amount(s: str) -> F:
    return F(s.replace("₹", "").split(" ")[0])


def _group_texts(svg: str, cls: str) -> list[str]:
    m = re.search(GROUP_TEXT.format(cls), svg)
    return TEXT_BODY.findall(m.group(1)) if m else []


def _bracket(x0, x1, y, down: bool) -> str:
    """A square bracket from x0 to x1. Its end ticks point down (above the bar) or up (below)."""
    t = 7 if down else -7
    return (f'<path d="M{_f(x0)},{_f(y + t)} L{_f(x0)},{_f(y)} L{_f(x1)},{_f(y)} L{_f(x1)},{_f(y + t)}" '
            f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')


def _label_x(cx, s: str, size: int) -> F:
    """Keep a centred label inside the viewBox."""
    half = F(len(s) * size * 6, 10) / 2  # rough text width: 0.6 em per character
    return max(F(PAD) + half, min(F(W - PAD) - half, F(cx)))


def percent_bar(whole: int | F, unit: str, shaded_percent: int | F, title: str,
                ask: bool = False) -> tuple[str, dict]:
    """whole: the amount that is 100%. shaded_percent: a multiple of 5.
    ask=True writes "?" for the shaded amount instead of the answer."""
    whole, shaded_percent = F(whole), F(shaded_percent)
    assert shaded_percent % 5 == 0 and 0 < shaded_percent <= 100
    parts = 10
    x0, x1 = F(PAD), F(W - PAD)
    pw = (x1 - x0) / parts
    top_label_y = F(PAD + 14)
    top_br_y = top_label_y + 10
    bar_y = top_br_y + 10
    bar_h = 36
    amt_y = bar_y + bar_h + 20
    bot_br_y = amt_y + 10
    bot_label_y = bot_br_y + 22

    body = []
    # whole bracket and label above the bar
    whole_label = f"100% = {_amount(whole, unit)}"
    body.append(f'<g class="whole">{_text(W / 2, top_label_y, whole_label, 15, weight="700")}</g>')
    body.append(_bracket(x0, x1, top_br_y, down=True))
    # shading first, so the part outlines and the "10%" text sit on top
    shaded_w = (x1 - x0) * shaded_percent / 100
    body.append(f'<rect class="shade" x="{_f(x0)}" y="{_f(bar_y)}" width="{_f(shaded_w)}" height="{bar_h}" '
                f'style="fill:{FILL};stroke:none"/>')
    for k in range(parts):
        body.append(f'<rect class="part" x="{_f(x0 + k * pw)}" y="{_f(bar_y)}" width="{_f(pw)}" height="{bar_h}" '
                    f'style="fill:none;stroke:{STROKE};stroke-width:1.5"/>')
    body.append(f'<rect x="{_f(x0)}" y="{_f(bar_y)}" width="{_f(x1 - x0)}" height="{bar_h}" '
                f'style="fill:none;stroke:{STROKE};stroke-width:2.5"/>')
    # the amount of each part, underneath
    part_amount = whole / parts
    s = _num(part_amount)
    assert len(s) <= 3, f"part amount {s!r} is too wide for a 10% cell at 14px"
    amt_texts = "".join(_text(x0 + (k + F(1, 2)) * pw, amt_y, s, 14) for k in range(parts))
    body.append(f'<g class="amt">{amt_texts}</g>')
    # bracket and label under the shaded part
    body.append(_bracket(x0, x0 + shaded_w, bot_br_y, down=False))
    shaded_amount = whole * shaded_percent / 100
    shaded_label = f"{_num(shaded_percent)}% = {'?' if ask else _amount(shaded_amount, unit)}"
    body.append(f'<g class="shaded">{_text(_label_x(x0 + shaded_w / 2, shaded_label, 15), bot_label_y, shaded_label, 15, weight="700")}</g>')
    cap_y = bot_label_y + 28
    caption = f"Each part is {F(100, parts)}%."
    body.append(f'<g class="pct">{_text(W / 2, cap_y, caption, 14, color=TEXT)}</g>')
    svg = _svg(cap_y + PAD - 4, body, title)

    # ---- read the facts back from the drawn SVG
    rects = [(F(x), F(w)) for x, w in PART_RECT.findall(svg)]
    widths = {w for _, w in rects}
    bar_w = sum(w for _, w in rects)
    (sx, sw), = [(F(x), F(w)) for x, w in SHADE_RECT.findall(svg)]
    drawn_pct = (sw / bar_w * 100).limit_denominator(1000)
    amounts = [F(t) for t in _group_texts(svg, "amt")]
    pcts = _group_texts(svg, "pct")
    drawn_whole = sum(amounts)
    whole_text = _group_texts(svg, "whole")[0]
    shaded_text = _group_texts(svg, "shaded")[0]
    # the labels must agree with the drawing
    assert _parse_amount(whole_text.split("= ")[1]) == drawn_whole
    assert pcts == [f"Each part is {F(100, len(rects))}%."]
    assert sx == rects[0][0]  # shading starts at the left end
    drawn_shaded_amount = drawn_whole * drawn_pct / 100
    if not ask:
        assert _parse_amount(shaded_text.split("= ")[1]) == drawn_shaded_amount
    meta = {
        "parts": len(rects),
        "equal": len(widths) == 1,
        "part_percent": str(F(100, len(rects))),
        "caption": pcts[0],
        "part_amount": _num(amounts[0]) if len(set(amounts)) == 1 else None,
        "whole": _num(drawn_whole),
        "whole_label": whole_text,
        "shaded_percent": _num(drawn_pct),
        "shaded_parts": _num(drawn_pct / F(100, len(rects))),
        "shaded_amount": _num(drawn_shaded_amount),
        "shaded_label": shaded_text,
    }
    return svg, meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "poq-bar-35", *percent_bar(240, "km", 35, "A percent bar: 35% of 240 km is 84 km"))
draw.save(OUT, "poq-bar-25", *percent_bar(360, "₹", 25, "A percent bar: 25% of 360 rupees is 90 rupees"))
draw.save(OUT, "poq-bar-whole", *percent_bar(40, "people", 35, "A percent bar: 14 people out of 40 is 35%"))
draw.save(OUT, "poq-p1", *percent_bar(500, "₹", 30, "A percent bar for 500 rupees with 30% shaded", ask=True))
draw.save(OUT, "poq-q1", *percent_bar(180, "km", 60, "A percent bar for 180 km with 60% shaded", ask=True))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-percent-of-quantity")
