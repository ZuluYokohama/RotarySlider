# Geometric Determinism — The Theory Behind IsoZ

> **What this is:** a faithful synthesis of the three foundational decks authored by ZuluYokohama
> (jtechAi Labs) — *The Geometry of Truth*, *Geometric Determinism*, and *The ZuluYokohama Protocol*.
> Together they are one layered theory (the **AxiomZ / Jones Framework**). IsoZ is its honest,
> minimal, *running* seed.
>
> **Honesty discipline (read first):** the decks are *manifesto-grade*. They name heavy mathematics
> (ATFT, a claimed Berry–Keating/Riemann correspondence, "mathematically guaranteed zero
> hallucination", a Ternary-Crystal hardware substrate) that is **asserted, not proven**, and is far
> beyond any code that exists. This document extracts the **buildable core** and explicitly separates
> it from the **aspirational vision**. Per the project's own `intent ≡ code ≡ value` doctrine: the
> decks are the *vision*; the code is the *current truth*; this file labels which is which.

## 1. The three decks are one stack

| Deck | Layer | Core claim |
|------|-------|-----------|
| **The Geometry of Truth** | WHY (conceptual) | Truth is geometric, not statistical. Truth = a **Global Section** of a cellular sheaf: all local views ("stalks") agree on their overlaps, so the **Sheaf Laplacian reaches zero (Dirichlet) energy**. **Value warps the metric** (the Information-Geometric Valuation Framework, IGVF): human intent is a "gravity well", and the aligned solution is the geodesic / "path of least resistance". A contradiction is a **cohomological obstruction** → the action is hard-blocked. Organizing metaphor: Map (Sheaves) · Compass (IGVF) · Pilot (the human, "MaxOp") · Engine (the Protocol). |
| **Geometric Determinism** | WHAT (formal) | Structure → *deterministic* computation → truth/value. The **Configurational Term Series** `X → f(x) → ℳ → v → ℳ_v → H_k → Q(Φ)`. The discrete **Sheaf Laplacian** `L_F = (δ⁰)*δ⁰`; cohomology diagnostics `H⁰` (coherence) / `H¹` (voids) / `H²` (obstructions). A **Commit-vs-Resolve** safety protocol: simulate, accept only if the spectral gap is preserved (`Δλ₁ ≥ 0`) and coherence strictly increases, else hard-block and log. Type-theory equality (isomorphism = inverse-morphism pairs) is chosen over set/category theory for computational V&V. A **Z-Axis "ladder of abstraction"** (Layers 0–5) forbids layer-skipping to prevent "Zombie" (syntactically valid, semantically ungrounded) states. |
| **The ZuluYokohama Protocol** | HOW (systems) | A bandwidth-first execution substrate: SHEAF-OS / ATFT, a quantized **Ternary Crystal** (Void/Identity/Prime) weight alphabet, sparse zero-copy dataflow, an **edge→Oracle** offload of unsolvable obstructions, and **geometry-penalized learning** (loss weighted by topological coherence shift `Δλ₁`). |

## 2. Topic abstraction — the six load-bearing, *buildable* ideas

Stripped of the manifesto framing, six ideas survive that are implementable today:

1. **Truth = coherence.** A claim-set is "true" when its local parts glue into a consistent global whole (sheaf global section / low Dirichlet energy) — not when it is probable.
2. **Alignment = agreement-on-overlap.** Model actors/views as stalks with restriction maps; consistency is measured on their *overlapping intersections*. This argues *for* set-overlap and *against* flat cosine-on-embeddings as the source of truth.
3. **Value = metric-warp.** Value is a *weighting field* over the space (IGVF), not a separate similarity. What you value bends the geometry so the valued solution becomes lowest-cost.
4. **Contradiction = obstruction.** An irreconcilable conflict is a cohomological obstruction (`H¹ ≠ 0`) → a deterministic **hard halt** ("zero-bypass gate"), not a soft low score.
5. **Determinism over stochastic.** Truth/value should be a *reproducible* function of structure (spectral invariants), not an LLM's judgment — so the same input always yields the same verdict.
6. **Commit-vs-Resolve.** Don't act, then filter. *Simulate* a change against the structure and **commit only if coherence does not decrease** (`Δλ₁ ≥ 0`).

## 3. The formal anchors (transcribed from the decks)

- **Sheaf Laplacian** (Geometric Determinism, slide 8): `L_F = (δ⁰)*δ⁰`; on a graph `G=(V,E)` acting on a 0-cochain `x`:
  `(L_F⁰ x)(v) = Σ_{e:v∼w} ℱ_{v⊴e}^T ( ℱ_{v⊴e} x(v) − ℱ_{w⊴e} x(w) )`, with restriction maps `ℱ`.
  Diagnostics: `H⁰` coherence (nullspace dim / `λ₁` stability), `H¹` voids (cycles / missing deps), `H²` obstructions.
- **Configurational Term Series** (calculus of emergence): `X → f(x) → ℳ → v → ℳ_v → H_k → Q(Φ)` — substrate → constrained dynamics → manifold → **value-warp `v`** → value-warped manifold → persistent homology (`β₀` clusters, `β₁` loops) → `Q(Φ)` the irreducible truth-form.
- **Truth = Global Section** (Geometry of Truth, slide 8): all locals agree on overlaps ⇔ Sheaf Laplacian zero energy ⇔ Dirichlet energy minimized.
- **Value geometry** (slides 11–13): base = Fisher Information Metric; an observer-dependent **Value Function `v`** warps it into a gravity well; aligned solution = geodesic.
- **Commit/Resolve invariant** (ZuluYokohama, slide 13; Geometric Determinism, slide 11): `loss = ce_loss · (1 + max(0, Δλ₁)·w)`; accept iff `Δλ₁ ≥ 0`; successful transitions emit "Shape Pairs" `(K_pre, K_post)`.

## 4. Buildable core vs. aspirational vision

**Buildable now (informs IsoZ / `truth_resolver`):** sheaf-style overlap/coherence scoring, value-weighted overlap, obstruction-as-halt, deterministic reproducibility, commit-vs-resolve gating, the pluggable Oracle/O-Box seam, no-layer-skipping verification.

**Aspirational vision (NOT code; label as roadmap/manifesto):** ATFT, the claimed exact Berry–Keating/Riemann (zeta) correspondence, "mathematically guaranteed zero hallucination", the Ternary-Crystal hardware substrate, HBM4/NVLink/NoC execution, persistent-homology phase detection at scale. These are named but unproven in the decks and unimplemented in code. Cite them as *direction*, never as *capability*.

## 5. Why this matters for IsoZ

IsoZ's thesis is not "a 3D studio + some gates." It is **the honest, minimal, running embodiment of Geometric Determinism**: a place where `intent ≡ code ≡ value` is the *Global Section / isomorphism* condition, made concrete by `scripts/truth_resolver.py`. The upgrade path from that 187-line seed toward the sheaf-coherence model is in [`TRUTH_RESOLVER_ROADMAP.md`](./TRUTH_RESOLVER_ROADMAP.md).

> Source decks (image-based PPTX): `The_Geometry_of_Truth.pptx` (21 slides), `Geometric_Determinism.pptx` (15), `The_ZuluYokohama_Protocol.pptx` (14). Full per-slide extractions were produced during the 2026-06-06 session.
