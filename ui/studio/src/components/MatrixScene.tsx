"use client";

import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { AlphaRig } from './AlphaRig';
import { TelemetryMonitor } from './TelemetryMonitor';
import { useIntentPulse } from '../lib/useIntentPulse';
import { RotaryDial } from './RotaryDial';

export function MatrixScene() {
  const coreRef = useRef<THREE.Group>(null);
  const pulse = useIntentPulse();
  const lastPulseId = useRef(0);
  const kick = useRef(0); // decays 1->0, scales the core on each new intent

  useFrame((state, delta) => {
    if (pulse && pulse.id !== lastPulseId.current) {
      lastPulseId.current = pulse.id;
      kick.current = 1;
    }
    kick.current = Math.max(0, kick.current - delta * 1.5);
    // The pop is animated; if the Canvas is ever switched to frameloop="demand",
    // keep requesting frames while the kick decays (no-op under the default "always").
    if (kick.current > 0) state.invalidate();
    if (coreRef.current) {
      coreRef.current.scale.setScalar(1 + kick.current * 0.4);
    }
  });

  return (
    <group>
      {/* The Central Rotary Slider Dial (instanced, O(1)) */}
      <group ref={coreRef} position={[0, 0, -5]}>
        <RotaryDial />
      </group>

      {/* Embedded Svelte Telemetry (Phase 3) */}
      <TelemetryMonitor />

      {/* AI Generated Dog Rig */}
      <AlphaRig />
    </group>
  );
}
