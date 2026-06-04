#!/usr/bin/env python3
"""
Autoresearch Superpowers CLI
Command-line interface for managing maxval vectors, evolution gates, and swarm recursion.
"""

import argparse
import os
import sys
import json
import subprocess

def get_target(target_path):
    return os.path.abspath(target_path)

def cmd_evolve(args):
    target = get_target(args.target)
    script = os.path.join(os.path.dirname(__file__), 'recursive_evolution.py')
    subprocess.run([sys.executable, script, target])

def cmd_gate(args):
    target = get_target(args.target)
    gate_script = os.path.join(target, 'evolution_gate.py')
    if not os.path.exists(gate_script):
        print(f"[FATAL] No evolution_gate.py found in {target}. Cannot evaluate MaxVal.")
        sys.exit(1)
    
    print(f"[CLI] Triggering Evolution Gate for {target}...\n")
    subprocess.run([sys.executable, gate_script], cwd=target)

def cmd_intent(args):
    target = get_target(args.target)
    map_path = os.path.join(target, 'feature_map.json')
    
    data = {"features": []}
    if os.path.exists(map_path):
        with open(map_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
                
    data["features"].append({
        "name": args.name,
        "intent": args.metric,
        "status": "pending"
    })
    
    with open(map_path, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"[CLI] INTENT INJECTED:")
    print(f"      Feature: {args.name}")
    print(f"      Metric:  {args.metric}")
    print(f"      Status:  PENDING")

def cmd_status(args):
    target = get_target(args.target)
    map_path = os.path.join(target, 'feature_map.json')
    if not os.path.exists(map_path):
        print(f"[CLI] No feature_map.json found in {target}")
        sys.exit(0)
        
    with open(map_path, 'r') as f:
        data = json.load(f)
        
    print(f"\n=== MAXVAL INTENT VECTORS ({target}) ===")
    for feat in data.get('features', []):
        status_color = "🟢" if feat['status'] == 'tallied' else "🔴"
        print(f"{status_color} [{feat['status'].upper()}] {feat['name']} -> {feat['intent']}")
    print("=========================================\n")

def main():
    parser = argparse.ArgumentParser(description="Autoresearch Superpowers - Swarm CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # evolve
    p_evolve = subparsers.add_parser('evolve', help="Boot the infinite recursive evolution matrix")
    p_evolve.add_argument('target', help="Target project directory")
    p_evolve.set_defaults(func=cmd_evolve)

    # gate
    p_gate = subparsers.add_parser('gate', help="Manually evaluate a project against its Evolution Gate")
    p_gate.add_argument('target', help="Target project directory")
    p_gate.set_defaults(func=cmd_gate)

    # intent
    p_intent = subparsers.add_parser('intent', help="Inject a new intent vector into the target's feature map")
    p_intent.add_argument('target', help="Target project directory")
    p_intent.add_argument('--name', required=True, help="Name of the feature or capability")
    p_intent.add_argument('--metric', required=True, help="SLA or target metric (e.g. 'O(1) lookups')")
    p_intent.set_defaults(func=cmd_intent)

    # status
    p_status = subparsers.add_parser('status', help="Check the current tally state of the intent vectors")
    p_status.add_argument('target', help="Target project directory")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
