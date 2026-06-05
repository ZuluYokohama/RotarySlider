"use client";

import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import * as THREE from 'three';

export function AlphaRig() {
  const group = useRef<THREE.Group>(null);

  // Smooth floating animation for the AI rig
  useFrame((state) => {
    if (group.current) {
      group.current.position.y = Math.sin(state.clock.elapsedTime) * 0.2 - 1;
      group.current.rotation.y = state.clock.elapsedTime * 0.5;
    }
  });

  return (
    <group ref={group} position={[4, -1, -2]}>
      {/* 
        Placeholder geometry for the AI Generated 3D Mesh of Alpha.
        In a live build, use: const { nodes } = useGLTF('/models/alpha_ai_gen.glb')
      */}
      <mesh>
        <octahedronGeometry args={[1.5, 2]} />
        <meshStandardMaterial color="#58a6ff" wireframe />
      </mesh>
      
      {/* Floating UI Label */}
      <Html center position={[0, 2, 0]}>
        <div style={{
          background: 'rgba(13, 17, 23, 0.8)',
          color: '#58a6ff',
          padding: '4px 8px',
          borderRadius: '4px',
          border: '1px solid #30363d',
          fontFamily: 'monospace',
          fontSize: '12px',
          whiteSpace: 'nowrap',
          backdropFilter: 'blur(4px)'
        }}>
          ALPHA_RIG_v1.0 (AI Gen)
        </div>
      </Html>
    </group>
  );
}
