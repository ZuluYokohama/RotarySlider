# IsoZ Identity Rebrand — Implementation Plan (Cycle 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unify the project's fragmented identity under the honest brand **IsoZ** by rewriting the README around the `intent ≡ code ≡ value` thesis, demoting user-facing overclaim strings, and renaming the GitHub repo — every claim traceable to a realized activity:state (spec §0).

**Architecture:** Pure documentation + identifier changes. No code-symbol/module renames (Cycle 2) and no website (Cycle 3). One worktree → PR → CodeRabbit → merge; the `gh repo rename` is a gated, human-approved admin step performed when no other PRs are open. "Tests" are verification greps (residual-overclaim scans, link/run-instruction presence).

**Tech Stack:** Markdown, JSON, a Python docstring/string edit, `gh`/`git` for the rename. The two theory docs (`docs/theory/GEOMETRIC_DETERMINISM.md`, `TRUTH_RESOLVER_ROADMAP.md`) are already written + committed (e013455) — the README links them; this plan does not re-create them.

---

## File Structure

- **Rewrite:** `README.md` — IsoZ H1, honest "what it is", thesis link, two-layer credit, Feature Studio run docs, demoted gate descriptions.
- **Modify (strings only):** `scripts/cli.py` (3 lines), `.claude-plugin/plugin.json` (name + descriptions), `docs/ISOMORPHISM_MANIFESTO.md` (1 line + a theory pointer), `assets/brand/BRAND_IDENTITY.md` (title + false-capability lines).
- **Admin (gated):** GitHub repo rename `RotarySlider` → `IsoZ` + local remote update.
- **Untouched:** all `scripts/*.py` symbol/module names, `ui/` website, code logic. (Cycles 2/3.)

---

## Task 1: Rewrite the README

**Files:** Rewrite `README.md`

- [ ] **Step 1: Write the new README**

Replace the entire contents of `README.md` with exactly:

```markdown
# IsoZ

**IsoZ** is a *Feature Studio* for agentic development — a Next.js + React-Three-Fiber 3D control surface (with a FastAPI backend and a SvelteKit telemetry panel) over a pluggable framework of verification **gates**. Its thesis is a single idea made runnable: a **deterministic `intent ≡ code ≡ value` alignment gate** (`scripts/truth_resolver.py`). IsoZ is built on the **Superpowers** development methodology and Andrej Karpathy's **autoresearch** training code, and is developed by **jtechAi Labs (ZuluYokohama)**.

> The rotary dial is IsoZ's mark; the Alpha Rig is its mascot. (IsoZ ships from a repository historically named *RotarySlider*.)

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
```

- [ ] **Step 2: Verify the rewrite (residual-overclaim + presence greps)**

