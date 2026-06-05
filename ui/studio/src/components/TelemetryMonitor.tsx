"use client";

import { Html } from '@react-three/drei';
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export function TelemetryMonitor() {
  const meshRef = useRef<THREE.Mesh>(null);

  // Subtle hover effect to make it feel physically present
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1 + 1;
    }
  });

  return (
    <mesh ref={meshRef} position={[-4, 1, -1]} rotation={[0, Math.PI / 6, 0]}>
      <boxGeometry args={[4.2, 3.2, 0.1]} />
      <meshStandardMaterial color="#0d1117" roughness={0.2} metalness={0.8} />
      
      {/* The iframe is physically embedded on the 3D mesh via Html transform */}
      <Html transform position={[0, 0, 0.06]} scale={0.1}>
        <div style={{ width: '400px', height: '300px', background: '#0d1117', border: '2px solid #3fb950', borderRadius: '4px', overflow: 'hidden' }}>
          <iframe 
            src="http://localhost:3001" 
            style={{ width: '100%', height: '100%', border: 'none' }}
            title="Spatial Telemetry Engine"
          />
        </div>
      </Html>
    </mesh>
  );
}
