# RotarySlider 3D Frontend (R3F) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Tasks and steps use checkbox (`- [ ]`) syntax for tracking.

## AAA Best Practices Applied
- **Single WebGL Context**: We will use a global `<Canvas>` wrapped around the Next.js `layout.tsx` to prevent WebGL context loss and frame drops during navigation.
- **View Tunneling**: Using `@react-three/drei`'s `<View>` or `tunnel-rat` to seamlessly mix DOM and WebGL space without layout thrashing.
- **Hardware Opti**: R3F components will be lazy-loaded, wrapped in `<Suspense>`, and we will aggressively cull invisible objects to adhere to our `HardwarePipingManager` ethos.

## Phase 1: Global Canvas & AAA Infrastructure
- [ ] **Step 1:** Configure Tailwind CSS (`tailwind.config.js` and `postcss.config.js`) for rapid DOM overlay styling.
- [ ] **Step 2:** Refactor `ui/studio/src/app/layout.tsx` to mount a persistent, full-screen `@react-three/fiber` `<Canvas>` behind all children.
- [ ] **Step 3:** Implement an event tunnel or global state manager to allow DOM inputs (like the Intent Form) to trigger 3D animations.
- [ ] **Step 4:** Add a global `<Suspense>` fallback (a cyber-loader) to mask 3D asset initialization.

## Phase 2: The Core Matrix (3D Background)
- [ ] **Step 1:** Create `src/components/canvas/MatrixScene.tsx`.
- [ ] **Step 2:** Add ambient lighting, fog, and a dark, moody camera setup.
- [ ] **Step 3:** Build a rotating particle field or central glowing "Rotary Slider" dial using instanced meshes for O(1) rendering performance.
- [ ] **Step 4:** Hook mouse coordinates to camera parallax using `framer-motion-3d` for buttery smooth AAA interaction.

## Phase 3: Spatial Telemetry Embedding
- [ ] **Step 1:** Create a 3D primitive (e.g., a floating terminal screen) in the `MatrixScene`.
- [ ] **Step 2:** Use `@react-three/drei`'s `<Html transform>` to embed the SvelteKit iframe (`http://localhost:3001`) onto the face of the 3D terminal.
- [ ] **Step 3:** Ensure the embedded `<Html>` respects occlusion (hides when rotated behind other 3D objects) to maintain immersion.

## Phase 4: Intent Nodes & Visual Gallery Textures
- [ ] **Step 1:** Refactor the `IntentForm` to spawn a visual 3D sphere/node in the Matrix for every active intent returned by the FastAPI backend.
- [ ] **Step 2:** Refactor the `VisualGallery` into a 3D carousel. Map the screenshots returned by the Playwright Visual V&V loop as `MeshBasicMaterial` textures onto floating 3D planes.
- [ ] **Step 3:** Hook `onClick` raycasting events to the 3D planes to zoom the camera in for detailed UX inspection.