Run each; confirm the expected result:
```bash
cd "$(git rev-parse --show-toplevel)"
grep -c "^# IsoZ" README.md                 # expect 1 (H1 is IsoZ)
grep -ci "Quantum-Resistant" README.md      # expect 0
grep -ci "Infinite Recursive LLM Swarm" README.md   # expect 0
grep -ci "cryptographic security checks" README.md  # expect 0
grep -c "truth_resolver" README.md          # expect >=1
grep -c "docs/theory/GEOMETRIC_DETERMINISM.md" README.md   # expect >=1
grep -c "npm run dev" README.md             # expect >=1 (studio documented)
grep -ci "Jesse Vincent\|Superpowers\|Karpathy\|autoresearch" README.md  # expect >=1 (credit kept)
```
Expected: H1=1, overclaims=0, thesis+studio+credit all present.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs(isoz): rewrite README around the intent=code=value thesis (IsoZ)"
```

---

## Task 2: Demote CLI strings (`scripts/cli.py`)

**Files:** Modify `scripts/cli.py` (lines 3, 37, 106 — strings only, no symbol renames)

- [ ] **Step 1: Edit the three strings**

- Line 3 (module docstring): change `Autoresearch Superpowers CLI with Rich TUI` → `IsoZ CLI with Rich TUI`.
- Line 37: change `description=f"Booting Infinite Recursive Matrix for {target}..."` → `description=f"[DEMO] Booting the IsoZ evolution loop for {target}..."`.
- Line 106: change `argparse.ArgumentParser(description="Autoresearch Superpowers - Swarm CLI")` → `argparse.ArgumentParser(description="IsoZ - Feature Studio & Gate CLI")`.

- [ ] **Step 2: Verify (no behavior change; parses + strings updated)**

```bash
python -c "import ast; ast.parse(open('scripts/cli.py').read()); print('PARSE OK')"
grep -ci "Autoresearch Superpowers" scripts/cli.py    # expect 0
grep -ci "Infinite Recursive Matrix" scripts/cli.py   # expect 0
grep -c "IsoZ" scripts/cli.py                          # expect >=2
```
Expected: PARSE OK; old strings gone; IsoZ present. (No argparse subcommand names changed — only description strings.)

- [ ] **Step 3: Commit**

```bash
git add scripts/cli.py
git commit -m "docs(isoz): rebrand CLI banner/strings to IsoZ (no symbol changes)"
```

---

## Task 3: Rebrand the plugin manifest (`.claude-plugin/plugin.json`)

**Files:** Modify `.claude-plugin/plugin.json` (the `name`, top-level `description`, and command `description` strings — NOT command `name` identifiers)

- [ ] **Step 1: Edit the manifest strings**

- `"name": "rotary-slider-matrix"` → `"name": "isoz"`.
- `"description": "Infinite Recursive Swarm Evolution via jtechAi Labs"` → `"description": "IsoZ — a Feature Studio + intent≡code≡value gate framework, by jtechAi Labs"`.
- Command description `"Trigger the AST Oracle to scan for O(N^2) bottlenecks and inject MaxVal intent vectors."` → `"Trigger the AST oracle to scan for O(N^2) bottlenecks and inject value-intent vectors."`
- Command description `"Boot the infinite recursive loop enforcing Flake8, Bandit, Radon, and Visual V&V."` → `"Run the [DEMO] evolution loop with the Flake8/Bandit/Radon quality gate."`
- Leave all command `"name"` identifiers (e.g. `ast-oracle-diagnosis`, `engage-aaa-matrix`) unchanged — identifier renames are Cycle 2.

- [ ] **Step 2: Verify (valid JSON + strings updated)**

```bash
python -c "import json; json.load(open('.claude-plugin/plugin.json')); print('JSON OK')"
grep -ci "rotary-slider-matrix\|Infinite Recursive Swarm\|MaxVal" .claude-plugin/plugin.json  # expect 0
grep -c "isoz\|IsoZ" .claude-plugin/plugin.json   # expect >=2
```
Expected: JSON OK; old identity/overclaim strings gone; IsoZ present.

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "docs(isoz): rebrand plugin manifest description/name to IsoZ"
```

---

## Task 4: Fix the manifesto overclaim + link the honest theory

**Files:** Modify `docs/ISOMORPHISM_MANIFESTO.md` (line 23 + a pointer)

- [ ] **Step 1: Fix the false-capability line + add a theory pointer**

- Change line 23 `- **PR #8 & #11 (AAA & Quantum Gates):** The intent of security maps 1:1 to static AST parsing ops, yielding cryptographic value.` → `- **PR #8 & #11 (quality gate & weak-crypto denylist lint):** the intent of code safety maps 1:1 to static AST parsing ops (a security/complexity lint — not cryptographic verification).`
- Append at the end of the file:
```markdown

---

> **See also:** [`docs/theory/GEOMETRIC_DETERMINISM.md`](theory/GEOMETRIC_DETERMINISM.md) extends this doctrine into the full IsoZ thesis, with an explicit *vision-vs-shipped-seed* honesty split.
```

- [ ] **Step 2: Verify**

```bash
grep -ci "cryptographic value" docs/ISOMORPHISM_MANIFESTO.md   # expect 0
grep -c "theory/GEOMETRIC_DETERMINISM.md" docs/ISOMORPHISM_MANIFESTO.md  # expect 1
```
Expected: overclaim gone; theory linked.

- [ ] **Step 3: Commit**

```bash
git add docs/ISOMORPHISM_MANIFESTO.md
git commit -m "docs(isoz): fix manifesto crypto overclaim; link the honest theory"
```

---

## Task 5: Rebrand the brand-identity doc

**Files:** Modify `assets/brand/BRAND_IDENTITY.md` (title + false-capability lines)

- [ ] **Step 1: Rebrand the title and demote false-capability claims**

- Line 1 `# Surface & Structure UI | RotarySlider Matrix` → `# IsoZ — Brand Identity`.
- Line 5: replace the sentence containing `"quantum gates, and infinite recursive loops bound by AAA industrial parameters"` so the paragraph reads: `The brand identity for **IsoZ** is rooted in the abstraction of raw, algorithmic energy being structurally harnessed — compute cycles bound into verifiable structure. The visual language draws on the rotary dial (the mark) and the Alpha Rig (the mascot).`
- Line 21 (`Concept 2` meaning): change `A nod to the Quantum-Resistant Cryptography gate and the Akashic Evolutionary Memory.` → `A nod to the weak-crypto denylist lint and the failure cache.` Leave the visual descriptions (lattice, glowing node) as design language; only the false-capability nouns change.

- [ ] **Step 2: Verify**

