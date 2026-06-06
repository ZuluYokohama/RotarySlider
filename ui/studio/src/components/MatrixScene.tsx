"use client";

import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { AlphaRig } from './AlphaRig';
import { TelemetryMonitor } from './TelemetryMonitor';
import { useIntentPulse } from '../lib/useIntentPulse';

export function MatrixScene() {
  const coreRef = useRef<THREE.Mesh>(null);
  const pulse = useIntentPulse();
  const lastPulseId = useRef(0);
  const kick = useRef(0); // decays 1->0, scales the core on each new intent

  useFrame((state, delta) => {
    if (pulse && pulse.id !== lastPulseId.current) {
      lastPulseId.current = pulse.id;
      kick.current = 1;
    }
    kick.current = Math.max(0, kick.current - delta * 1.5);
    if (coreRef.current) {
      coreRef.current.rotation.x += delta * 0.2;
      coreRef.current.rotation.y += delta * 0.3;
      const s = 1 + kick.current * 0.4; // visible pop on new intent
      coreRef.current.scale.setScalar(s);
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
