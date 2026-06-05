"use client";

import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { AlphaRig } from './AlphaRig';
import { TelemetryMonitor } from './TelemetryMonitor';

export function MatrixScene() {
  const coreRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (coreRef.current) {
      coreRef.current.rotation.x += delta * 0.2;
      coreRef.current.rotation.y += delta * 0.3;
    }
  });

  return (
    <group>
      {/* The Central Rotary Matrix Core */}
      <mesh ref={coreRef} position={[0, 0, -5]}>
        <torusKnotGeometry args={[3, 0.5, 128, 32]} />
        <meshStandardMaterial color="#3fb950" wireframe opacity={0.3} transparent />
      </mesh>

      {/* Embedded Svelte Telemetry (Phase 3) */}
      <TelemetryMonitor />

      {/* AI Generated Dog Rig */}
      <AlphaRig />
    </group>
  );
}
