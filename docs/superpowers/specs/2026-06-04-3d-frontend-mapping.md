# RotarySlider 3D Frontend Mapping (via react-three-next)

## Inspiration Context
Target Vibe: [Yuta Abe's Portfolio](https://yutaabe.com/about/)
Base Architecture: [react-three-next](https://github.com/pmndrs/react-three-next)

Yuta's site heavily utilizes React Three Fiber (R3F) for smooth, WebGL-driven 3D background elements, physics, floating UI, and seamless page transitions. This perfectly matches the "Matrix" aesthetic of RotarySlider.

## Comprehensive Mapping to RotarySlider Needs

### 1. The Shell (Next.js App Router + R3F Canvas)
- **Current State:** Basic 2D Next.js layout.
- **R3F Upgrade:** We wrap the entire application in a persistent WebGL `<Canvas>`. The Next.js pages act as overlays (using `@react-three/drei`'s `<Html>` component) or drive state changes that manipulate the 3D scene underneath.
- **Visuals:** A dark, cyberpunk 3D particle field or a literal "Rotary Slider" (a glowing 3D dial) sitting in the background.

### 2. Intent Injection Form
- **Current State:** HTML `<form>`.
- **R3F Upgrade:** The intent vectors are visualized as 3D nodes floating around a central core (The Matrix). When a user submits a new intent, a new 3D node physically animates into existence in the WebGL scene.

### 3. Visual V&V Gallery
- **Current State:** 2D CSS grid of screenshots.
- **R3F Upgrade:** An interactive 3D carousel. Screenshots captured by Playwright are loaded as textures onto floating 3D planes. Users can physically drag/rotate the gallery in 3D space to inspect the failed/passed UX components.

### 4. SvelteKit Telemetry Engine
- **Current State:** 2D `<iframe>` in a CSS grid.
- **R3F Upgrade:** We use Drei's `<Html transform>` to embed the blazing-fast Svelte telemetry iframe directly onto the face of a 3D monitor object within the WebGL scene. It remains ultra-fast but exists in 3D space.

## Required Dependencies (Injected)
- `three`: Core WebGL library.
- `@react-three/fiber`: React reconciler for Three.js.
- `@react-three/drei`: Helpers for R3F (crucial for `<Html>` embedding).
- `framer-motion`: For smooth, industrial-grade layout animations.
- `tailwindcss`: For rapid DOM overlay styling.
