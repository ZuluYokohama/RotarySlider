"use client";

import { useLayoutEffect, useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { computeDialInstances } from '../lib/dialInstances';

const TICK_COUNT = 48;
const RADIUS = 3;
const HUB_SEGMENTS = 48;

export function RotaryDial() {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const groupRef = useRef<THREE.Group>(null);
  const transforms = useMemo(() => computeDialInstances(TICK_COUNT, RADIUS), []);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  // O(1) per-frame cost: instance matrices are set once; only the group rotates.
  useLayoutEffect(() => {
    if (!meshRef.current) return;
    transforms.forEach((t, i) => {
      dummy.position.set(t.position[0], t.position[1], t.position[2]);
      dummy.rotation.set(0, 0, t.rotationZ);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, [transforms, dummy]);

  useFrame((_, delta) => {
    if (groupRef.current) groupRef.current.rotation.z -= delta * 0.15;
  });

  return (
    <group ref={groupRef}>
      <instancedMesh ref={meshRef} args={[undefined, undefined, TICK_COUNT]}>
        <boxGeometry args={[0.12, 0.5, 0.12]} />
        {/* toneMapped={false} keeps the emissive glow at full brightness — deliberate, since the pipeline has no bloom/postprocessing. */}
        <meshStandardMaterial
          color="#3fb950"
          emissive="#3fb950"
          emissiveIntensity={1.4}
          toneMapped={false}
        />
      </instancedMesh>
      {/* glowing hub */}
      <mesh>
        <circleGeometry args={[0.6, HUB_SEGMENTS]} />
        <meshStandardMaterial color="#58a6ff" emissive="#58a6ff" emissiveIntensity={1.2} toneMapped={false} />
      </mesh>
    </group>
  );
}
