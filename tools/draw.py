"""Code-drawn maths diagrams as SVG.

Every function returns (svg, meta). `meta` is computed from the shapes actually
drawn (not copied from the request), so the verifier can compare it with the
`checks` a topic file declares and catch a diagram that does not match its text.

Colours use CSS variables with fallbacks so diagrams follow light/dark mode when
inlined into the site.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

STROKE = "var(--viz-stroke,#1F2421)"
FILL = "var(--viz-fill,#C2703D)"
EMPTY = "var(--viz-empty,#FFFFFF)"
TEXT = "var(--viz-text,#1F2421)"
POINT = "var(--viz-point,#2F6F62)"
MUTED = "var(--viz-muted,#8A938D)"
FONT = "system-ui,-apple-system,Segoe UI,Roboto,sans-serif"

W = 320  # viewBox width; scales to the container
PAD = 20


def _f(x) -> str:
    return f"{float(x):.2f}".rstrip("0").rstrip(".")


def _svg(height: float, body: list[str], title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {_f(height)}" '
        f'role="img" aria-label="{title}" style="font-family:{FONT}">'
        + "".join(body) + "</svg>"
    )


def _text(x, y, s, size=14, anchor="middle", weight="400", color=TEXT) -> str:
    return (f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" style="fill:{color}">{s}</text>')


def _frac_label(x, y_top, num, den, size=13) -> str:
    """Stacked fraction: numerator, bar, denominator. y_top is the numerator baseline."""
    w = max(len(str(num)), len(str(den))) * size * 0.62 + 4
    return (_text(x, y_top, num, size) +
            f'<line x1="{_f(x - w / 2)}" y1="{_f(y_top + 4)}" x2="{_f(x + w / 2)}" y2="{_f(y_top + 4)}" '
            f'style="stroke:{TEXT};stroke-width:1.2"/>' +
            _text(x, y_top + 4 + size + 1, den, size))


# ---------------------------------------------------------------- bars
def bars(rows: list[dict], title: str) -> tuple[str, dict]:
    """rows: [{"weights": [1,1,1,1], "shaded": [0,1,2], "label": "3/4"}]. All bars have equal length."""
    labels = [r.get("label") or "" for r in rows]
    text_len = max((len(lab) for lab in labels if "/" not in lab), default=0)
    label_w = max(52, text_len * 8 + 12) if any(labels) else 0
    x0, x1 = PAD + label_w, W - PAD
    bar_h, gap = 34, 22
    body, meta_bars = [], []
    for i, r in enumerate(rows):
        y = PAD + i * (bar_h + gap)
        total = Fraction(sum(r["weights"]))
        x = Fraction(x0)
        widths = []
        shaded_count = 0
        for j, wgt in enumerate(r["weights"]):
            w = Fraction(x1 - x0) * Fraction(wgt) / total
            shaded = j in set(r.get("shaded", []))
            shaded_count += shaded
            body.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{bar_h}" '
                        f'style="fill:{FILL if shaded else EMPTY};stroke:{STROKE};stroke-width:1.5"/>')
            widths.append(w)
            x += w
        lab = r.get("label")
        if lab:
            if "/" in lab:
                n, d = lab.split("/")
                body.append(_frac_label(PAD + label_w / 2 - 6, y + 13, n, d))
            else:
                body.append(_text(PAD, y + bar_h / 2 + 5, lab, 13, anchor="start", weight="600"))
        meta_bars.append({"parts": len(widths), "equal": len(set(widths)) == 1, "shaded": shaded_count})
    h = PAD * 2 + len(rows) * bar_h + (len(rows) - 1) * gap
    return _svg(h, body, title), {"bars": meta_bars}


# ---------------------------------------------------------------- roti (circle)
def roti(sectors: int, shaded: int, title: str) -> tuple[str, dict]:
    import math
    cx, r = W / 2, 70
    cy = PAD + r
    body = [f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{r}" style="fill:{EMPTY};stroke:{STROKE};stroke-width:1.5"/>']
    for k in range(sectors):
        a0 = -math.pi / 2 + 2 * math.pi * k / sectors
        a1 = -math.pi / 2 + 2 * math.pi * (k + 1) / sectors
        p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        large = 1 if (a1 - a0) > math.pi else 0
        fill = FILL if k < shaded else EMPTY
        body.append(f'<path d="M{_f(cx)},{_f(cy)} L{_f(p0[0])},{_f(p0[1])} A{r},{r} 0 {large} 1 {_f(p1[0])},{_f(p1[1])} Z" '
                    f'style="fill:{fill};stroke:{STROKE};stroke-width:1.5"/>')
    return _svg(PAD * 2 + 2 * r, body, title), {"sectors": sectors, "shaded": min(shaded, sectors)}


# ---------------------------------------------------------------- groups of dots
def dot_groups(groups: int, per_group: int, highlight: int, title: str) -> tuple[str, dict]:
    gw = (W - 2 * PAD) / groups
    body, counts = [], []
    for g in range(groups):
        gx = PAD + g * gw
        hl = g < highlight
        body.append(f'<rect x="{_f(gx + 6)}" y="{PAD}" width="{_f(gw - 12)}" height="76" rx="14" '
                    f'style="fill:none;stroke:{POINT if hl else MUTED};stroke-width:{2.5 if hl else 1.5};'
                    f'{"" if hl else "stroke-dasharray:5 4"}"/>')
        n = 0
        cols = 2
        for k in range(per_group):
            col, row = k % cols, k // cols
            x = gx + gw / 2 + (col - 0.5) * 26
            y = PAD + 22 + row * 30
            body.append(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="10" style="fill:{FILL};stroke:{STROKE};stroke-width:1.2"/>')
            n += 1
        counts.append(n)
    meta = {"groups": groups, "per_group": counts[0] if len(set(counts)) == 1 else None,
            "highlighted_groups": highlight}
    return _svg(PAD * 2 + 76, body, title), meta


# ---------------------------------------------------------------- number lines
def _number_line(y, start: Fraction, end: Fraction, spu: int, labels, point, body) -> dict:
    """Draw one number line at height y. Returns meta derived from the drawing."""
    x0, x1 = Fraction(PAD + 10), Fraction(W - PAD - 10)
    unit_px = (x1 - x0) / (end - start)
    body.append(f'<line x1="{_f(x0)}" y1="{_f(y)}" x2="{_f(x1)}" y2="{_f(y)}" style="stroke:{STROKE};stroke-width:2"/>')
    n_ticks = int((end - start) * spu) + 1
    tick_xs = []
    drawn_labels = []
    for k in range(n_ticks):
        value = start + Fraction(k, spu)
        x = x0 + (value - start) * unit_px
        whole = value.denominator == 1
        h = 10 if whole else 7
        body.append(f'<line x1="{_f(x)}" y1="{_f(y - h)}" x2="{_f(x)}" y2="{_f(y + h)}" '
                    f'style="stroke:{STROKE};stroke-width:{2 if whole else 1.5}"/>')
        tick_xs.append(x)
        lab = None
        if labels == "wholes" and whole:
            lab = str(value.numerator)
        elif labels == "all":  # wholes as whole numbers, other marks as k/spu
            lab = str(value.numerator) if whole else f"{k + int(start * spu)}/{spu}"
        elif labels == "steps":  # every mark as k/spu, including 0/spu
            lab = f"{k + int(start * spu)}/{spu}"
        if lab is not None:
            drawn_labels.append(lab)
            if "/" in lab:
                num, den = lab.split("/")
                body.append(_frac_label(x, y + 26, num, den, 12))
            else:
                body.append(_text(x, y + 30, lab, 15, weight="600"))
    gaps = {tick_xs[i + 1] - tick_xs[i] for i in range(len(tick_xs) - 1)}
    meta = {"start": str(start), "end": str(end),
            "spaces_per_unit": int((len(tick_xs) - 1) / (end - start)) if len(gaps) == 1 else None,
            "labels": drawn_labels}
    if point is not None:
        px = x0 + (Fraction(point) - start) * unit_px
        body.append(f'<circle cx="{_f(px)}" cy="{_f(y)}" r="7" style="fill:{POINT};stroke:{EMPTY};stroke-width:2"/>')
        meta["point"] = str(start + (px - x0) / unit_px)  # read back from the drawn position
    return meta


def number_line(start, end, spu, title, labels="wholes", point=None) -> tuple[str, dict]:
    body: list[str] = []
    meta = _number_line(Fraction(PAD + 14), Fraction(start), Fraction(end), spu, labels, point, body)
    if labels == "steps":
        # also show whole numbers under the fraction labels
        x0, x1 = PAD + 10, W - PAD - 10
        for v in range(int(start), int(end) + 1):
            x = x0 + (v - start) * (x1 - x0) / (end - start)
            body.append(_text(x, PAD + 14 + 72, str(v), 14, weight="700", color=POINT))
        h = PAD + 14 + 82
    else:
        h = PAD + 14 + 50
    return _svg(h, body, title), meta


def stacked_number_lines(lines: list[dict], title: str) -> tuple[str, dict]:
    body: list[str] = []
    metas = []
    for i, ln in enumerate(lines):
        y = PAD + 14 + i * 70
        m = _number_line(Fraction(y), Fraction(0), Fraction(1), ln["spu"], ln.get("labels", "wholes"), ln.get("point"), body)
        metas.append({"spaces_per_unit": m["spaces_per_unit"], "point": m.get("point")})
    # dashed guide through the points to show they line up
    pts = [ln.get("point") for ln in lines]
    no_mid_labels = all(ln.get("labels", "wholes") == "wholes" for ln in lines)
    if no_mid_labels and all(p is not None for p in pts) and len({Fraction(p) for p in pts}) == 1:
        x = PAD + 10 + Fraction(pts[0]) * (W - 2 * PAD - 20)
        body.append(f'<line x1="{_f(x)}" y1="{PAD}" x2="{_f(x)}" y2="{_f(PAD + 14 + (len(lines) - 1) * 70 + 10)}" '
                    f'style="stroke:{POINT};stroke-width:1.5;stroke-dasharray:4 4"/>')
    return _svg(PAD + 14 + (len(lines) - 1) * 70 + 50, body, title), {"lines": metas}


# ---------------------------------------------------------------- output
def save(out_dir: Path, vid: str, svg: str, meta: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{vid}.svg").write_text(svg + "\n", encoding="utf-8", newline="\n")
    (out_dir / f"{vid}.meta.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8", newline="\n")
