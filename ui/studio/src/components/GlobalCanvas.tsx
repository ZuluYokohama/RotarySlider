"use client";

import { Canvas } from '@react-three/fiber';
import { Suspense } from 'react';
import { MatrixScene } from './MatrixScene';
import { Preload } from '@react-three/drei';

export function GlobalCanvas() {
  return (
    <Canvas 
      camera={{ position: [0, 0, 10], fov: 50 }}
      style={{ pointerEvents: 'auto' }} // Allow 3D interaction
      dpr={[1, 2]} // AAA Practice: Cap device pixel ratio for performance
    >
      <Suspense fallback={null}>
        <ambientLight intensity={0.2} />
        <directionalLight position={[10, 10, 5]} intensity={1} color="#58a6ff" />
        <MatrixScene />
        <Preload all />
      </Suspense>
    </Canvas>
  );
}
