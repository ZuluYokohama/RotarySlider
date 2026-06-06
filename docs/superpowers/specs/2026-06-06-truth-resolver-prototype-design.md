# Truth-Resolver Prototype — Design Spec

> **Status:** Approved for planning (2026-06-06)
> **Author:** ZuluYokohama (b.jones@jtech.ai), via Claude Code brainstorming
> **Scope:** Sub-project SP2 (the Module), built **prototype-first**. SP1 (doctrine doc) is
> back-filled from what the prototype proves; SP3 (agent operating-mode binding) is a later cycle.

## 1. Purpose

A standalone gate that, given a proposed **action** and the **actors** involved
(user / agent / subagent / element), returns a **Verdict**: is the action *aligned* across the
actors' distilled **intent**, **context**, and **value**, and is it **net-positive on value**?

It operationalises the repo's `[ INTENT ] ≡ [ CODE OPS ] ≡ [ VALUE GEN ]` doctrine as a runnable
resolver. Unlike the existing deterministic gates (`aaa_quality`, `evolution_gate`: flake8 /
bandit / radon / pytest), this gate scores **semantic alignment** — so its one genuinely-semantic
step is quarantined behind a pluggable interface (the "seam"), letting the prototype run and
unit-test deterministically today while leaving a drop-in upgrade to an LLM distiller later.

**Prototype boundary:** standalone callable + CLI (`python scripts/truth_resolver.py action.json`)
and an importable `resolve(...)`. It does **not** wire into the live evolution loop, call any LLM,
or touch the in-flight R3F work.

## 2. Core model

Each actor contributes an `AlignmentVector { intent, context, value }`. The pipeline isolates the
semantic step to `Distiller.distill`:

```text
Distiller.distill(raw_actor)  -> AlignmentVector        # ← THE SEAM (deterministic now, LLM later)
overlap(vectors)              -> per-dimension alignment 0..1   # deterministic (Jaccard)
score_value(action, vectors)  -> net value (float)             # deterministic (weighted delta)
resolve(alignment, value)     -> Verdict
```

- **`Distiller`** is an interface (Python `Protocol`/ABC). `DeterministicDistiller` (this prototype):
  normalises free text into lowercased token/tag sets per dimension. `LLMDistiller` (future, NOT in
  this prototype): same interface, calls a model to distill normalized intent/context/value.
- **`overlap`** computes pairwise + aggregate alignment of `intent`, `context`, and `value` token
  sets across actors using Jaccard similarity (|A∩B| / |A∪B|), returning a 0..1 score per dimension
  and an aggregate (mean of dimension scores).
- **`score_value`** scores the action's net value as a weighted sum over value dimensions
  (see §4), where each dimension's contribution is the action's claimed/realised delta on that
  dimension, gated by whether the actors share that value (no shared value → no credit).

## 3. The Verdict (output)

```python
@dataclass
class Verdict:
    passed: bool        # alignment >= ALIGN_THRESHOLD AND value > 0.0
    alignment: float    # 0..1 aggregate overlap across actors
    value: float        # net value score (may be negative)
    rationale: str      # human-readable explanation of the decision
    dissent: list[str]  # actor/dimension pairs that broke alignment, e.g. "subagent:context"
```

`dissent` is the load-bearing output: it names *where* truth failed to resolve so a misalignment is
actionable, not just a red light. `ALIGN_THRESHOLD` is a module constant (default `0.5`),
overridable per call.

## 4. "Value, dimensioned for knowledge integration"

`score_value` evaluates the action across explicit **value dimensions**:

- `correctness`, `performance`, `security` — mirroring the existing gate family.
- **`knowledge_integration`** — the dimension named in the original intent. Scores how much the
  action *coheres* with existing knowledge: reuses existing abstractions, reduces drift, and
  preserves the `[INTENT]≡[CODE OPS]≡[VALUE GEN]` isomorphism, vs fragments it. Concretely, the
  prototype derives this from the action's `value_claims` (e.g. `"no new deps"`, `"reuses X"`,
  `"DRY"` raise it; `"new dependency"`, `"duplicate"`, `"fork-specific"` lower it) intersected with
  the actors' shared values. This structurally **rewards DRY, isomorphic, low-drift actions** —
  encoding the repo's own doctrine as a scoring dimension.

