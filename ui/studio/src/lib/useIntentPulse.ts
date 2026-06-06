"use client";

import { useSyncExternalStore } from 'react';
import { getIntentPulse, subscribeIntentPulse, type IntentPulse } from './intentPulseStore';

export function useIntentPulse(): IntentPulse | null {
  return useSyncExternalStore(
    subscribeIntentPulse,
    getIntentPulse,
    () => null, // server snapshot
  );
}
