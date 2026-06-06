# RotarySlider 3D Frontend (R3F) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Tasks and steps use checkbox (`- [ ]`) syntax for tracking.

> **Reconciliation (2026-06-06):** This plan was executed and verified in a finishing pass; checkboxes below now reflect merged reality (`intent ≡ code`).
> - **C4 prerequisite (PR #17):** an audit found the studio did not build (malformed `<section>` in `page.tsx`, missing TypeScript deps, Tailwind v4 dep against a v3 config) and the persistent `<Canvas>` was occluded by an opaque page background. All fixed before any 3D work.
> - **Phase 1·Step 3 → C1 (PR #18):** intent-pulse external store + `useSyncExternalStore` hook + `router.refresh()`.
> - **Phase 2·Step 1 path drift:** the file is `src/components/MatrixScene.tsx`, not `src/components/canvas/MatrixScene.tsx` — no `canvas/` subdirectory exists.
> - **Phase 2·Step 3 → C2 (PR #20)** and **Phase 2·Step 4 → C3 (PR #21).**
> - **Phase 4 overclaim — checkboxes corrected to `[ ]` below:** Steps 1–3 were marked done but describe 3D-mesh implementations (a sphere per intent, a 3D screenshot carousel, raycasting zoom) that were **never built**. The actual `IntentForm`/`VisualGallery` are DOM components (`ClientViews.tsx`); C1 connected the DOM form to the scene via the intent pulse, but the literal 3D-mesh forms remain unimplemented.

## AAA Best Practices Applied
- **Single WebGL Context**: We will use a global `<Canvas>` wrapped around the Next.js `layout.tsx` to prevent WebGL context loss and frame drops during navigation.
- **View Tunneling**: Using `@react-three/drei`'s `<View>` or `tunnel-rat` to seamlessly mix DOM and WebGL space without layout thrashing.
- **Hardware Opti**: R3F components will be lazy-loaded, wrapped in `<Suspense>`, and we will aggressively cull invisible objects to adhere to our `HardwarePipingManager` ethos.

## Phase 1: Global Canvas & AAA Infrastructure
- [x] **Step 1:** Configure Tailwind CSS (`tailwind.config.js` and `postcss.config.js`) for rapid DOM overlay styling.
- [x] **Step 2:** Refactor `ui/studio/src/app/layout.tsx` to mount a persistent, full-screen `@react-three/fiber` `<Canvas>` behind all children.
- [x] **Step 3:** Implement an event tunnel or global state manager to allow DOM inputs (like the Intent Form) to trigger 3D animations. *(C1, PR #18: intent-pulse store + `useSyncExternalStore` + `router.refresh()`.)*
- [x] **Step 4:** Add a global `<Suspense>` fallback (a cyber-loader) to mask 3D asset initialization.

## Phase 2: The Core Matrix (3D Background)
- [x] **Step 1:** Create `src/components/MatrixScene.tsx`. *(Path corrected from `canvas/MatrixScene.tsx`; no `canvas/` subdir exists.)*
- [x] **Step 2:** Add ambient lighting, fog, and a dark, moody camera setup.
- [x] **Step 3:** Build a rotating particle field or central glowing "Rotary Slider" dial using instanced meshes for O(1) rendering performance. *(C2, PR #20: 48-tick instanced dial + glowing hub.)*
- [x] **Step 4:** Hook mouse coordinates to camera parallax for buttery smooth AAA interaction. *(C3, PR #21: dependency-free `useFrame` damp — `framer-motion-3d` not used: not installed/unmaintained.)*

## Phase 3: Spatial Telemetry Embedding
- [x] **Step 1:** Create a 3D primitive (e.g., a floating terminal screen) in the `MatrixScene`.
- [x] **Step 2:** Use `@react-three/drei`'s `<Html transform>` to embed the SvelteKit iframe (`http://localhost:3001`) onto the face of the 3D terminal.
- [x] **Step 3:** Ensure the embedded `<Html>` respects occlusion (hides when rotated behind other 3D objects) to maintain immersion.

## Phase 4: Intent Nodes & Visual Gallery Textures
- [ ] **Step 1:** Refactor the `IntentForm` (Abstracted via UI mesh) to spawn a visual 3D sphere/node in the Matrix for every active intent returned by the FastAPI backend. *(NOT as written: `IntentForm` is a DOM form in `ClientViews.tsx`, not a 3D sphere-spawning mesh. C1 connected the DOM form to the scene via the intent pulse, but the per-intent 3D node was never built.)*
- [ ] **Step 2:** Refactor the `VisualGallery` (Abstracted via UI mesh) into a 3D carousel. Map the screenshots returned by the Playwright Visual V&V loop as `MeshBasicMaterial` textures onto floating 3D planes. *(NOT as written: `VisualGallery` is a DOM grid in `ClientViews.tsx`, not a 3D carousel of textured planes.)*
- [ ] **Step 3:** Hook `onClick` raycasting events to the 3D planes to zoom the camera in for detailed UX inspection. *(NOT implemented: no raycasting/camera-zoom; no 3D gallery planes exist.)*