Dimension weights are a module-level dict (default equal weights), overridable per call.

## 5. Inputs

A JSON document describing the action and actors:

```json
{
  "action": {
    "summary": "Tunnel intent form to 3D pulse via a hand-rolled store",
    "value_claims": ["no new deps", "reuses useSyncExternalStore", "O(1)"]
  },
  "actors": [
    {"role": "user",     "intent": "...", "context": "...", "values": ["correctness", "knowledge_integration"]},
    {"role": "agent",    "intent": "...", "context": "...", "values": ["correctness", "performance"]},
    {"role": "subagent", "intent": "...", "context": "...", "values": ["correctness"]}
  ]
}
```

`role`, `intent`, `context` are strings; `values` is a list of value-dimension names. The CLI reads
this from a file path argument; `resolve()` accepts the parsed dict (or typed objects).

## 6. File structure

- `scripts/truth_resolver.py` — dataclasses (`AlignmentVector`, `Verdict`), the `Distiller`
  interface + `DeterministicDistiller`, the pure functions (`overlap`, `score_value`, `resolve`),
  and a `main()` CLI entry. One file, one responsibility (resolve truth for an action); kept under
  ~200 lines. If it grows past that, split `distillers.py` out — but not preemptively (YAGNI).
- `tests/test_truth_resolver.py` — unit tests (see §7).

No changes to any existing file in this prototype.

## 7. Testing (TDD, deterministic)

Red/green unit tests for every pure piece:

- `overlap`: identical actors → 1.0; fully disjoint → 0.0; partial → exact Jaccard value;
  per-dimension breakdown correct.
- `score_value`: net-positive claims vs shared values → positive; value claimed but unshared by
  actors → no credit; drift-claims (`"new dependency"`) → negative contribution.
- `resolve`: alignment ≥ threshold AND value > 0 → `passed=True`; either failing → `False`, with
  correct `dissent` entries naming the actor:dimension that broke alignment.
- `DeterministicDistiller`: text → normalized token/tag sets (lowercase, punctuation-stripped,
  known value-tags mapped).
- `LLMDistiller` is **not** implemented here; a test asserts the `Distiller` interface is satisfiable
  (a trivial stub conforms) so the seam is real.

Runs green with no API key, like the other gates. `pytest -q` is the runner.

## 8. Composition & future cycles (out of scope here)

- **SP1 (doctrine doc):** `docs/TRUTH_RESOLVER.md`, a sibling to `ISOMORPHISM_MANIFESTO.md`,
  back-filled from the prototype's proven model. Later cycle.
- **SP2-proper (live integration):** wire `resolve()` into the evolution/AAA pre-gate as an
  alignment pre-check. Later cycle.
- **SP3 (agent operating-mode):** bind the orchestrator's autonomous "fix-for-value" behaviour to a
  `resolve()` alignment check (the safe form of the perpetual-permission grant) via a memory/feedback
  preference and optional hooks. Later cycle. **Irreversible/outward-facing actions remain
  human-gated regardless of resolver verdict.**

## 9. Definition of Done (prototype)

- `scripts/truth_resolver.py` implements §2–§5 with the pluggable `Distiller` seam.
- `pytest -q tests/test_truth_resolver.py` is green (no API key).
- CLI runs against a sample `action.json` and prints a Verdict (pass + fail examples).
- No existing file modified; no LLM call; R3F work untouched.

## 10. Risks & constraints

- **Semantic fidelity:** the deterministic distiller reduces "distillation" to token/tag overlap —
  honest about this; the seam exists precisely so the real semantics arrive via `LLMDistiller`
  without a rewrite. The prototype proves the *pipeline and contract*, not production-grade alignment.
- **Value scoring is heuristic:** `score_value` over `value_claims` is a deliberately simple,
  inspectable heuristic for the prototype, not a learned model. Documented as such.
- **Determinism:** no `Date.now()`/random; all scoring is pure functions of inputs, so tests are
  exact.
