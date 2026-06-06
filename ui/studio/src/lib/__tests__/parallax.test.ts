import { describe, it, expect } from 'vitest';
import { computeParallaxTarget, damp } from '../parallax';

describe('computeParallaxTarget', () => {
  it('scales normalized pointer by intensity', () => {
    expect(computeParallaxTarget({ x: 1, y: -1 }, 2)).toEqual({ x: 2, y: -2 });
    expect(computeParallaxTarget({ x: 0, y: 0 }, 5)).toEqual({ x: 0, y: 0 });
  });
});

describe('damp', () => {
  it('returns the current value when dt is 0', () => {
    expect(damp(3, 10, 5, 0)).toBeCloseTo(3, 6);
  });

  it('moves toward the target and never overshoots for positive lambda/dt', () => {
    const next = damp(0, 10, 5, 0.016);
    expect(next).toBeGreaterThan(0);
    expect(next).toBeLessThan(10);
  });

  it('approaches the target as dt grows large', () => {
    expect(damp(0, 10, 5, 100)).toBeCloseTo(10, 5);
  });

  it('does not overshoot a negative target', () => {
    expect(damp(0, -10, 5, 100)).toBeGreaterThanOrEqual(-10);
    const step = damp(0, -10, 5, 0.016);
    expect(step).toBeLessThan(0);
    expect(step).toBeGreaterThan(-10);
  });

  it('is frame-rate independent (one dt step == two dt/2 steps)', () => {
    const oneBig = damp(0, 10, 5, 1 / 30);
    const twoSmall = damp(damp(0, 10, 5, 1 / 60), 10, 5, 1 / 60);
    expect(twoSmall).toBeCloseTo(oneBig, 6);
  });
});
