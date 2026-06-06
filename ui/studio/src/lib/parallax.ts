// Pure parallax helpers. Frame-rate-independent exponential damping so motion is
// identical at 30 or 144 fps. No three/react imports -> testable in plain node.
export interface Vec2 {
  x: number;
  y: number;
}

export function computeParallaxTarget(pointer: Vec2, intensity: number): Vec2 {
  return { x: pointer.x * intensity, y: pointer.y * intensity };
}

export function damp(current: number, target: number, lambda: number, dt: number): number {
  return current + (target - current) * (1 - Math.exp(-lambda * dt));
}
