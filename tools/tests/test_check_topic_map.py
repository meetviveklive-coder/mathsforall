"""Tests that the topic-map checker catches structural errors."""
import copy
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import check_topic_map as ctm  # noqa: E402

REAL = ctm.load()


def topic(tid, stage, prereqs):
    return {"id": tid, "title": f"Topic {tid}", "stage": stage, "prerequisites": prereqs,
            "objectives": ["objective one here", "objective two here"],
            "misconceptions": ["a misconception here"], "est_minutes": 20}


def doc(*topics):
    return {"version": 1, "stages": [], "topics": list(topics)}


def test_real_map_passes():
    fails, _ = ctm.check(copy.deepcopy(REAL))
    assert fails == []


def test_cycle_fails():
    fails, _ = ctm.check(doc(topic("s0-a", 0, ["s0-b"]), topic("s0-b", 0, ["s0-a"])))
    assert any("cycle" in f for f in fails)


def test_unknown_prereq_fails():
    fails, _ = ctm.check(doc(topic("s0-a", 0, ["s0-missing"])))
    assert any("unknown prerequisite" in f for f in fails)


def test_later_stage_prereq_fails():
    fails, _ = ctm.check(doc(topic("s1-b", 1, []), topic("s0-a", 0, ["s1-b"])))
    assert any("later stage" in f for f in fails)


def test_redundant_prereq_warns():
    _, warns = ctm.check(doc(topic("s0-a", 0, []), topic("s0-b", 0, ["s0-a"]),
                             topic("s0-c", 0, ["s0-a", "s0-b"])))
    assert any("s0-a is redundant" in w for w in warns)


def test_stage_prefix_mismatch_fails():
    fails, _ = ctm.check(doc(topic("s1-a", 0, [])))
    assert any("prefix" in f for f in fails)
