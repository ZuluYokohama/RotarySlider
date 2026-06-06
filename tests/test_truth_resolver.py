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
