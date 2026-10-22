#!/usr/bin/env python3
"""Verify topic files: schema, IDs, and every answer by SymPy computation.

Usage:
    python3 tools/verify_content.py                 # all files in content/topics/
    python3 tools/verify_content.py path/to/x.json  # specific files

Exit code 1 if any FAIL. WARNs do not fail the run but must be read by a human.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathcheck  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "topic.schema.json").read_text())
TOPIC_MAP_PATH = ROOT / "curriculum" / "topic-map.json"
RAW_HTML = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")


class Report:
    def __init__(self, name: str):
        self.name = name
        self.fails: list[str] = []
        self.warns: list[str] = []
        self.passes = 0

    def fail(self, where: str, msg: str):
        self.fails.append(f"FAIL {where}: {msg}")

    def warn(self, where: str, msg: str):
        self.warns.append(f"WARN {where}: {msg}")

    def ok(self):
        self.passes += 1


def _texts(obj, path="$"):
    """Yield (path, string) for every string in the document."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _texts(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _texts(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def check_value(rep: Report, where: str, verify: dict, answer: str):
    kind = verify["kind"]
    if kind == "manual":
        rep.warn(where, f"manual check ({verify.get('reason', 'no reason')}) - human must confirm")
        return
    try:
        computed = mathcheck.parse(verify["expr"])
    except Exception as e:  # noqa: BLE001
        rep.fail(where, f"cannot evaluate verify.expr {verify['expr']!r}: {e}")
        return
    if kind == "relation":
        truth = mathcheck.as_bool(computed)
        if truth is None:
            rep.fail(where, f"relation {verify['expr']!r} did not evaluate to true/false (got {computed})")
            return
        if answer.strip().lower() not in ("true", "false"):
            rep.fail(where, f"relation check needs answer 'true' or 'false', got {answer!r}")
            return
        if truth != (answer.strip().lower() == "true"):
            rep.fail(where, f"answer {answer!r} but {verify['expr']!r} is {truth}")
            return
        rep.ok()
        return
    try:
        stated = mathcheck.parse(answer)
    except Exception as e:  # noqa: BLE001
        rep.fail(where, f"cannot parse answer {answer!r}: {e}")
        return
    if mathcheck.equal(computed, stated):
        rep.ok()
    else:
        rep.fail(where, f"answer {answer!r} but {verify['expr']!r} = {computed}")


def check_mcq(rep: Report, where: str, q: dict):
    options = q["options"]
    correct = [o for o in options if o["correct"]]
    if len(correct) != 1:
        rep.fail(where, f"MCQ must have exactly 1 correct option, has {len(correct)}")
        return
    texts = [o["text"].strip() for o in options]
    if len(set(texts)) != len(texts):
        rep.fail(where, "duplicate option texts")
    if q["answer"].strip() != correct[0]["text"].strip():
        rep.fail(where, "answer does not match the text of the correct option")
    v = q["verify"]
    if v["kind"] == "manual":
        rep.warn(where, f"manual MCQ ({v.get('reason')}) - human must confirm")
        return
    if v["kind"] != "sympy":
        rep.fail(where, "MCQ verify.kind must be 'sympy' or 'manual'")
        return
    if any("value" not in o for o in options):
        rep.fail(where, "every MCQ option needs a 'value' when verify.kind is sympy")
        return
    try:
        computed = mathcheck.parse(v["expr"])
    except Exception as e:  # noqa: BLE001
        rep.fail(where, f"cannot evaluate verify.expr: {e}")
        return
    for i, o in enumerate(options):
        try:
            val = mathcheck.parse(o["value"])
        except Exception as e:  # noqa: BLE001
            rep.fail(f"{where} option {i}", f"cannot parse value {o['value']!r}: {e}")
            continue
        is_eq = mathcheck.equal(computed, val)
        if o["correct"] and not is_eq:
            rep.fail(f"{where} option {i}", f"marked correct but {o['value']} != {computed}")
        elif not o["correct"] and is_eq:
            rep.fail(f"{where} option {i}", f"marked wrong but {o['value']} == {computed} (two correct answers)")
        else:
            rep.ok()


def load_topic_map():
    if not TOPIC_MAP_PATH.exists():
        return {}
    return {t["id"]: t for t in json.loads(TOPIC_MAP_PATH.read_text())["topics"]}


