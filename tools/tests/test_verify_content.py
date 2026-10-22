"""Tests that the verifier passes good content and catches each class of error."""
import copy
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import verify_content as vc  # noqa: E402

FIXTURE = TOOLS / "tests" / "fixtures" / "s0-sample.json"
GOOD = json.loads(FIXTURE.read_text(encoding="utf-8"))


def run(doc, tmp_path, topic_map=None):
    p = tmp_path / f"{doc['id']}.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return vc.verify_file(p, topic_map or {})


def test_good_fixture_passes(tmp_path):
    rep = run(copy.deepcopy(GOOD), tmp_path)
    assert rep.fails == []
    assert rep.passes >= 10
    assert any("manual" in w for w in rep.warns)


def test_wrong_numeric_answer_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["quiz"][1]["answer"] = "38"
    rep = run(doc, tmp_path)
    assert any("q-2" in f and "36" in f for f in rep.fails)


def test_wrong_worked_example_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["lesson"]["examples"][0]["answer"] = "8"
    assert any("examples[0]" in f for f in run(doc, tmp_path).fails)


def test_mcq_two_correct_values_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["quiz"][0]["options"][1]["value"] = "6/8"  # equals 3/4 but marked wrong
    assert any("two correct answers" in f for f in run(doc, tmp_path).fails)


def test_mcq_wrong_option_marked_correct_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    q = doc["quiz"][0]
    q["options"][0]["correct"], q["options"][1]["correct"] = False, True
    q["options"][0]["why_wrong"] = "x"
    q["options"][1].pop("why_wrong")
    q["answer"] = q["options"][1]["text"]
    assert any("marked correct" in f for f in run(doc, tmp_path).fails)


def test_wrong_relation_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["practice"][2]["answer"] = "false"
    assert any("p-3" in f for f in run(doc, tmp_path).fails)


def test_raw_html_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["lesson"]["hook"] = "Hi <script>alert(1)</script>"
    assert any("raw HTML" in f for f in run(doc, tmp_path).fails)


def test_unsafe_expression_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["quiz"][1]["verify"]["expr"] = "__import__('os').system('true')"
    assert any("cannot evaluate" in f for f in run(doc, tmp_path).fails)


def test_duplicate_question_id_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["quiz"][1]["id"] = "s0-sample/q-1"
    assert any("duplicate question id" in f for f in run(doc, tmp_path).fails)


def test_numeric_manual_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["quiz"][1]["verify"] = {"kind": "manual", "reason": "lazy"}
    assert any("must be computer-verified" in f for f in run(doc, tmp_path).fails)


def test_verified_without_review_fails(tmp_path):
    doc = copy.deepcopy(GOOD)
    doc["status"] = "verified"
    assert any("requires a review" in f for f in run(doc, tmp_path).fails)


def test_topic_not_in_map_fails(tmp_path):
    rep = run(copy.deepcopy(GOOD), tmp_path, topic_map={"s0-other": {"objectives": ["a", "b"]}})
    assert any("not in curriculum" in f for f in rep.fails)


@pytest.mark.parametrize("field", ["hints", "explanation", "verify"])
def test_missing_required_field_fails(tmp_path, field):
    doc = copy.deepcopy(GOOD)
    doc["quiz"][1].pop(field)
    assert run(doc, tmp_path).fails


# ---- drawings, SVG safety and answer-matching rules

def test_checks_match_by_value():
    assert vc.compare_checks({"lines": [{"point": "2/4"}]}, {"lines": [{"point": "1/2"}]}) == []


def test_checks_detect_wrong_drawing():
    problems = vc.compare_checks({"bars": [{"parts": 4, "shaded": 3}]}, {"bars": [{"parts": 4, "shaded": 2}]})
    assert problems and "shaded" in problems[0]


def test_checks_detect_missing_bar():
    assert vc.compare_checks({"bars": [{"parts": 2}, {"parts": 4}]}, {"bars": [{"parts": 2}]})


@pytest.mark.parametrize("svg", [
    '<svg viewBox="0 0 1 1"><script>alert(1)</script></svg>',
    '<svg viewBox="0 0 1 1"><rect onclick="x()"/></svg>',
    '<svg viewBox="0 0 1 1"><image href="https://x.test/a.png"/></svg>',
    '<svg viewBox="0 0 1 1"><rect style="fill:url(https://x.test/a)"/></svg>',
    '<svg><rect/></svg>',
])
def test_unsafe_svg_fails(svg):
    rep = vc.Report("t")
    vc.check_svg_safety(rep, "v", svg)
    assert rep.fails


def test_safe_svg_passes():
    rep = vc.Report("t")
    vc.check_svg_safety(rep, "v", '<svg viewBox="0 0 1 1"><rect style="fill:var(--viz-fill,#C2703D)"/></svg>')
    assert not rep.fails


@pytest.mark.parametrize("answer,ok", [("3/4", True), ("6/8", False), ("2", True), ("0.75", False)])
def test_simplest_rule(answer, ok):
    rep = vc.Report("t")
    vc.check_match_rule(rep, "q", {"type": "numeric", "answer": answer, "match": "simplest"})
    assert (not rep.fails) == ok


def test_exact_rule_needs_fraction():
    rep = vc.Report("t")
    vc.check_match_rule(rep, "q", {"type": "numeric", "answer": "2", "match": "exact"})
    assert rep.fails


@pytest.mark.parametrize("answer,ok", [("2 1/3", True), ("3", True), ("7/3", False), ("1 4/3", False)])
def test_mixed_rule(answer, ok):
    rep = vc.Report("t")
    vc.check_match_rule(rep, "q", {"type": "numeric", "answer": answer, "match": "mixed"})
    assert (not rep.fails) == ok


@pytest.mark.parametrize("answer,ok", [("7/5", True), ("1 2/5", False), ("2", False)])
def test_improper_rule(answer, ok):
    rep = vc.Report("t")
    vc.check_match_rule(rep, "q", {"type": "numeric", "answer": answer, "match": "improper"})
    assert (not rep.fails) == ok
