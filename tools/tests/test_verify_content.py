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
GOOD = json.loads(FIXTURE.read_text())


def run(doc, tmp_path, topic_map=None):
    p = tmp_path / f"{doc['id']}.json"
    p.write_text(json.dumps(doc))
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
