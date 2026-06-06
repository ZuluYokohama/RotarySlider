# Truth-Resolver Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, unit-tested `truth_resolver.py` prototype gate that scores whether a proposed action is aligned (across actors' intent/context/value) and net-positive on value, with the one semantic step isolated behind a pluggable `Distiller` seam.

**Architecture:** Pure-function pipeline `distill → overlap → score_value → resolve`. The only swappable part is `Distiller` (a `runtime_checkable` Protocol); the prototype ships `DeterministicDistiller` (text → token/tag sets) and intentionally does NOT implement `LLMDistiller` (a test only asserts the interface is satisfiable). All scoring is pure functions of inputs — no `Date`/random, no LLM, no network — so tests are exact.

**Tech Stack:** Python 3.14, stdlib only (`dataclasses`, `typing.Protocol`, `re`, `json`, `sys`), `pytest` as the test runner. Follows the repo convention: tests `sys.path`-append `../scripts` and import modules by bare name.

---

## File Structure

- **Create** `scripts/truth_resolver.py` — the whole prototype (dataclasses, `Distiller` Protocol + `DeterministicDistiller`, pure functions `overlap`/`score_value`/`resolve`, helpers, `main()` CLI). One responsibility: resolve truth for an action. Target < 200 lines.
- **Create** `tests/test_truth_resolver.py` — pytest tests, grown one task at a time.
- **Create** `tests/fixtures/action_pass.json`, `tests/fixtures/action_fail.json` — CLI fixtures (Task 6).
- **Modify:** none. No existing file is touched; nothing is wired into the evolution loop.

**Test file header** (created in Task 1, unchanged after): every test references the module as `tr.<symbol>`, so a not-yet-written function fails with `AttributeError` (RED) without breaking the file import.

```python
import os
import sys
import json
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import truth_resolver as tr  # noqa: E402
```

---

## Task 0: Ensure pytest is available (one-time)

- [ ] **Step 1: Check/instal pytest**

Run: `python -m pytest --version`
If it errors with "No module named pytest", run: `python -m pip install --quiet --disable-pip-version-check pytest`
Expected: a version prints (e.g. `pytest 8.x`).

(No commit — environment setup only.)

---

## Task 1: Module scaffold — constants, dataclasses, `Distiller` protocol

**Files:**
- Create: `scripts/truth_resolver.py`
- Create: `tests/test_truth_resolver.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_truth_resolver.py` with the header above, then append:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'truth_resolver'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/truth_resolver.py`:

```python
"""Truth-Resolver prototype gate.

Resolves whether a proposed action is aligned across the involved actors'
intent / context / value, and net-positive on value. Deterministic pipeline
with the single semantic step (distillation) isolated behind the `Distiller`
interface so an LLM-backed distiller can drop in later without a rewrite.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

ALIGN_THRESHOLD = 0.5
VALUE_DIMENSIONS = ("correctness", "performance", "security", "knowledge_integration")
DEFAULT_WEIGHTS = {d: 1.0 for d in VALUE_DIMENSIONS}


@dataclass
class AlignmentVector:
    """One actor's distilled stance, as token/tag sets per dimension."""
    role: str
    intent: set[str]
    context: set[str]
    value: set[str]


@dataclass
class Verdict:
    """The resolver's decision for an action."""
    passed: bool
    alignment: float
    value: float
    rationale: str
    dissent: list[str]


@runtime_checkable
class Distiller(Protocol):
    """The pluggable seam: turn a raw actor dict into an AlignmentVector."""
    def distill(self, actor: dict) -> AlignmentVector: ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/truth_resolver.py tests/test_truth_resolver.py
