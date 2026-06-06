# IsoZ

> Prototype 0.001a — in dev. Last human update 6 Jun 26 (mr.orange@jtech.ai).

**IsoZ** is a *Feature Studio* for agentic development — a Next.js + React-Three-Fiber 3D control surface (with a FastAPI backend and a SvelteKit telemetry panel) over a pluggable framework of verification **gates**. Its thesis is a single idea made runnable: a **deterministic `intent ≡ code ≡ value` alignment gate** (`scripts/truth_resolver.py`). IsoZ is built on the **Superpowers** development methodology and Andrej Karpathy's **autoresearch** training code, and is developed by **jtechAi Labs (ZuluYokohama)**.

> The rotary dial is IsoZ's mark; the Alpha Rig is its mascot. (IsoZ ships from a repository historically named *RotarySlider*; "ARS" — Autoresearch Superpowers — is its prototype lineage.)

## The thesis: intent ≡ code ≡ value

IsoZ is the honest, minimal, **running** seed of a larger theory — *Geometric Determinism* / the *AxiomZ / Jones Framework* — in which **truth is structural coherence** (a sheaf "Global Section": local views that agree on their overlaps), **value warps the metric**, and a **contradiction is an obstruction that halts**. The theory and the roadmap from the current seed toward the full geometric model live in:

- [`docs/theory/GEOMETRIC_DETERMINISM.md`](docs/theory/GEOMETRIC_DETERMINISM.md) — the synthesis (3 decks → one framework).
- [`docs/theory/TRUTH_RESOLVER_ROADMAP.md`](docs/theory/TRUTH_RESOLVER_ROADMAP.md) — v1 (shipped) → v2 sheaf coherence → v3 commit-vs-resolve.

**Honesty split:** the *theory decks are the vision*; the *code is the current seed*. Anything not yet in code (ATFT, the Ternary-Crystal hardware substrate, sheaf-v2) is labeled **roadmap**, never capability. Today, `truth_resolver` is a 187-line deterministic gate that scores intent/context/value overlap; that is the real, shipped state.

## What's IsoZ-original vs inherited

**Inherited (credit where due):**
- **Superpowers** — the composable skills + agent methodology (brainstorming, TDD, planning, subagent-driven development, code review) by Jesse Vincent. Install and use it per its own project; the `skills/` library here is that layer.
- **autoresearch** — Karpathy's training/research code (`train.py`, `prepare.py`) rides along.

**IsoZ-original:**
- **The Feature Studio** — `ui/studio` (Next.js + R3F: a glowing rotary dial, intent-pulse interactions, camera parallax), `ui/telemetry` (Svelte), and `scripts/api_server.py` (FastAPI).
- **The gate framework** — `scripts/`: a quality gate (Flake8 / Bandit security-lint / Radon), a weak-crypto denylist lint, an AST complexity oracle, a failure cache, and a demonstration evolution loop.
- **`truth_resolver`** — the deterministic `intent ≡ code ≡ value` alignment gate (the thesis in code).

## Run the Feature Studio

```bash
# 1. Backend (FastAPI) — serves /status, /intent, /gallery, /telemetry
python scripts/api_server.py            # http://localhost:8000

# 2. Telemetry panel (SvelteKit)
cd ui/telemetry && npm install && npm run dev   # http://localhost:3001

# 3. Studio (Next.js + R3F)
cd ui/studio && npm install && npm run dev      # http://localhost:3000
```

Prerequisites: Node 18+, Python 3.11+, and (for the gates) `pip install rich fastapi uvicorn flake8 bandit radon`.

## The gates (honest descriptions)

- **Quality gate** (`scripts/aaa_quality.py`) — runs **Flake8** (style), **Bandit** (a security linter for unsafe code patterns — *not* cryptographic verification), and **Radon** (cyclomatic complexity).
- **Weak-crypto denylist lint** (`scripts/quantum_gate.py`) — flags identifiers matching a small weak-crypto blocklist (`md5`, `sha1`, `rsa`, …). It is a denylist lint, *not* post-quantum cryptography.
- **AST oracle** (`scripts/oracle.py`) — detects nested loops and naked recursion, injecting optimization intents.
- **Failure cache** (`scripts/akashic_records.py`) — a SQLite cache that remembers, by content hash, which mutations previously failed.
- **Evolution loop — DEMONSTRATION** (`scripts/recursive_evolution.py`, `evolve.py`) — a `[DEMO]` loop that deterministically tallies features to illustrate the gate flow. It does **not** run a real LLM swarm (clearly labeled in its output).

## CLI

```bash
python scripts/cli.py intent <target> --name "Feature" --metric "O(1)"   # inject an intent vector
python scripts/cli.py status <target>                                     # show the feature map
python scripts/cli.py evolve <target>                                     # run the [DEMO] evolution loop
```

## License

See [LICENSE](LICENSE). The inherited Superpowers and autoresearch layers retain their original authors' licenses and credit.
