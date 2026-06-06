"""Truth-Resolver prototype gate.

Resolves whether a proposed action is aligned across the involved actors'
intent / context / value, and net-positive on value. Deterministic pipeline
with the single semantic step (distillation) isolated behind the `Distiller`
interface so an LLM-backed distiller can drop in later without a rewrite.
"""
from __future__ import annotations

import re
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