git commit -m "feat(truth-resolver): scaffold dataclasses + Distiller protocol"
```

---

## Task 2: `DeterministicDistiller` (text → token/tag sets)

**Files:**
- Modify: `scripts/truth_resolver.py`
- Test: `tests/test_truth_resolver.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_truth_resolver.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_truth_resolver.py -q -k distiller or tokens`
Expected: FAIL — `AttributeError: module 'truth_resolver' has no attribute '_tokens'`.

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/truth_resolver.py` (after the `Distiller` protocol, add the `re` import at the top with the other imports):

```python
import re
```

```python
def _tokens(text: str) -> set[str]:
    """Lowercase, split on non-alphanumerics, drop empties."""
    return {t for t in re.split(r"[^a-z0-9]+", text.lower()) if t}


class DeterministicDistiller:
    """Default distiller: normalize free text into token/tag sets. No LLM."""
    def distill(self, actor: dict) -> AlignmentVector:
        return AlignmentVector(
            role=actor.get("role", "unknown"),
            intent=_tokens(actor.get("intent", "")),
            context=_tokens(actor.get("context", "")),
            value={v.strip().lower() for v in actor.get("values", [])},
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: PASS (5 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/truth_resolver.py tests/test_truth_resolver.py
git commit -m "feat(truth-resolver): add DeterministicDistiller + tokenizer"
```

---

## Task 3: `overlap` (Jaccard per dimension + aggregate)

**Files:**
- Modify: `scripts/truth_resolver.py`
- Test: `tests/test_truth_resolver.py`

- [ ] **Step 1: Write the failing test**

Append:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_truth_resolver.py -q -k overlap`
Expected: FAIL — `AttributeError: ... has no attribute 'overlap'`.

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/truth_resolver.py`:

```python
def _jaccard_all(sets: list[set[str]]) -> float:
    """Multi-set Jaccard: |intersection of all| / |union of all|.

    Empty union (every actor empty on this dimension) is vacuously aligned -> 1.0.
    """
    if not sets:
        return 1.0
    union: set[str] = set().union(*sets)
    if not union:
        return 1.0
    inter = set(sets[0]).intersection(*sets[1:])
    return len(inter) / len(union)


def overlap(vectors: list[AlignmentVector]) -> dict:
    """Per-dimension and aggregate alignment across actors."""
    dims = {
        "intent": _jaccard_all([v.intent for v in vectors]),
        "context": _jaccard_all([v.context for v in vectors]),
        "value": _jaccard_all([v.value for v in vectors]),
    }
    aggregate = sum(dims.values()) / len(dims)
    return {"dimensions": dims, "aggregate": aggregate}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: PASS (9 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/truth_resolver.py tests/test_truth_resolver.py
git commit -m "feat(truth-resolver): add per-dimension Jaccard overlap"
```

---

## Task 4: `score_value` (claim → dimension, gated by shared values)

**Files:**
- Modify: `scripts/truth_resolver.py`
- Test: `tests/test_truth_resolver.py`

- [ ] **Step 1: Write the failing test**

Append:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_truth_resolver.py -q -k score_value`
Expected: FAIL — `AttributeError: ... has no attribute 'score_value'`.

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/truth_resolver.py`:

```python
# claim phrase -> (value dimension, polarity)
CLAIM_MAP = {
    "no new deps": ("knowledge_integration", +1),
    "reuses": ("knowledge_integration", +1),
    "dry": ("knowledge_integration", +1),
    "isomorphic": ("knowledge_integration", +1),
    "low drift": ("knowledge_integration", +1),
    "new dependency": ("knowledge_integration", -1),
    "duplicate": ("knowledge_integration", -1),
    "drift": ("knowledge_integration", -1),
    "fork-specific": ("knowledge_integration", -1),
    "o(1)": ("performance", +1),
    "o(n^2)": ("performance", -1),
    "tested": ("correctness", +1),
    "untested": ("correctness", -1),
    "secure": ("security", +1),
    "insecure": ("security", -1),
}


def score_value(action: dict, vectors: list[AlignmentVector],
                weights: dict | None = None) -> float:
    """Net value: each known claim credits its dimension (weighted), but only
    if every actor shares that value dimension. Unknown claims are ignored."""
    weights = weights or DEFAULT_WEIGHTS
    shared = set.intersection(*[v.value for v in vectors]) if vectors else set()
    score = 0.0
    for claim in action.get("value_claims", []):
        key = claim.strip().lower()
        if key in CLAIM_MAP:
            dim, polarity = CLAIM_MAP[key]
            if dim in shared:
                score += polarity * weights.get(dim, 1.0)
    return score
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: PASS (14 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/truth_resolver.py tests/test_truth_resolver.py
git commit -m "feat(truth-resolver): add shared-value-gated value scoring"
```