def verify_file(path: Path, topic_map: dict) -> Report:
    rep = Report(path.name)
    try:
        doc = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        rep.fail("$", f"invalid JSON: {e}")
        return rep

    errors = sorted(Draft202012Validator(SCHEMA).iter_errors(doc), key=lambda e: list(e.path))
    for e in errors:
        rep.fail("$." + ".".join(map(str, e.path)), e.message[:200])
    if errors:
        return rep  # structure is wrong; deeper checks would be noise

    tid = doc["id"]
    if path.stem != tid:
        rep.fail("$.id", f"file name {path.stem!r} must equal id {tid!r}")
    entry = topic_map.get(tid)
    if topic_map and entry is None and doc["status"] != "retired":
        rep.fail("$.id", f"{tid!r} is not in curriculum/topic-map.json")

    for where, s in _texts(doc):
        if RAW_HTML.search(s):
            rep.fail(where, "raw HTML is not allowed in content")

    for i, ex in enumerate(doc["lesson"]["examples"]):
        check_value(rep, f"lesson.examples[{i}]", ex["verify"], ex["answer"])

    visual_ids = {v["id"] for v in doc.get("visuals", [])}
    for v in doc.get("visuals", []):
        if "file" in v and not (path.parent / v["file"]).exists() and not (ROOT / v["file"]).exists():
            (rep.warn if doc["status"] == "draft" else rep.fail)(f"visuals.{v['id']}", f"file {v['file']} not found")
        if "file" not in v:
            (rep.warn if doc["status"] == "draft" else rep.fail)(f"visuals.{v['id']}", "not drawn yet")
    for i, s in enumerate(doc["lesson"]["sections"]):
        if s.get("visual") and s["visual"] not in visual_ids:
            rep.fail(f"lesson.sections[{i}]", f"unknown visual {s['visual']!r}")

    seen_ids: set[str] = set()
    prompts: dict[str, str] = {}
    n_obj = len(entry["objectives"]) if entry else None
    covered: set[int] = set()
    for group in ("practice", "quiz"):
        for i, q in enumerate(doc[group]):
            where = f"{group}[{i}] {q['id']}"
            if not q["id"].startswith(tid + "/"):
                rep.fail(where, f"question id must start with {tid}/")
            if q["id"] in seen_ids:
                rep.fail(where, "duplicate question id")
            seen_ids.add(q["id"])
            norm = re.sub(r"\s+", " ", q["prompt"].strip().lower())
            if norm in prompts:
                rep.fail(where, f"same prompt as {prompts[norm]}")
            prompts[norm] = q["id"]
            if q.get("visual") and q["visual"] not in visual_ids:
                rep.fail(where, f"unknown visual {q['visual']!r}")
            if "objective" in q and n_obj is not None:
                if q["objective"] >= n_obj:
                    rep.fail(where, f"objective {q['objective']} out of range (topic has {n_obj})")
                elif group == "quiz":
                    covered.add(q["objective"])

            if q["type"] == "mcq":
                check_mcq(rep, where, q)
            elif q["type"] == "true_false":
                if q["verify"]["kind"] == "sympy":
                    rep.fail(where, "true_false must use verify.kind 'relation' or 'manual'")
                else:
                    check_value(rep, where, q["verify"], q["answer"])
            else:
                check_value(rep, where, q["verify"], q["answer"])
                if q["type"] == "numeric" and q["verify"]["kind"] == "manual":
                    rep.fail(where, "numeric questions must be computer-verified")

    if n_obj is not None:
        missing = sorted(set(range(n_obj)) - covered)
        if missing:
            rep.warn("quiz", f"objectives not covered by any quiz question: {missing}")

    if doc["status"] in ("verified", "approved") and not doc.get("review"):
        rep.fail("$.review", f"status {doc['status']!r} requires a review entry")
    return rep


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in argv] or sorted((ROOT / "content" / "topics").glob("*.json"))
    if not paths:
        print("No topic files found.")
        return 0
    topic_map = load_topic_map()
    total_fail = 0
    for p in paths:
        rep = verify_file(p, topic_map)
        for line in rep.fails + rep.warns:
            print(f"  {line}")
        status = "FAIL" if rep.fails else "PASS"
        print(f"{status} {rep.name}: {rep.passes} checks passed, {len(rep.fails)} failed, {len(rep.warns)} warnings")
        total_fail += len(rep.fails)
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
