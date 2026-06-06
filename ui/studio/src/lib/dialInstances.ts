// Pure geometry for the instanced rotary dial. No three/react imports so it runs
// in plain node under Vitest. The R3F component turns these into instance matrices.
export interface InstanceTransform {
  position: [number, number, number];
  rotationZ: number;
  scale: number;
}

export function computeDialInstances(count: number, radius: number): InstanceTransform[] {
  if (count <= 0) return [];
  const out: InstanceTransform[] = [];
  for (let i = 0; i < count; i += 1) {
    const theta = (i / count) * Math.PI * 2;
    out.push({
      position: [Math.cos(theta) * radius, Math.sin(theta) * radius, 0],
      rotationZ: theta,
      scale: 1,
    });
  }
  return out;
}