```bash
grep -ci "Quantum-Resistant\|RotarySlider Matrix\|Surface & Structure" assets/brand/BRAND_IDENTITY.md  # expect 0
grep -c "IsoZ" assets/brand/BRAND_IDENTITY.md   # expect >=1
```
Expected: false-capability + old identity gone; IsoZ present.

- [ ] **Step 3: Commit**

```bash
git add assets/brand/BRAND_IDENTITY.md
git commit -m "docs(isoz): rebrand brand-identity doc to IsoZ; demote false-capability nouns"
```

---

## Task 6: Repo rename — GATED human admin step

> **Do NOT run this until: (a) the human partner gives explicit go, AND (b) no other PRs are open/mid-flight** (renaming mid-PR can disrupt refs). This is the one outward-facing, semi-irreversible action in Cycle 1. GitHub auto-redirects old clone/Pages URLs, but external bookmarks may need updating.

- [ ] **Step 1: Confirm preconditions**

```bash
gh pr list -R ZuluYokohama/RotarySlider --state open   # expect: no open PRs (the IsoZ PR itself merged first, OR rename after merge)
```
Recommended sequence: merge the Cycle-1 docs PR FIRST, then rename, to avoid renaming with this PR open.

- [ ] **Step 2: Rename the repo (after explicit human OK)**

```bash
gh repo rename IsoZ -R ZuluYokohama/RotarySlider --yes
```
Expected: repo is now `ZuluYokohama/IsoZ`; GitHub creates redirects from the old name.

- [ ] **Step 3: Update the local remote in the main worktree**

```bash
# Run from inside the main RotarySlider/IsoZ checkout (the released worktree, not this PR's worktree):
git remote set-url origin https://github.com/ZuluYokohama/IsoZ.git
git remote -v   # confirm origin -> .../IsoZ.git
```

- [ ] **Step 4: Verify Pages still serves**

```bash
gh api repos/ZuluYokohama/IsoZ/pages --jq '{url,status}'   # expect status "built"; url is github.io/IsoZ (redirect from /RotarySlider)
```
Expected: Pages still built (URL moves to `/IsoZ`; old URL redirects). The website *content* rebrand is Cycle 3.

---

## PR & Review Ritual (Tasks 1–5 ship as one PR; Task 6 is post-merge admin)

1. Self-review via `superpowers:requesting-code-review`.
2. Fill `.github/PULL_REQUEST_TEMPLATE.md` completely (model/harness/plugins disclosure; problem = fragmented identity + overclaims; core-appropriate = No, fork rebrand; existing-PR search).
3. Show the human partner the complete diff; get explicit approval.
4. Open PR against `master`; wait for CodeRabbit; triage via `superpowers:receiving-code-review` (verify before applying; push back on false findings with evidence).
5. Merge once CodeRabbit is satisfied.
6. THEN perform Task 6 (gated rename) with explicit human go.

---

## Definition of Done

- README rewritten: IsoZ H1, honest "what it is", thesis + theory links with vision/seed split, two-layer credit (upstream credited), Feature Studio run instructions, honest gate descriptions, Bandit correctly labeled.
- CLI banner/strings, plugin manifest description+name, manifesto crypto line, and brand-doc title/claims all say IsoZ and drop false-capability terms; no code symbols/module names changed.
- All verification greps pass; `cli.py` parses; `plugin.json` is valid JSON.
- PR merged to `master`; repo renamed to IsoZ (gated) with redirects verified.
- Every IsoZ assertion traces to a realized activity:state (spec §0); vision-tier labeled roadmap.

---

## Self-Review

**1. Spec coverage:** §1 goal → all tasks; §2 identity model (IsoZ brand, repo rename, dial/Alpha-Rig marks) → Task 1 (marks line) + Task 6 (rename); §3 vocabulary demotions (Cycle-1 docs layer) → Tasks 1–5 (Quantum-Resistant dropped, Akashic→failure cache, Bandit→security linter, MaxVal→value, Infinite-Recursive→[DEMO]); §4 README structure → Task 1 (H1, what-it-is, thesis, two-layer credit, studio docs, honest gates); §5 theory docs → already committed, linked in Task 1/4; §6 scope (no code symbols/website) → enforced (Tasks 2/3 strings-only, command names untouched); §0 invariant (trace to activity:state, vision labeled roadmap) → README thesis section + DoD. All spec sections map to a task. ✅

**2. Placeholder scan:** No TBD/TODO; the full new README content is inline; every edit gives exact old→new strings and a verification command. ✅

**3. Consistency:** "IsoZ" used as the brand uniformly; demotion targets identical across tasks and the spec §3 table (Quantum-Resistant→dropped, Akashic→failure cache, Bandit→security linter, MaxVal→value, Matrix/Infinite→[DEMO]/honest); command/symbol identifiers explicitly deferred to Cycle 2 in both Task 3 and the DoD. ✅
