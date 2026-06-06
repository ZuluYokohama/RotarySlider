# truth_resolver Roadmap — From Jaccard Seed to Sheaf Coherence

> Maps the [Geometric Determinism theory](./GEOMETRIC_DETERMINISM.md) onto a concrete, honest
> upgrade path for `scripts/truth_resolver.py`. Each stage is independently shippable and keeps the
> determinism + pluggable-seam discipline the prototype already has. **This is a direction, not a
> promise** — only v1 exists today.

## v1 — Shipped (PR #19)

A deterministic gate: each actor's `intent`/`context`/`value` is distilled into token/tag sets;
alignment = mean Jaccard overlap across the three dimensions; value = a shared-value-gated claim
score; output = `Verdict{passed, alignment, value, rationale, dissent}` where `dissent` names the
`actor:dimension` pairs that broke alignment. A `Distiller` Protocol is the pluggable seam
(`DeterministicDistiller` now; an LLM distiller later). 26 tests, stdlib-only, no API key.

**Theory mapping:** Jaccard-on-overlap ≈ a poor-man's *agreement-on-intersections*; `dissent` ≈ a
coarse *obstruction localization*; the `Distiller` seam ≈ the decks' **O-Box / Oracle**.

## v2 — Sheaf coherence (the core upgrade)

Replace ad-hoc Jaccard with the actual sheaf model from the theory.

| Aspect | v1 | v2 |
|--------|----|----|
| Representation | flat token sets per actor | **stalks**: a vector per actor over a shared concept base + **restriction maps** between actors |
| Alignment | mean Jaccard | **`1 − normalized Dirichlet energy`** of the sheaf Laplacian `L_F` (true Global-Section coherence; perfect agreement → 1.0) |
| Value | shared-value gating of claims | **value-weighted overlap** — value is a weighting field over cells (IGVF metric-warp); already foreshadowed by `score_value`'s shared-value gate |
| `dissent` | `actor:dimension` list | **`H¹` obstruction localization** — the specific edges/cells whose restriction maps fail to glue |
| Gate | soft `passed` (alignment ≥ θ AND value > 0) | soft score **plus** a deterministic **obstruction halt** (any irreconcilable cell ⇒ blocked, not low-scored) |

Deliverable: a `sheaf.py` helper (build incidence/coboundary `δ⁰`, restriction maps, `L_F = (δ⁰)*δ⁰`,
Dirichlet energy, nullspace/`λ₁`) wired behind the existing `resolve()` API. Still deterministic,
still unit-testable with exact numbers (small graphs have closed-form Laplacians).

## v3 — Commit-vs-Resolve gate

Turn `truth_resolver` from a standalone scorer into a **pre-commit / evolution gate**:

1. **Propose** a change (a diff, a spec edit, an agent action).
2. **Resolve** — recompute the intent≡code≡value sheaf coherence *with the change simulated*.
3. **Commit** only if coherence does not decrease (`Δλ₁ ≥ 0`); else **halt + log** the obstruction.

This is the decks' Commit-vs-Resolve / "zero-bypass" protocol, scaled down to a CI/commit hook —
a principled "does this change preserve intent-alignment?" check. It composes with the existing
`evolution_gate_template.py` and the (now-honest) `aaa_quality.py` gate family.

## v4+ — Pluggable semantics (the Oracle), still bounded

Swap `DeterministicDistiller` for an `LLMDistiller` behind the *same* `Distiller` Protocol — the
decks' **O-Box / Oracle** that injects richer meaning while the deterministic sheaf skeleton (and its
reproducible verdict structure) stays fixed. The gate never becomes stochastic; only the *distillation
of raw input into stalks* gains semantics.

## Out of scope (vision, not roadmap)

ATFT, the Berry–Keating/Riemann correspondence, the Ternary-Crystal hardware substrate, and
bandwidth-level execution claims from *The ZuluYokohama Protocol* are **not** on this roadmap. They
are research-vision; cite them as such, never as shipped capability.

## Guardrail

Every stage must preserve the prototype's three invariants: **deterministic** (same input → same
verdict), **unit-tested with exact expected values**, and **honest** (the README/docs state which
stage actually exists). v1 is real; v2+ are proposals until built and merged.
