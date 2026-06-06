# IsoZ Identity & Positioning — Design Spec (Cycle 1)

> **Status:** Approved-in-brainstorm 2026-06-06 (direction, name, and key decisions chosen by the user).
> **Author:** ZuluYokohama (b.jones@jtech.ai) via Claude Code brainstorming.
> **Cycle 1 of 3.** Cycle 2 = code-symbol demotion (module/function renames). Cycle 3 = website (deferred for a real screenshot).

## 1. Goal

Unify the project's four-way fragmented identity (repo *RotarySlider* · README *Autoresearch Superpowers* ·
plugin *rotary-slider-matrix* · website *Surface & Structure UI*) under one honest brand — **IsoZ** —
and rewrite the README around the project's true thesis: **the honest, minimal, *running* embodiment
of Geometric Determinism** (`intent ≡ code ≡ value` as a sheaf Global Section), seeded by
`scripts/truth_resolver.py`.

**Direction (chosen):** *Hybrid with a Z-brand* — honest substance, a deliberate Z-harmonized brand skin,
never a false-capability claim.

## 2. Identity model

- **Canonical brand: IsoZ**, content-facing everywhere (README H1, website headline, CLI banner,
  plugin description). "IsoZ" = *isomorphism* — the project's real thesis (`intent ≡ code ≡ value` =
  Global Section), grounded in the user's **AxiomZ / Jones Framework** theory (see `docs/theory/`).
- **Repo: rename `RotarySlider` → `IsoZ`** (chosen). GitHub auto-redirects old clone/Pages URLs;
  perform the rename when no other PRs are mid-flight, and update the local remote + the live Pages
  URL reference (`github.io/RotarySlider` → `/IsoZ`).
- **Visual marks:** the **rotary dial** (now real, built in C2) = the logo; the **Alpha Rig** = the
  sanctioned mascot flourish.
- **Author identity:** unify attribution to *jtechAi Labs (ZuluYokohama)* going forward (`git config`).
  The three historical commit identities (BravoWon / Nomo Yokahaaka / ZuluYokohama) are one author —
  noted, not history-rewritten.

## 3. Vocabulary — honest substance, Z-brand skin

Rule: **brand-skin is allowed on *presentation*, never on *capability claims*.** Cycle 1 applies the
demotions to **user-facing docs/strings**; Cycle 2 applies them to **code symbols** (module/function
renames) — the user chose *aggressive demotion everywhere incl. code*, split across the two cycles by risk.

| Current (overclaim) | IsoZ (honest) | Cycle |
|---|---|---|
| "Autoresearch Superpowers" (README H1) | **IsoZ** + honest descriptor; credit inherited layers | 1 |
| "Surface & Structure UI" / "rotary-slider-matrix" | **IsoZ** (website headline, plugin description) | 1 |
| CLI banner "Autoresearch Superpowers – Swarm CLI" | **IsoZ** CLI | 1 |
| "Quantum-Resistant Cryptography Gate" | **weak-crypto denylist lint** (drop "Quantum-Resistant") | 1 docs / 2 code (`quantum_gate.py`→`crypto_denylist.py`) |
| "Akashic Records / evolutionary memory" | **failure cache** | 1 docs / 2 code (`akashic_records.py`→`failure_cache.py`) |
| "Infinite Recursive LLM Swarm" | **evolution loop (demo)** | done (`[DEMO]`, PR #24) |
| Bandit = "cryptographic checks" | **security linter** | 1 |
| "MaxVal" / "the Matrix" | **value score** / **3D scene** | 1 docs / 2 code/skill |

## 4. README rewrite (Cycle 1)

New structure:

1. **H1 IsoZ** + a one-paragraph honest "what it is": a Feature Studio (Next.js + R3F 3D control
   surface, FastAPI backend, Svelte telemetry) plus a pluggable gate framework, whose thesis is a
   deterministic `intent ≡ code ≡ value` alignment gate (`truth_resolver`).
2. **The thesis** — link `docs/theory/GEOMETRIC_DETERMINISM.md`; state plainly that the decks are the
   *vision* and `truth_resolver` is the current *seed* (the honesty split). Link the roadmap.
3. **Two-layer credit split** — *Inherited* (Jesse Vincent's superpowers methodology + Karpathy's
   autoresearch; honest attribution, scoped install notes) vs *IsoZ original* (the Studio, the gate
   scripts, `truth_resolver`).
4. **Document the Feature Studio** (currently absent): real run instructions —
   `python scripts/api_server.py`, `cd ui/studio && npm run dev`, `cd ui/telemetry && npm run dev`.
5. **Honest gate descriptions** (apply the §3 demotions in prose); fix the Bandit mislabel.

## 5. Theory foundation (Cycle 1 — already drafted)

- `docs/theory/GEOMETRIC_DETERMINISM.md` — synthesis of the three decks + the buildable-vs-vision split.
- `docs/theory/TRUTH_RESOLVER_ROADMAP.md` — v1→v2(sheaf coherence)→v3(commit-vs-resolve)→v4(Oracle) path.

These ground the IsoZ thesis in real theory while enforcing the honesty discipline.

## 6. Scope & sequencing

- **Cycle 1 (this spec):** repo rename → IsoZ; README rewrite; user-facing doc/string demotions
  (manifesto, brand doc, CLI banner, plugin.json description, website-URL references); theory docs.
- **Cycle 2:** code-symbol demotion — rename `akashic_records.py`/`quantum_gate.py`, demote
  `MaxVal`/`Matrix` symbols, fix all imports/callers/Makefile/MCP/skill, **run-verify each**. Own spec.
- **Cycle 3:** website `index.html` rewrite (IsoZ, a11y, honest copy) — deferred for a real studio screenshot.

Each cycle is its own worktree → PR → CodeRabbit → merge, human-gated (outward-facing).

## 7. Definition of Done (Cycle 1)

- Repo renamed to IsoZ; local remote + Pages reference updated.
- README rewritten: IsoZ H1, honest thesis with the decks=vision / code=seed split, two-layer credit,
  Feature Studio documented, gate descriptions demoted, Bandit mislabel fixed.
- User-facing strings (CLI banner, plugin.json description, manifesto/brand-doc headers) say IsoZ and
  drop false-capability terms (esp. "Quantum-Resistant").
- `docs/theory/` reference + roadmap committed.
- No code-symbol renames yet (that's Cycle 2); nothing broken.

## 8. Risks

- **Repo rename timing** — do it with no PRs mid-flight; verify redirects; update the gh-pages URL note.
- **Re-inflation risk** — folding the decks could re-import overclaim; mitigated by the explicit
  vision/seed honesty split in both the README and `docs/theory/`.
- **Scope discipline** — Cycle 1 must NOT touch code symbols (defer to Cycle 2) to keep it low-risk.
