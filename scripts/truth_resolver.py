"""Truth-Resolver prototype gate.

Resolves whether a proposed action is aligned across the involved actors'
intent / context / value, and net-positive on value. Deterministic pipeline
with the single semantic step (distillation) isolated behind the `Distiller`
interface so an LLM-backed distiller can drop in later without a rewrite.
"""
from __future__ import annotations

import json
import re
import sys
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
