# RotarySlider Feature Studio Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Tasks and steps use checkbox (`- [ ]`) syntax for tracking.

## Phase 1: Python Backend & Playwright Integration (The Visual Matrix)
- [ ] **Step 1:** Add FastAPI and Playwright dependencies to `pyproject.toml`.
- [ ] **Step 2:** Create `scripts/visual_matrix.py` to handle headless component rendering and screenshot generation.
- [ ] **Step 3:** Update `evolution_gate.py` to optionally invoke `visual_matrix.py` if a visual intent is detected in the `feature_map.json`.
- [ ] **Step 4:** Create `scripts/api_server.py` using FastAPI to expose REST/WebSocket endpoints wrapping the CLI logic.

## Phase 2: The SvelteKit Telemetry Engine
- [x] **Step 1:** Initialize a SvelteKit project in `ui/telemetry`.
- [x] **Step 2:** Implement a WebSocket client store to connect to the FastAPI backend.
- [x] **Step 3:** Build reactive UI components for Hardware Leases, Epoch loops, and the Tally Matrix.
- [ ] **Step 4:** Build the SvelteKit project into static assets suitable for embedding.

## Phase 3: The Next.js Feature Studio Shell
- [x] **Step 1:** Initialize a Next.js project in `ui/studio`.
- [x] **Step 2:** Build the layout shell (Sidebar, Header, Main Content Area).
- [x] **Step 3:** Embed the compiled SvelteKit Telemetry Engine into the main dashboard view.
- [ ] **Step 4:** Build an Intent Injection form that posts to the FastAPI REST endpoints.
- [ ] **Step 5:** Build a Visual Gallery page to display screenshots and Vision Model grades from the Evolution Gate.
