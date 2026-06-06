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


def test_score_value_credits_positive_claim_when_dimension_shared():
    a = _vec("user", ["i"], ["c"], ["knowledge_integration"])
    b = _vec("agent", ["i"], ["c"], ["knowledge_integration"])
    action = {"value_claims": ["no new deps", "reuses"]}
    # both claims map to knowledge_integration (+1 each), dim shared -> +2.0
    assert tr.score_value(action, [a, b]) == 2.0


def test_score_value_no_credit_when_dimension_not_shared():
    a = _vec("user", ["i"], ["c"], ["correctness"])
    b = _vec("agent", ["i"], ["c"], ["performance"])  # no shared value dim
    action = {"value_claims": ["no new deps"]}
    assert tr.score_value(action, [a, b]) == 0.0


def test_score_value_negative_claims_subtract():
    a = _vec("user", ["i"], ["c"], ["knowledge_integration"])
    b = _vec("agent", ["i"], ["c"], ["knowledge_integration"])
    action = {"value_claims": ["new dependency", "duplicate"]}
    assert tr.score_value(action, [a, b]) == -2.0


def test_score_value_maps_claims_to_correct_dimensions():
    a = _vec("user", ["i"], ["c"], ["performance", "correctness"])
    b = _vec("agent", ["i"], ["c"], ["performance", "correctness"])
    action = {"value_claims": ["o(1)", "tested"]}  # performance +1, correctness +1
    assert tr.score_value(action, [a, b]) == 2.0


def test_score_value_ignores_unknown_claims():
    a = _vec("user", ["i"], ["c"], ["knowledge_integration"])
    b = _vec("agent", ["i"], ["c"], ["knowledge_integration"])
    action = {"value_claims": ["banana"]}
    assert tr.score_value(action, [a, b]) == 0.0


def test_resolve_passes_when_aligned_and_value_positive():
    actors = [
        {"role": "user", "intent": "reduce drift", "context": "studio", "values": ["knowledge_integration"]},
        {"role": "agent", "intent": "reduce drift", "context": "studio", "values": ["knowledge_integration"]},
    ]
    action = {"summary": "reuse store", "value_claims": ["no new deps"]}
    v = tr.resolve(action, actors)
    assert v.passed is True
    assert v.alignment == 1.0
    assert v.value == 1.0
    assert v.dissent == []
    assert "alignment=1.00" in v.rationale


def test_resolve_fails_and_names_dissent_when_misaligned():
    actors = [
        {"role": "user", "intent": "reduce drift", "context": "studio", "values": ["knowledge_integration"]},
        {"role": "subagent", "intent": "rewrite everything", "context": "backend", "values": ["knowledge_integration"]},
    ]
    action = {"summary": "x", "value_claims": ["no new deps"]}
    v = tr.resolve(action, actors)
    assert v.passed is False
    # intent and context are disjoint -> both below threshold -> dissent names role:dim
    assert "user:intent" in v.dissent or "subagent:intent" in v.dissent
    assert any(d.endswith(":context") for d in v.dissent)


def test_resolve_fails_when_value_not_positive_even_if_aligned():
    actors = [
        {"role": "user", "intent": "same", "context": "same", "values": ["knowledge_integration"]},
        {"role": "agent", "intent": "same", "context": "same", "values": ["knowledge_integration"]},
    ]
    action = {"summary": "x", "value_claims": ["new dependency"]}  # -1 value
    v = tr.resolve(action, actors)
    assert v.alignment == 1.0
    assert v.value == -1.0
    assert v.passed is False


def test_resolve_threshold_is_overridable():
    actors = [
        {"role": "user", "intent": "x y", "context": "c", "values": ["knowledge_integration"]},
        {"role": "agent", "intent": "y z", "context": "c", "values": ["knowledge_integration"]},
    ]
    action = {"value_claims": ["no new deps"]}
    # intent overlap 1/3, context 1.0, value 1.0 -> aggregate ~0.778
    high = tr.resolve(action, actors, threshold=0.9)
    assert high.passed is False
    low = tr.resolve(action, actors, threshold=0.5)
    assert low.passed is True


FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def test_llm_distiller_interface_is_satisfiable_without_implementing_it():
    # The seam is real: a trivial conforming stub passes the Protocol check,
    # and the prototype does NOT ship an LLMDistiller class.
    class _StubLLMDistiller:
        def distill(self, actor):
            return tr.AlignmentVector(role=actor.get("role", "x"),
                                      intent=set(), context=set(), value=set())
    assert isinstance(_StubLLMDistiller(), tr.Distiller)
    assert not hasattr(tr, "LLMDistiller")


def test_main_returns_zero_and_prints_passed_on_pass_fixture(capsys):
    rc = tr.main([os.path.join(FIXTURES, "action_pass.json")])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert out["passed"] is True
    assert out["value"] == 2.0
    assert out["dissent"] == []


def test_main_returns_one_on_fail_fixture(capsys):
    rc = tr.main([os.path.join(FIXTURES, "action_fail.json")])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert out["passed"] is False


def test_main_usage_when_no_args(capsys):
    rc = tr.main([])
    assert rc == 2
    assert "usage" in capsys.readouterr().out.lower()


def test_resolve_runs_with_subprocess_cli(tmp_path):
    # End-to-end: invoke the module as a script against the pass fixture.
    script = os.path.join(os.path.dirname(__file__), "..", "scripts", "truth_resolver.py")
    fixture = os.path.join(FIXTURES, "action_pass.json")
    result = subprocess.run([sys.executable, script, fixture], capture_output=True, text=True)
    assert result.returncode == 0
    assert '"passed": true' in result.stdout
