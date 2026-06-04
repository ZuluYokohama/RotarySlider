---
name: maxval-effect-intent
description: The ultimate meta-skill. Enforces the alignment of Intent (what), Effect (impact), and Maxval (optimal output) across all agent actions.
---

# MaxVal Effect Intent Vectors

Use this skill when initializing an autonomous swarm or when evaluating the terminal outcome of a complex development loop.

## 1. Intent Vector (The 'What')
Every action must have a precise mathematical or logical objective. 
- **Query:** What is the precise constraint we are solving?
- **Action:** Define the exact SLA, performance metric, or correctness proof required. (e.g., `evolution_gate.py`).

## 2. Effect Vector (The 'Impact')
No code is written without a measurable effect.
- **Query:** How will this change alter the system state?
- **Action:** Run the parallel swarm (`subagent-driven-development`). Generate multiple hypothesis branches.

## 3. MaxVal Vector (The 'Optimal')
We do not accept "better"; we demand the local or global maximum value (MaxVal).
- **Query:** Which effect vector produces the highest yield against the intent vector?
- **Action:** Route all hypothesis branches through the Evolution Gate. The branch with the highest delta between Baseline and Effect is merged. All others are purged.

## Execution
When executing the MaxVal loop:
1. `baseline_intent()`
2. `apply_maxval_vector()`
3. `finalize_effect()`
