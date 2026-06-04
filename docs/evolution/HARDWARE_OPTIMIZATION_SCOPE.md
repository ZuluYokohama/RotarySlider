# Hardware Optimization & Resource Piping Scope

This document outlines the architectural roadmap for piping and optimizing hardware resources (RAM, CPU, GPU, VRAM) within the `autoresearch-superpowers` matrix. Since the framework runs an infinite recursive swarm (and relies on PyTorch/LLM inference), strict resource management is required to prevent Out-Of-Memory (OOM) errors and CPU throttling.

## 1. VRAM (Video RAM) & GPU Piping
**Current State:** PyTorch defaults to aggressive VRAM allocation. If local LLM agents run concurrently with the Evolution Gate's model tests, VRAM will fragment and OOM.
**Optimization Vectors:**
- **Dynamic Device Mapping:** Implement an intent vector that assigns specific sub-agents to specific GPU UUIDs (`CUDA_VISIBLE_DEVICES`).
- **VRAM Time-Slicing:** The Evolution Gate must flush the CUDA cache (`torch.cuda.empty_cache()`) before and after benchmarking.
- **Mixed Precision Inference:** Enforce FP16/BF16 via intent vectors for all local LLM swarm operations to slash VRAM usage by 50%.
- **KV Cache Quantization:** For long-context research tasks, pipe context through a quantized KV cache.

## 2. RAM (System Memory) Piping
**Current State:** Parallel swarm branches load identical git worktrees into memory simultaneously.
**Optimization Vectors:**
- **Memory-Mapped Data (mmap):** Dataset ingestion for the `autoresearch` models must use zero-copy `mmap` to share RAM across parallel Python processes.
- **Lazy Worktree Loading:** Agents should only load file deltas into RAM, rather than the entire project context.
- **Garbage Collection Aggression:** Force `gc.collect()` at the end of every Evolution Epoch to reclaim memory from discarded sub-optimal branches.

## 3. CPU & Multiprocessing Piping
**Current State:** The recursive matrix `evolve.py` is largely sequential or relies on unmanaged OS subprocessing.
**Optimization Vectors:**
- **Ray / Process Pools:** Pipe the "Swarm Mutation" phase through a strictly bounded CPU process pool (e.g., max workers = `os.cpu_count() - 2`) to leave headroom for OS stability.
- **Thread Pinning:** Use `taskset` or PyTorch thread pinning to prevent context-switching overhead when running CPU-bound V&V tests.
- **Async I/O:** All Git operations, API calls to external LLMs, and filesystem writes should be ported to `asyncio` to unblock the main execution thread.

## 4. Implementation Strategy (The Piping Architecture)
To implement this, we will introduce a `HardwarePipingManager` class to the framework. 
Whenever `scripts/recursive_evolution.py` triggers an epoch, it requests a "Resource Lease" (e.g., 2 CPU cores, 4GB RAM, 8GB VRAM) for each agent or test. If the lease exceeds physical limits, the matrix queues the mutation instead of crashing.