---

## Task 5: `resolve` + `_dissent` (the Verdict)

**Files:**
- Modify: `scripts/truth_resolver.py`
- Test: `tests/test_truth_resolver.py`

- [ ] **Step 1: Write the failing test**

Append:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_truth_resolver.py -q -k resolve`
Expected: FAIL — `AttributeError: ... has no attribute 'resolve'`.

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/truth_resolver.py`:

```python
def _dissent(vectors: list[AlignmentVector], dim_scores: dict, threshold: float) -> list[str]:
    """For each below-threshold dimension, name the actors holding tokens that
    are not shared by all actors (i.e. the contributors to the misalignment)."""
    out: list[str] = []
    for dim in ("intent", "context", "value"):
        if dim_scores[dim] >= threshold:
            continue
        sets = [getattr(v, dim) for v in vectors]
        shared = set.intersection(*sets) if sets else set()
        for v in vectors:
            if getattr(v, dim) - shared:
                out.append(f"{v.role}:{dim}")
    return out


def resolve(action: dict, raw_actors: list[dict], distiller: Distiller | None = None,
            threshold: float = ALIGN_THRESHOLD, weights: dict | None = None) -> Verdict:
    """Distill actors, score alignment + value, and gate."""
    distiller = distiller or DeterministicDistiller()
    vectors = [distiller.distill(a) for a in raw_actors]
    ov = overlap(vectors)
    alignment = ov["aggregate"]
    value = score_value(action, vectors, weights)
    passed = alignment >= threshold and value > 0.0
    rationale = (
        f"alignment={alignment:.2f} (>= {threshold}: {alignment >= threshold}); "
        f"value={value:.2f} (> 0: {value > 0.0})"
    )
    return Verdict(
        passed=passed,
        alignment=alignment,
        value=value,
        rationale=rationale,
        dissent=_dissent(vectors, ov["dimensions"], threshold),
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: PASS (18 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/truth_resolver.py tests/test_truth_resolver.py
git commit -m "feat(truth-resolver): add resolve() + dissent reporting"
```

---

## Task 6: CLI `main()` + interface-satisfiable seam test + fixtures

**Files:**
- Modify: `scripts/truth_resolver.py`
- Create: `tests/fixtures/action_pass.json`, `tests/fixtures/action_fail.json`
- Test: `tests/test_truth_resolver.py`

- [ ] **Step 1: Create the fixtures**

Create `tests/fixtures/action_pass.json`:

```json
{
  "action": { "summary": "Reuse the existing store", "value_claims": ["no new deps", "reuses"] },
  "actors": [
    { "role": "user", "intent": "reduce drift", "context": "studio", "values": ["knowledge_integration"] },
    { "role": "agent", "intent": "reduce drift", "context": "studio", "values": ["knowledge_integration"] }
  ]
}
```

Create `tests/fixtures/action_fail.json`:

```json
{
  "action": { "summary": "Add a new framework", "value_claims": ["new dependency"] },
  "actors": [
    { "role": "user", "intent": "stay minimal", "context": "studio", "values": ["knowledge_integration"] },
    { "role": "subagent", "intent": "introduce library", "context": "backend", "values": ["knowledge_integration"] }
  ]
}
```

- [ ] **Step 2: Write the failing test**

