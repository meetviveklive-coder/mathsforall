"""Diagrams for s0-fractions-decimals-conversion. Run from repo root.

Adds one helper (kept here, not in tools/draw.py):
- double_line: two parallel number lines from 0 to 1. The top line is cut into
  fractions and labelled above. The bottom line is cut into decimal steps and
  labelled below. A dashed guide joins each top mark to a bottom mark at the same x.

It follows draw.py's rule: the meta is read back from what was drawn. Every
label's value is worked out from its x position, and the pairs of marks that
line up are found by comparing the drawn x positions, not copied from the request.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, MUTED, PAD, POINT, STROKE, TEXT, W, _f, _frac_label, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent


def _dec(value: F) -> str:
    """Write a fraction with denominator 10, 100 or 1000 as a decimal string ('0.25', '1')."""
    for places in range(0, 4):
        if (value * 10 ** places).denominator == 1:
            if places == 0:
                return str(value.numerator)
            whole, frac = divmod(int(value * 10 ** places), 10 ** places)
            return f"{whole}.{frac:0{places}d}"
    raise ValueError(value)


def double_line(top_spu: int, bottom_spu: int, title: str, top_marks=None, top_point=None,
                blank=None, bottom_skip=()) -> tuple[str, dict]:
    """top_marks: the k values (k/top_spu) to label on the top line; None means every mark between 0 and 1.
    blank: a value on the bottom line drawn as a '?' box instead of its decimal.
    bottom_skip: bottom values left unlabelled."""
    x0, x1 = F(PAD + 10), F(W - PAD - 10)
    unit = x1 - x0
    y_top, y_bot = F(PAD + 44), F(PAD + 112)
    body = []

    def x_of(v: F) -> F:
        return x0 + unit * v

    def value_at(x: F) -> F:
        return (x - x0) / unit

    for y in (y_top, y_bot):
        body.append(f'<line x1="{_f(x0)}" y1="{_f(y)}" x2="{_f(x1)}" y2="{_f(y)}" style="stroke:{STROKE};stroke-width:2"/>')

    # top line: fractions above
    top_ticks, top_labels = [], []  # (x, label)
    if top_marks is None:
        top_marks = range(1, top_spu)
    for k in range(top_spu + 1):
        v = F(k, top_spu)
        x = x_of(v)
        whole = v.denominator == 1
        h = 10 if whole else 7
        body.append(f'<line x1="{_f(x)}" y1="{_f(y_top - h)}" x2="{_f(x)}" y2="{_f(y_top + h)}" '
                    f'style="stroke:{STROKE};stroke-width:{2 if whole else 1.5}"/>')
        top_ticks.append(x)
        if whole:
            body.append(_text(x, y_top - 18, str(v.numerator), 14, weight="700"))
        elif k in top_marks:
            body.append(_frac_label(x, y_top - 36, k, top_spu, 13))
            top_labels.append((x, f"{k}/{top_spu}"))
    if top_point is not None:
        px = x_of(F(top_point))
        body.append(f'<circle cx="{_f(px)}" cy="{_f(y_top)}" r="7" style="fill:{POINT};stroke:{EMPTY};stroke-width:2"/>')

    # bottom line: decimals below
    bot_ticks, bot_labels = [], []  # (x, label)
    blank_x = None
    for k in range(bottom_spu + 1):
        v = F(k, bottom_spu)
        x = x_of(v)
        whole = v.denominator == 1
        h = 10 if whole else 7
        body.append(f'<line x1="{_f(x)}" y1="{_f(y_bot - h)}" x2="{_f(x)}" y2="{_f(y_bot + h)}" '
                    f'style="stroke:{STROKE};stroke-width:{2 if whole else 1.5}"/>')
        bot_ticks.append(x)
        if blank is not None and v == F(blank):
            body.append(f'<rect x="{_f(x - 13)}" y="{_f(y_bot + 13)}" width="26" height="24" rx="4" '
                        f'style="fill:none;stroke:{POINT};stroke-width:1.8;stroke-dasharray:4 3"/>')
            body.append(_text(x, y_bot + 31, "?", 16, weight="700", color=POINT))
            blank_x = x
            continue
        if v in {F(s) for s in bottom_skip}:
            continue
        lab = _dec(v)
        size = 14 if bottom_spu <= 5 else 13
        body.append(_text(x, y_bot + 30, lab, size, weight="700" if whole else "400",
                          color=TEXT if whole else POINT))
        bot_labels.append((x, lab))

    # dashed guides where a labelled top mark sits exactly above a bottom mark
    bot_by_x = {x: lab for x, lab in bot_labels}
    bot_tick_set = set(bot_ticks)
    pairs, unmatched, between = [], [], {}
    for x, lab in [(top_ticks[0], "0")] + top_labels + [(top_ticks[-1], "1")]:
        if x in bot_tick_set:
            body.append(f'<line x1="{_f(x)}" y1="{_f(y_top + 11)}" x2="{_f(x)}" y2="{_f(y_bot - 11)}" '
                        f'style="stroke:{MUTED};stroke-width:1.5;stroke-dasharray:4 4"/>')
            pairs.append([lab, bot_by_x.get(x, "?" if x == blank_x else None)])
        else:
            unmatched.append(lab)
            left = max(b for b in bot_labels if b[0] < x)
            right = min(b for b in bot_labels if b[0] > x)
            between[lab] = [left[1], right[1]]

    def spu(ticks):
        gaps = {ticks[i + 1] - ticks[i] for i in range(len(ticks) - 1)}
        return len(ticks) - 1 if len(gaps) == 1 else None

    meta = {
        "start": "0", "end": "1",
        "top": {"spaces_per_unit": spu(top_ticks), "labels": [lab for _, lab in top_labels],
                "labels_at_own_value": all(F(lab) == value_at(x) for x, lab in top_labels)},
        "bottom": {"spaces_per_unit": spu(bot_ticks), "labels": [lab for _, lab in bot_labels],
                   "labels_at_own_value": all(F(lab) == value_at(x) for x, lab in bot_labels)},
        "lined_up": pairs,
        "lined_up_equal": all(b is None or b == "?" or F(a) == F(b) for a, b in pairs),
        "not_lined_up": unmatched,
        "between": between,
    }
    if blank_x is not None:
        meta["blank_at"] = str(value_at(blank_x))
    if top_point is not None:
        meta["point"] = str(value_at(x_of(F(top_point))))
    return _svg(y_bot + 46, body, title), meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "fd-quarters", *double_line(
    4, 4, "Quarters as fractions and as decimals", top_marks=[1, 2, 3]))
draw.save(OUT, "fd-thirds", *double_line(
    3, 10, "Thirds above a number line in tenths"))
draw.save(OUT, "fd-p4", *double_line(
    5, 5, "Fifths as fractions and decimals, one decimal missing", blank=F(3, 5)))
draw.save(OUT, "fd-q8", *double_line(
    6, 10, "A dot at five sixths above a number line in tenths", top_marks=[5], top_point=F(5, 6)))
print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-fractions-decimals-conversion")
