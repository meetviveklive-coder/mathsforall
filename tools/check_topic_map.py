#!/usr/bin/env python3
"""Validate curriculum/topic-map.json: schema, references, stage order, DAG.

FAIL: schema errors, duplicate ids, unknown or self prerequisites,
      prerequisites from a later stage, cycles.
WARN: prerequisites already implied by another listed prerequisite (redundant).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def load(path: Path | None = None):
    path = path or ROOT / "curriculum" / "topic-map.json"
    return json.loads(path.read_text(encoding="utf-8"))


def topo_order(topics: list[dict]) -> list[str] | None:
    """Kahn's algorithm, stable by file order. Returns None if there is a cycle."""
    ids = [t["id"] for t in topics]
    indeg = {i: 0 for i in ids}
    children: dict[str, list[str]] = {i: [] for i in ids}
    for t in topics:
        for p in t["prerequisites"]:
            if p in indeg:
                indeg[t["id"]] += 1
                children[p].append(t["id"])
    ready = [i for i in ids if indeg[i] == 0]
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for c in children[n]:
            indeg[c] -= 1
            if indeg[c] == 0:
                ready.append(c)
    return order if len(order) == len(ids) else None


def ancestors(tid: str, by_id: dict) -> set[str]:
    seen: set[str] = set()
    stack = list(by_id[tid]["prerequisites"])
    while stack:
        p = stack.pop()
        if p in seen or p not in by_id:
            continue
        seen.add(p)
        stack.extend(by_id[p]["prerequisites"])
    return seen


def check(doc: dict) -> tuple[list[str], list[str]]:
    fails, warns = [], []
    schema = json.loads((ROOT / "schema" / "topic-map.schema.json").read_text(encoding="utf-8"))
    for e in Draft202012Validator(schema).iter_errors(doc):
        fails.append(f"schema {'/'.join(map(str, e.path))}: {e.message[:160]}")
    if fails:
        return fails, warns

    topics = doc["topics"]
    by_id: dict[str, dict] = {}
    for t in topics:
        if t["id"] in by_id:
            fails.append(f"duplicate id {t['id']}")
        by_id[t["id"]] = t
        if not t["id"].startswith(f"s{t['stage']}-"):
            fails.append(f"{t['id']}: id prefix does not match stage {t['stage']}")

    for t in topics:
        for p in t["prerequisites"]:
            if p == t["id"]:
                fails.append(f"{t['id']}: lists itself as a prerequisite")
            elif p not in by_id:
                fails.append(f"{t['id']}: unknown prerequisite {p}")
            elif by_id[p]["stage"] > t["stage"]:
                fails.append(f"{t['id']}: prerequisite {p} is in a later stage")

    if topo_order(topics) is None:
        fails.append("prerequisite graph has a cycle")
        return fails, warns

    for t in topics:
        for p in t["prerequisites"]:
            others = [q for q in t["prerequisites"] if q != p]
            for q in others:
                if p in ancestors(q, by_id):
                    warns.append(f"{t['id']}: {p} is redundant (already required by {q})")
                    break
    return fails, warns


def main() -> int:
    doc = load()
    fails, warns = check(doc)
    for f in fails:
        print("FAIL", f)
    for w in warns:
        print("WARN", w)
    if not fails:
        topics = doc["topics"]
        by_stage: dict[int, int] = {}
        for t in topics:
            by_stage[t["stage"]] = by_stage.get(t["stage"], 0) + 1
        roots = [t["id"] for t in topics if not t["prerequisites"]]
        mins = sum(t["est_minutes"] for t in topics)
        print(f"PASS {len(topics)} topics {by_stage}, roots={roots}, est. {mins} min (~{mins/60:.0f} h)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
