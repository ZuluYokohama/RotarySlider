# 1:1 Isomorphism: Truth in Intent

## The Doctrine of IsoZ
In standard software engineering, there is always drift between what is desired (The Intent), what is written (The Code Ops), and what is delivered (The Value Gen). 

**IsoZ works to eliminate this drift.** Its architecture targets a strict **1:1 Isomorphism** (see the honest vision-vs-seed split in [`theory/GEOMETRIC_DETERMINISM.md`](theory/GEOMETRIC_DETERMINISM.md)).

`[ INTENT ] ≡ [ CODE OPS ] ≡ [ VALUE GEN ]`

### 1. Truth in Intent (The Mathematical Bound)
Intent is never ambiguous or conversational. It is a strict vector (e.g., `O(1) memory overhead`, `Contrast > 4.5:1`). In IsoZ, the `feature_map.json` and the AST oracle serve as the Truth in Intent.

### 2. Code Ops (The Execution Mesh)
Code operations aim to be the manifestation of the Intent. Today a demonstration evolution loop (`[DEMO]` — no real LLM swarm yet; see the roadmap), bounded by the `HardwarePipingManager`, iterates over the feature map; the quality gate (Flake8/Bandit/Radon), the weak-crypto denylist lint, and the Playwright visual check screen each candidate. Where Code Ops deviate from the Intent, those gates flag it.

### 3. Value Gen (the value score)
Value generation is not an arbitrary metric. It is the 1:1 realization of the completed Code Ops passing the Evolution Gate. When a feature is tallied `[PASS]`, the value score is realized.

## Retrospective Alignment of All PRs and Reviews
Every Pull Request, every CodeRabbit AI review, and every line of code committed to this repository represents this 1:1 Isomorphism:
- **PR #2 & #3 (Visual Matrix & UI Mesh):** The visual intent maps 1:1 to the headless Playwright rendering operations, generating aesthetic value.
- **PR #7 (AST Oracle):** The detection of O(N^2) loops maps 1:1 to the generation of memoization ops, yielding performance value.
- **PR #8 & #11 (quality gate & weak-crypto denylist lint):** the intent of code safety maps 1:1 to static AST parsing ops (a security/complexity lint — not cryptographic verification).

There is no gap. There is no abstraction leak. 
**The Intent IS the Code. The Code IS the Value.**
