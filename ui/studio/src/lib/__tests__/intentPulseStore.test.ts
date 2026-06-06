import { describe, it, expect, beforeEach } from 'vitest';
import {
  emitIntentPulse,
  getIntentPulse,
  subscribeIntentPulse,
  __resetIntentPulseStore,
} from '../intentPulseStore';

describe('intentPulseStore', () => {
  beforeEach(() => __resetIntentPulseStore());

  it('starts empty', () => {
    expect(getIntentPulse()).toBeNull();
  });

  it('emits a pulse with a monotonically increasing id', () => {
    const a = emitIntentPulse('Cyberpunk Button', 'O(1)', 1000);
    const b = emitIntentPulse('Neon Slider', 'Contrast 4.5:1', 2000);
    expect(a.id).toBe(1);
    expect(b.id).toBe(2);
    expect(getIntentPulse()).toEqual(b);
    expect(b).toEqual({ id: 2, name: 'Neon Slider', metric: 'Contrast 4.5:1', at: 2000 });
  });

  it('notifies subscribers on emit and stops after unsubscribe', () => {
    let calls = 0;
    const unsub = subscribeIntentPulse(() => { calls += 1; });
    emitIntentPulse('A', 'm', 1);
    emitIntentPulse('B', 'm', 2);
    expect(calls).toBe(2);
    unsub();
    emitIntentPulse('C', 'm', 3);
    expect(calls).toBe(2);
  });
});
