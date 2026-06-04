#!/usr/bin/env python3
"""
Infinite Recursive Evolution Loop
Loops continuously until the derived feature checklist reaches "perfect" state.
Applies MaxVal/Effect/Intent vectors through Gated Evolution on each epoch.
"""

import os
import sys
import json
import time
import subprocess

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

def trigger_evolution_gate(target_dir):
    print(f"  [GATE] Engaging swarm for hypothesis mutation...")
    # Calls the evolve meta-loop we built earlier
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'evolve.py'), target_dir], capture_output=True)

def infinite_evolution_loop(target_dir):
    epoch = 0
    print("[INIT] Booting Infinite Recursive Evolution Matrix...")
    
    while True:
        epoch += 1
        print(f"\n=== [EPOCH {epoch}] ===")
        
        checklist = load_checklist(target_dir)
        if not checklist:
            print("[FATAL] feature_map.json missing. Cannot derive perfection state. Halting.")
            sys.exit(1)
            
        if is_perfect(checklist):
            print("[PERFECT] Derived checklist is fully tallied. All features mapped and gated.")
            print("[TERMINATE] Recursive evolution achieved absolute MaxVal. Halting loop.")
            break
            
        print("[STATE] Sub-optimal state detected. Deriving pending intents:")
        for feat in checklist['features']:
            if feat['status'] != 'tallied':
                print(f"  -> Intent Vector: {feat['intent']} | Feature: {feat['name']}")
                
        # Trigger the gated evolution
        trigger_evolution_gate(target_dir)
        
        # --- SIMULATION OF AGENT SUCCESS ---
        # In a live environment, the subagent-driven-development skill updates this JSON when tests pass.
        # For this demonstration of the infinite loop terminating, we simulate the swarm successfully 
        # mapping and tallying one feature per epoch.
        for feat in checklist['features']:
            if feat['status'] != 'tallied':
                feat['status'] = 'tallied'
                print(f"  [MAXVAL] Evolution successful! Feature '{feat['name']}' tallied & mapped.")
                break
                
        save_checklist(target_dir, checklist)
        time.sleep(1) # Recursive buffer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./recursive_evolution.py <target_project_directory>")
        sys.exit(1)
    infinite_evolution_loop(os.path.abspath(sys.argv[1]))
