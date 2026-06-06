#!/usr/bin/env python3
"""
Recursive Evolution Loop with Hardware Piping (DEMONSTRATION)

DEMO: this loops over feature_map.json and, each epoch, deterministically marks
one pending feature as 'tallied' until all are tallied. It does NOT run a real
LLM swarm or mutate code; trigger_evolution_gate() invokes the evolve.py stub.
The HardwarePipingManager leasing/GC is real; the "evolution" is simulated.
"""

import os
import sys
import json
import time
import subprocess
from hardware_piping import HardwarePipingManager

def load_checklist(target_dir):
    path = os.path.join(target_dir, 'feature_map.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return json.load(f)

def save_checklist(target_dir, data):
    path = os.path.join(target_dir, 'feature_map.json')
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def is_perfect(checklist):
    return all(item['status'] == 'tallied' for item in checklist['features'])

def trigger_evolution_gate(target_dir, hw_manager):
    print(f"  [HARDWARE] Requesting compute lease...")
    if hw_manager.request_lease(cpu_req=1):
        try:
            print(f"  [GATE][DEMO] Lease granted. Running the evolve.py stub (no real swarm)...")
            hw_manager.flush_vram() # VRAM time-slicing prep
            subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'evolve.py'), target_dir], capture_output=True)
        finally:
            hw_manager.flush_vram() # VRAM time-slicing cleanup
            print(f"  [HARDWARE] Releasing compute lease...")
            hw_manager.release_lease(cpu_req=1)
    else:
        print(f"  [HARDWARE][DEMO] Lease denied (System fully utilized). Simulated mutation queued for next cycle.")

def infinite_evolution_loop(target_dir):
    epoch = 0
    print("[INIT][DEMO] Booting the Evolution Matrix demonstration loop (deterministic tally; no real LLM swarm)...")
    hw_manager = HardwarePipingManager()
    print(f"[INIT] HardwarePipingManager active. Max bounded CPU units: {hw_manager.max_cpu}")
    
    while True:
        epoch += 1
        print(f"\n=== [EPOCH {epoch}] ===")
        
        checklist = load_checklist(target_dir)
        if not checklist:
            print("[FATAL] feature_map.json missing. Cannot derive perfection state. Halting.")
            sys.exit(1)
            
        if is_perfect(checklist):
            print("[PERFECT] Derived checklist is fully tallied. All features mapped and gated.")
            print("[TERMINATE][DEMO] Demonstration loop complete — all features tallied (no real MaxVal optimization performed).")
            break
            
        print("[STATE] Sub-optimal state detected. Deriving pending intents:")
        pending_features = [f for f in checklist['features'] if f['status'] != 'tallied']
        
        for feat in pending_features:
            print(f"  -> Intent Vector: {feat['intent']} | Feature: {feat['name']}")
                
        # Trigger the gated evolution with hardware manager constraint
        trigger_evolution_gate(target_dir, hw_manager)
        
        # Simulate Swarm Success for the demonstration
        for feat in checklist['features']:
            if feat['status'] != 'tallied':
                feat['status'] = 'tallied'
                print(f"  [MAXVAL][DEMO] Simulated success: feature '{feat['name']}' marked 'tallied' (no real evolution performed).")
                break
                
        save_checklist(target_dir, checklist)
        
        # GC Aggression (as defined in HARDWARE_OPTIMIZATION_SCOPE.md)
        reclaimed = hw_manager.collect_garbage()
        print(f"  [HARDWARE] Epoch GC completed. Objects reclaimed: {reclaimed}")
        
        time.sleep(1) # Recursive buffer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./recursive_evolution.py <target_project_directory>")
        sys.exit(1)
    infinite_evolution_loop(os.path.abspath(sys.argv[1]))
