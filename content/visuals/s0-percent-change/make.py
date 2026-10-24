"""Diagrams for s0-percent-change. Run from repo root.

Adds one helper (kept here, not in tools/draw.py):
- amount_bars: horizontal bars whose lengths are drawn to scale from rupee amounts.
  Each bar is a row of segments. A segment is "fill" (money that stays), "cut"
  (money taken off, drawn as a dashed empty box) or "extra" (money added on).
  An optional guide marks one amount: a labelled dashed line, in the POINT colour
  on a light halo, that runs from its label at the top down through every bar.

It follows draw.py's rule: every segment and label is first placed as a record with
its position, the SVG is written from those records, and the meta is read back from
the same records (segment values come from the drawn widths, not from the request).
"""
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import draw  # noqa: E402
from draw import EMPTY, FILL, MUTED, PAD, POINT, STROKE, TEXT, W, _f, _svg, _text  # noqa: E402

OUT = Path(__file__).resolve().parent

BAR_H = 34
ROW_LABEL_H = 22   # space above a bar for its row label
SEG_LABEL_H = 24   # space below a bar for its segment labels
ROW_GAP = 14
CHAR_W = 8.2       # rough width of one 14px character, used to keep labels apart
SIZE = 14
GUIDE_OUT = 3     # how far the guide line runs past the bottom of the last bar
GUIDE_GAP = 6     # space kept between the guide line and any segment label


def _text_w(s: str) -> float:
    return len(s) * CHAR_W


def _rupees(v: F) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):.2f}"


def amount_bars(rows: list[dict], scale_max, title: str, guide=None, guide_text=None) -> tuple[str, dict]:
    """rows: [{"label": str, "segments": [{"value": num, "style": "fill"|"cut"|"extra", "text": str}]}].

    Bar length is proportional to amount; scale_max fills the width W - 2*PAD.
    The first row's total is the "original" that segment percents are measured against.
    """
    x0, x1 = F(PAD), F(W - PAD)
    unit = (x1 - x0) / F(scale_max)
    guide_x = x0 + F(guide) * unit if guide is not None else None
    body: list[str] = []
    seg_recs = []   # {"row", "x", "w", "style", "text"}
    lab_recs = []   # {"row", "x0", "x1", "y", "text", "kind"}
    y = F(PAD)
    row_tops = []
    for i, r in enumerate(rows):
        lab_recs.append({"row": i, "x0": x0, "x1": x0 + _text_w(r["label"]), "y": y + 15,
                         "text": r["label"], "kind": "row"})
        by = y + ROW_LABEL_H
        row_tops.append(by)
        x = x0
        for s in r["segments"]:
            w = F(s["value"]) * unit
            seg_recs.append({"row": i, "x": x, "w": w, "y": by, "style": s["style"], "text": s.get("text", "")})
            x += w
        # segment labels below the bar: centred under the segment, clamped inside the picture
        prev_end = None
        for s in [k for k in seg_recs if k["row"] == i]:
            if not s["text"]:
                continue
            tw = F(_text_w(s["text"]))
            c = s["x"] + s["w"] / 2
            a, b = c - tw / 2, c + tw / 2
            if b > W - 4:
                a, b = W - 4 - tw, F(W - 4)
            if a < 4:
                a, b = F(4), 4 + tw
            if prev_end is not None and a < prev_end + 6:  # push right of the previous label
                a, b = prev_end + 6, prev_end + 6 + tw
            if guide_x is not None and a - GUIDE_GAP < guide_x < b + GUIDE_GAP:  # keep clear of the guide
                a, b = guide_x + GUIDE_GAP, guide_x + GUIDE_GAP + tw
            prev_end = b
            lab_recs.append({"row": i, "x0": a, "x1": b, "y": by + BAR_H + 18, "text": s["text"], "kind": "seg"})
        y = by + BAR_H + SEG_LABEL_H + ROW_GAP
    height = y - ROW_GAP + PAD - 4

    # draw segments
    for s in seg_recs:
        if s["style"] == "fill":
            st = f"fill:{FILL};stroke:{STROKE};stroke-width:1.5"
        elif s["style"] == "extra":
            st = f"fill:{POINT};stroke:{STROKE};stroke-width:1.5"
        else:  # cut
            st = f"fill:{EMPTY};stroke:{MUTED};stroke-width:1.8;stroke-dasharray:5 4"
        body.append(f'<rect x="{_f(s["x"])}" y="{_f(s["y"])}" width="{_f(s["w"])}" height="{BAR_H}" style="{st}"/>')
    # guide line: one line from under its label (top) down through every bar
    guide_top = guide_bot = None
    if guide_x is not None:
        text = guide_text or ""
        if text:
            tw = F(_text_w(text))
            lab_recs.append({"row": -1, "x0": guide_x - tw / 2, "x1": guide_x + tw / 2, "y": F(PAD) + 15,
                             "text": text, "kind": "guide"})
        guide_top = F(PAD) + 15 + 4
        guide_bot = row_tops[-1] + BAR_H + GUIDE_OUT
        line = f'x1="{_f(guide_x)}" y1="{_f(guide_top)}" x2="{_f(guide_x)}" y2="{_f(guide_bot)}"'
        body.append(f'<line {line} style="stroke:{EMPTY};stroke-width:5"/>')  # halo, so it shows on any fill
        body.append(f'<line {line} style="stroke:{POINT};stroke-width:2.4;stroke-dasharray:6 4"/>')
    # draw labels
    for lab in lab_recs:
        weight = "700" if lab["kind"] in ("row", "guide") else "600"
        color = POINT if lab["kind"] == "guide" else TEXT
        body.append(_text(lab["x0"], lab["y"], lab["text"], SIZE, anchor="start", weight=weight, color=color))

    # ---- meta, read back from the drawn records
    rows_meta = []
    for i in range(len(rows)):
        segs = [s for s in seg_recs if s["row"] == i]
        vals = [s["w"] / unit for s in segs]
        rows_meta.append({
            "label": next(lab["text"] for lab in lab_recs if lab["row"] == i and lab["kind"] == "row"),
            "segments": [{"value": _rupees(v), "style": s["style"], "text": s["text"]} for v, s in zip(vals, segs)],
            # the amount the bar stands for: everything except money cut off
            "amount": _rupees(sum(v for v, s in zip(vals, segs) if s["style"] != "cut")),
            "length": _rupees(sum(vals)),
        })
    original = sum(s["w"] for s in seg_recs if s["row"] == 0 and s["style"] != "cut") / unit
    for rm in rows_meta:
        for sm in rm["segments"]:
            sm["percent_of_original"] = str(F(sm["value"]) / original * 100)
        rm["percent_of_original"] = str(F(rm["amount"]) / original * 100)
    # overlap check on every pair of labels in the same text line
    overlaps = 0
    for a in range(len(lab_recs)):
        for b in range(a + 1, len(lab_recs)):
            la, lb = lab_recs[a], lab_recs[b]
            if la["y"] == lb["y"] and la["x0"] < lb["x1"] and lb["x0"] < la["x1"]:
                overlaps += 1
    if guide_x is not None:  # the guide line must not run through any label but its own
        for lab in lab_recs:
            if lab["kind"] == "guide":
                continue
            ly0, ly1 = lab["y"] - SIZE + 2, lab["y"] + 4  # text box: cap height to descender
            if lab["x0"] - 2 <= guide_x <= lab["x1"] + 2 and ly0 < guide_bot and guide_top < ly1:
                overlaps += 1
    inside = all(0 <= lab["x0"] and lab["x1"] <= W for lab in lab_recs)
    meta = {"rows": rows_meta, "original": _rupees(original), "label_overlaps": overlaps,
            "labels_inside": inside}
    if guide_x is not None:
        meta["guide"] = _rupees((guide_x - x0) / unit)
        meta["guide_text"] = next((lab["text"] for lab in lab_recs if lab["kind"] == "guide"), "")
        # rows whose bar the line runs through, from top to bottom
        meta["guide_crosses_rows"] = sum(1 for t in row_tops if guide_top <= t and t + BAR_H <= guide_bot)
    return _svg(height, body, title), meta


