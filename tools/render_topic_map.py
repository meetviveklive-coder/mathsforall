#!/usr/bin/env python3
"""Render curriculum/topic-map.json as curriculum/TOPIC_MAP.md for human review."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_topic_map as ctm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def render(doc: dict) -> str:
    topics = doc["topics"]
    num = {t["id"]: i + 1 for i, t in enumerate(topics)}
    stage_names = {s["stage"]: s["name"] for s in doc["stages"]}
    mins = sum(t["est_minutes"] for t in topics)
    out = [
        "# Topic map — for review",
        "",
        f"{len(topics)} topics, about {mins // 60} hours of learning time. "
        "Numbers in brackets are prerequisites. Generated from `curriculum/topic-map.json` — edit that file, not this one.",
        "",
    ]
    stage = unit = None
    for t in topics:
        if t["stage"] != stage:
            stage, unit = t["stage"], None
            out += [f"## Stage {stage} — {stage_names.get(stage, '')}", ""]
        if t.get("unit") != unit:
            unit = t.get("unit")
            out += [f"### {unit}", ""]
        pre = ", ".join(f"{num[p]}" for p in t["prerequisites"]) or "start"
        out.append(f"**{num[t['id']]}. {t['title']}** · [{pre}] · {t['est_minutes']} min")
        out.append("")
        for o in t["objectives"]:
            out.append(f"- {o}")
        out.append(f"- *Watch for:* {'; '.join(t['misconceptions'])}")
        if t.get("indian_context"):
            out.append(f"- *Context:* {t['indian_context']}")
        out.append("")
    leaves = [t for t in topics if not any(t["id"] in u["prerequisites"] for u in topics)]
    out += ["## End points", "", "Topics nothing else depends on yet (they will feed later stages):", ""]
    out += [f"- {num[t['id']]}. {t['title']}" for t in leaves]
    out.append("")
    return "\n".join(out)


def main() -> int:
    doc = ctm.load()
    fails, _ = ctm.check(doc)
    if fails:
        print("Topic map has errors; run tools/check_topic_map.py")
        return 1
    path = ROOT / "curriculum" / "TOPIC_MAP.md"
    path.write_text(render(doc), encoding="utf-8", newline="\n")
    print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
