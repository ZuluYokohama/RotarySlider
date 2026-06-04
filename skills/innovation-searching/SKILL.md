---
name: innovation-searching
description: Use when tasked with improving, evolving, or finding novel solutions to an existing codebase. Triggers V&V and Evolution Gating logic.
---

# Innovation Searching & Evolution Gating

Use this skill when the user asks to evolve a project, find better approaches, or run autonomous research on a codebase.

## 1. Baseline Establishment (V&V)
Before proposing any changes, you must establish the baseline:
- Run existing tests.
- Note key performance metrics (if available).
- Document the current architectural constraints.

## 2. Innovation Search Phase
Generate at least three (3) distinct paths for improvement. These could be:
- Algorithmic optimization.
- Architectural refactoring.
- Integration of a new, highly-relevant external library or methodology.

## 3. Implementation (Worktrees)
Use the `using-git-worktrees` skill to implement each of the three paths in isolated branches.

## 4. Evolution Gating
For each proposed innovation, apply the Evolution Gate:
- Does it pass the baseline V&V?
- Does it introduce new capabilities?
- Are the new capabilities fully tested (TDD)?
- Does it reduce complexity or significantly improve performance?

**If an innovation fails the gate, discard it.**

## 5. Selection & Handoff
Select the winning innovation that passed the gate. Present a summary of why it won compared to the baseline and the discarded options. Use `finishing-a-development-branch` to finalize the work.