Append to `tests/test_truth_resolver.py`:

```python
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
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest tests/test_truth_resolver.py -q -k main or cli or interface`
Expected: FAIL — `AttributeError: ... has no attribute 'main'`.

- [ ] **Step 4: Write minimal implementation**

Add to `scripts/truth_resolver.py` (add `import json` and `import sys` to the top imports):

```python
import json
import sys
```

```python
def main(argv: list[str] | None = None) -> int:
    """CLI: read an action+actors JSON file, print the Verdict as JSON.

    Returns 0 if the verdict passes, 1 if it fails, 2 on usage error.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: truth_resolver.py <action.json>")
        return 2
    with open(argv[0], encoding="utf-8") as f:
        doc = json.load(f)
    verdict = resolve(doc["action"], doc["actors"])
    print(json.dumps({
        "passed": verdict.passed,
        "alignment": round(verdict.alignment, 4),
        "value": verdict.value,
        "rationale": verdict.rationale,
        "dissent": verdict.dissent,
    }, indent=2))
    return 0 if verdict.passed else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: PASS (23 tests total).

- [ ] **Step 6: Final full-suite run**

Run: `python -m pytest tests/test_truth_resolver.py -q`
Expected: all green. Also sanity-run the CLI by hand:
`python scripts/truth_resolver.py tests/fixtures/action_pass.json` → prints `"passed": true`, exit 0.
`python scripts/truth_resolver.py tests/fixtures/action_fail.json` → prints `"passed": false`, exit 1.

- [ ] **Step 7: Commit**

```bash
git add scripts/truth_resolver.py tests/test_truth_resolver.py tests/fixtures/action_pass.json tests/fixtures/action_fail.json
git commit -m "feat(truth-resolver): add CLI main() + seam interface test + fixtures"
```

---

## Definition of Done

- `scripts/truth_resolver.py` implements the full pipeline (`AlignmentVector`, `Verdict`,
  `Distiller` protocol, `DeterministicDistiller`, `overlap`, `score_value`, `resolve`, `main`).
- `python -m pytest tests/test_truth_resolver.py -q` is green (23 tests), no API key, no network.
- CLI runs on both fixtures (pass → exit 0, fail → exit 1).
- `LLMDistiller` is NOT implemented; the seam is proven satisfiable by a stub (Task 6 test).
- No existing file modified; nothing wired into the evolution loop; R3F work untouched.

---

## Self-Review

**1. Spec coverage:** §1 purpose → standalone module + CLI (Task 6); §2 pipeline → Tasks 2–5; the `Distiller` seam → Task 1 (protocol) + Task 2 (deterministic) + Task 6 (interface-satisfiable, no `LLMDistiller`); §3 `Verdict` incl. `dissent` → Task 5; §4 `knowledge_integration` value dimension → Task 4 `CLAIM_MAP`; §5 JSON input → Task 6 fixtures + `main`; §6 single file → all tasks; §7 deterministic TDD → every task is red/green; §9 DoD mirrored above; §10 risks (heuristic value, deterministic) honored (pure functions, documented claim map). All spec sections map to a task. ✅

**2. Placeholder scan:** No TBD/TODO; every step has runnable code and exact commands. ✅

**3. Type/name consistency:** `AlignmentVector{role,intent,context,value}`, `Verdict{passed,alignment,value,rationale,dissent}`, `overlap()->{"dimensions","aggregate"}`, `score_value(action,vectors,weights)`, `resolve(action,raw_actors,distiller,threshold,weights)`, `_tokens`, `_jaccard_all`, `_dissent`, `CLAIM_MAP`, `ALIGN_THRESHOLD`, `VALUE_DIMENSIONS`, `DEFAULT_WEIGHTS`, `main(argv)` — all referenced consistently across tasks and tests. The test file uses `tr.<symbol>` throughout so partial implementations fail with `AttributeError` (clean RED). ✅
