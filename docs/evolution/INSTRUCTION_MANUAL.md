# Autoresearch Superpowers: Evolution & Innovation Manual

Welcome to the autonomous V&V and Evolution framework for Autoresearch Superpowers. This system combines the rigorous agentic workflows of Superpowers with the research-driven exploration capabilities of Autoresearch.

## 1. System Overview
The goal of this system is to enable agents to not just write code, but to **research, validate, evolve, and innovate** software solutions automatically.

### Key Components
- **Verification & Validation (V&V) Engine:** Enforces strict compliance checks before any code is merged or considered "complete". It builds on `systematic-debugging` and `test-driven-development`.
- **Evolution Gating Logic:** A mechanism that prevents regression. New iterations of a solution must provably outperform or cleanly extend the capabilities of the previous version.
- **Innovation Searching:** A continuous background or active loop where the agent explores alternative architectures, algorithms, or external repositories to find novel approaches to the current problem.

## 2. Standalone Remote Repo Integration
The system is designed to operate as a standalone plugin that can interact with remote repositories (like GitHub/GitLab). 

### Workflow
1. **Fetch/Clone:** The agent fetches a remote repository.
2. **Analyze & Baseline:** The V&V engine establishes a baseline of current tests, performance metrics, and static analysis.
3. **Innovation Search:** The agent looks for "innovations" (e.g., modernizing dependencies, algorithmic improvements, architectural refactors).
4. **Implement & Test:** The agent applies the innovation in a separate worktree.
5. **Evolution Gate:** The proposed changes are run against the V&V engine. If the new version passes all existing tests AND improves metrics (or adds new verified capabilities), the gate opens.
6. **Deploy/Merge:** The agent pushes the changes or submits a PR automatically.

## 3. Using the Innovation Skill
To activate this workflow, the agent will use a new skill: `innovation-searching`.

When active, the agent will:
- Identify the core problem.
- Propose at least 3 distinct innovative approaches.
- Run them through the Evolution Gate.
- Select the winner based on V&V results.

## 4. Gating Criteria
- **Correctness:** 100% pass rate on existing test suites.
- **Performance:** No degradation in execution time or memory footprint beyond a 5% margin, unless justified by a massive capability increase.
- **Novelty:** The solution must introduce a measurable improvement (cleaner code, faster execution, fewer dependencies).