# ---------------------------------------------------------------- the visuals
draw.save(OUT, "pc-discount", *amount_bars([
    {"label": "Before: ₹800", "segments": [{"value": 800, "style": "fill", "text": "100% = ₹800"}]},
    {"label": "Sale: 25% off", "segments": [
        {"value": 600, "style": "fill", "text": "You pay ₹600"},
        {"value": 200, "style": "cut", "text": "25% = ₹200"}]},
], 800, "A ₹800 price with 25% off: ₹200 is cut off and you pay ₹600"))

draw.save(OUT, "pc-gst", *amount_bars([
    {"label": "Before GST: ₹3000", "segments": [{"value": 3000, "style": "fill", "text": "100% = ₹3000"}]},
    {"label": "With 5% GST: ₹3150", "segments": [
        {"value": 3000, "style": "fill", "text": "₹3000"},
        {"value": 150, "style": "extra", "text": "GST ₹150"}]},
], 3150, "A ₹3000 price before GST, with 5% GST added: ₹150 more, ₹3150 in all"))

draw.save(OUT, "pc-tomato", *amount_bars([
    {"label": "Before: ₹40 a kg", "segments": [{"value": 10, "style": "fill", "text": "₹10"} for _ in range(4)]},
    {"label": "Now: ₹50 a kg", "segments": [{"value": 10, "style": "fill", "text": "₹10"} for _ in range(4)]
        + [{"value": 10, "style": "extra", "text": "+₹10"}]},
], 50, "Tomatoes rise from ₹40 to ₹50: 4 parts of ₹10 become 5 parts"))

draw.save(OUT, "pc-up-down", *amount_bars([
    {"label": "Start: ₹500", "segments": [{"value": 500, "style": "fill", "text": "₹500"}]},
    {"label": "Up 20%: ₹600", "segments": [
        {"value": 500, "style": "fill", "text": "₹500"},
        {"value": 100, "style": "extra", "text": "+₹100"}]},
    {"label": "Then down 20%: ₹480", "segments": [
        {"value": 480, "style": "fill", "text": "₹480"},
        {"value": 120, "style": "cut", "text": "−₹120"}]},
], 600, "₹500 up 20% is ₹600, then down 20% is ₹480, short of ₹500", guide=500, guide_text="₹500"))

print("drew", len(list(OUT.glob("*.svg"))), "visuals for s0-percent-change")
