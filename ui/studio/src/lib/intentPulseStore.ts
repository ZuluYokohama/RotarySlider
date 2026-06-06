// Framework-agnostic external store for "intent pulses". Pure and synchronous so it
// can be unit-tested in plain node, then bridged into React via useSyncExternalStore.
export type PulseListener = () => void;

export interface IntentPulse {
  id: number;
  name: string;
  metric: string;
  at: number; // epoch ms, supplied by caller (keeps the store deterministic/testable)
}

let current: IntentPulse | null = null;
let count = 0;
const listeners = new Set<PulseListener>();

export function emitIntentPulse(name: string, metric: string, at: number): IntentPulse {
  count += 1;
  current = { id: count, name, metric, at };
  listeners.forEach((listener) => listener());
  return current;
}

export function getIntentPulse(): IntentPulse | null {
  return current;
}

export function subscribeIntentPulse(listener: PulseListener): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

// Test-only helper.
export function __resetIntentPulseStore(): void {
  current = null;
  count = 0;
  listeners.clear();
}
