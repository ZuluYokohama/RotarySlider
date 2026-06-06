import { describe, it, expect } from 'vitest';
import { computeDialInstances } from '../dialInstances';

describe('computeDialInstances', () => {
  it('returns an empty array for non-positive counts', () => {
    expect(computeDialInstances(0, 3)).toEqual([]);
    expect(computeDialInstances(-5, 3)).toEqual([]);
  });

  it('produces `count` evenly-spaced ticks around a ring of the given radius', () => {
    const ticks = computeDialInstances(4, 2);
    expect(ticks).toHaveLength(4);
    expect(ticks[0].position[0]).toBeCloseTo(2, 5);
    expect(ticks[0].position[1]).toBeCloseTo(0, 5);
    expect(ticks[0].rotationZ).toBeCloseTo(0, 5);
    expect(ticks[1].position[0]).toBeCloseTo(0, 5);
    expect(ticks[1].position[1]).toBeCloseTo(2, 5);
    expect(ticks[1].rotationZ).toBeCloseTo(Math.PI / 2, 5);
  });

  it('keeps every tick on the ring (radius invariant)', () => {
    for (const t of computeDialInstances(16, 3)) {
      const r = Math.hypot(t.position[0], t.position[1]);
      expect(r).toBeCloseTo(3, 5);
    }
  });

  it('places the final tick without duplicating theta=2pi (uses i/count, not i/(count-1))', () => {
    const ticks = computeDialInstances(4, 2);
    expect(ticks[3].position[0]).toBeCloseTo(0, 5);
    expect(ticks[3].position[1]).toBeCloseTo(-2, 5);
    expect(ticks[3].rotationZ).toBeCloseTo((3 * Math.PI) / 2, 5);
  });

  it('handles count = 1 (single tick on the +X axis)', () => {
    const ticks = computeDialInstances(1, 3);
    expect(ticks).toHaveLength(1);
    expect(ticks[0].position[0]).toBeCloseTo(3, 5);
    expect(ticks[0].position[1]).toBeCloseTo(0, 5);
    expect(ticks[0].rotationZ).toBeCloseTo(0, 5);
  });
});
