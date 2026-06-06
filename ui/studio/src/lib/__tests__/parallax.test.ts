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
});
