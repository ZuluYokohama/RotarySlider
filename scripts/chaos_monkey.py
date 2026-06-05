#!/usr/bin/env python3
"""
The YOLO Chaos Monkey
Randomly injects extreme, highly-restrictive SLA constraints into the feature_map.json
to stress-test the infinite recursive swarm's ability to evolve solutions under pressure.
"""

import sys
import os
import json
import random

CHAOS_INTENTS = [
    {"name": "Zero Allocation Routing", "intent": "O(1) memory overhead. Strict 0 bytes allocated during request phase."},
    {"name": "Clock-Cycle Pinning", "intent": "Execution variance < 10 nanoseconds."},
    {"name": "SIMD Vectorization", "intent": "Force CPU loop vectorization using AVX-512 instructions where applicable."},
    {"name": "Self-Modifying Hotpath", "intent": "JIT compile the critical path at runtime for 3x throughput."},
    {"name": "Zero-Dependency Core", "intent": "Rewrite module to remove all standard library imports except `sys`."}
]

def unleash_chaos(target_dir):
    print(f"\n[YOLO] Unleashing Chaos Monkey on {target_dir}...")
    
    map_path = os.path.join(target_dir, 'feature_map.json')
    data = {"features": []}
    if os.path.exists(map_path):
        with open(map_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    # Pick a random chaotic intent
    chaos = random.choice(CHAOS_INTENTS)
    
    # Check if it's already there
    existing_features = {f['name'] for f in data.get('features', [])}
    if chaos['name'] in existing_features:
        print(f"[YOLO] Chaos intent '{chaos['name']}' is already torturing the swarm.")
        return

    data['features'].append({
        "name": f"[CHAOS] {chaos['name']}",
        "intent": chaos['intent'],
        "status": "pending"
    })
    
    with open(map_path, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"[YOLO] INJECTED: {chaos['name']}")
    print(f"       Constraint: {chaos['intent']}")
    print(f"[YOLO] May the Swarm survive the evolution.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./chaos_monkey.py <target_project_directory>")
        sys.exit(1)
    unleash_chaos(os.path.abspath(sys.argv[1]))
