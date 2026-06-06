import os
import sys
import json
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import truth_resolver as tr  # noqa: E402


def test_constants_and_dataclasses_exist():
    assert tr.ALIGN_THRESHOLD == 0.5
    assert tr.VALUE_DIMENSIONS == ("correctness", "performance", "security", "knowledge_integration")

    v = tr.AlignmentVector(role="user", intent={"a"}, context={"b"}, value={"correctness"})
    assert v.role == "user"
    assert v.intent == {"a"} and v.context == {"b"} and v.value == {"correctness"}

    verdict = tr.Verdict(passed=True, alignment=1.0, value=2.0, rationale="ok", dissent=[])
    assert verdict.passed is True and verdict.alignment == 1.0
    assert verdict.value == 2.0 and verdict.rationale == "ok" and verdict.dissent == []


def test_distiller_is_runtime_checkable_protocol():
    class StubDistiller:
        def distill(self, actor):
            return tr.AlignmentVector(role="x", intent=set(), context=set(), value=set())
    assert isinstance(StubDistiller(), tr.Distiller)
    assert not isinstance(object(), tr.Distiller)


def test_tokens_splits_lowercases_and_drops_empties():
    assert tr._tokens("O(1) memory, Zero-Drift!") == {"o", "1", "memory", "zero", "drift"}
    assert tr._tokens("") == set()


def test_deterministic_distiller_builds_vector():
    d = tr.DeterministicDistiller()
    actor = {
        "role": "user",
        "intent": "Reduce drift to O(1)",
        "context": "studio build",
        "values": ["Correctness", "Knowledge_Integration"],
    }
    v = d.distill(actor)
    assert isinstance(v, tr.AlignmentVector)
    assert v.role == "user"
    assert v.intent == {"reduce", "drift", "to", "o", "1"}
    assert v.context == {"studio", "build"}
    assert v.value == {"correctness", "knowledge_integration"}  # lowercased


def test_deterministic_distiller_defaults_for_missing_fields():
    v = tr.DeterministicDistiller().distill({})
    assert v.role == "unknown"
    assert v.intent == set() and v.context == set() and v.value == set()


def _vec(role, intent, context, value):
    return tr.AlignmentVector(role=role, intent=set(intent), context=set(context), value=set(value))


def test_overlap_identical_actors_is_one():
    a = _vec("user", ["x", "y"], ["c"], ["correctness"])
    b = _vec("agent", ["x", "y"], ["c"], ["correctness"])
    ov = tr.overlap([a, b])
    assert ov["dimensions"] == {"intent": 1.0, "context": 1.0, "value": 1.0}
    assert ov["aggregate"] == 1.0


def test_overlap_disjoint_actors_is_zero():
    a = _vec("user", ["x"], ["c1"], ["correctness"])
    b = _vec("agent", ["y"], ["c2"], ["performance"])
    ov = tr.overlap([a, b])
    assert ov["dimensions"] == {"intent": 0.0, "context": 0.0, "value": 0.0}
    assert ov["aggregate"] == 0.0


def test_overlap_partial_is_exact_jaccard():
    # intent: {x,y} vs {y,z} -> inter {y}=1, union {x,y,z}=3 -> 1/3
    a = _vec("user", ["x", "y"], ["c"], ["correctness"])
    b = _vec("agent", ["y", "z"], ["c"], ["correctness"])
    ov = tr.overlap([a, b])
    assert abs(ov["dimensions"]["intent"] - (1 / 3)) < 1e-9
    assert ov["dimensions"]["context"] == 1.0
    assert ov["dimensions"]["value"] == 1.0


def test_overlap_all_empty_dimension_is_vacuously_one():
    a = _vec("user", [], [], [])
    b = _vec("agent", [], [], [])
    ov = tr.overlap([a, b])
    assert ov["aggregate"] == 1.0
