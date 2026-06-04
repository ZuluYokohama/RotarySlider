#!/usr/bin/env python3
"""
Autoresearch Superpowers CLI with Rich TUI
Command-line interface for managing maxval vectors, evolution gates, and swarm recursion.
"""

import argparse
import os
import sys
import json
import subprocess
import time

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Please install 'rich' to use this CLI: pip install rich")
    sys.exit(1)

console = Console()

def get_target(target_path):
    return os.path.abspath(target_path)

def cmd_evolve(args):
    target = get_target(args.target)
    script = os.path.join(os.path.dirname(__file__), 'recursive_evolution.py')
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Booting Infinite Recursive Matrix for {target}...", total=None)
        # Execute the recursive script, streaming output
        subprocess.run([sys.executable, script, target])

def cmd_gate(args):
    target = get_target(args.target)
    gate_script = os.path.join(target, 'evolution_gate.py')
    if not os.path.exists(gate_script):
        console.print(f"[bold red]FATAL:[/bold red] No evolution_gate.py found in {target}.")
        sys.exit(1)
    
    console.print(Panel(f"[bold cyan]Triggering Evolution Gate[/bold cyan]\nTarget: {target}"))
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
        
    table = Table(title="Intent Injected Successfully")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Feature", args.name)
    table.add_row("Metric", args.metric)
    table.add_row("Status", "[yellow]PENDING[/yellow]")
    console.print(table)

def cmd_status(args):
    target = get_target(args.target)
    map_path = os.path.join(target, 'feature_map.json')
    if not os.path.exists(map_path):
        console.print(f"[yellow]No feature_map.json found in {target}[/yellow]")
        sys.exit(0)
        
    with open(map_path, 'r') as f:
        data = json.load(f)
        
    table = Table(title=f"MaxVal Intent Vectors ({os.path.basename(target)})", show_header=True, header_style="bold magenta")
    table.add_column("Status")
    table.add_column("Feature")
    table.add_column("Intent Metric")
    
    for feat in data.get('features', []):
        if feat['status'] == 'tallied':
            status = "[bold green]🟢 TALLIED[/bold green]"
        else:
            status = "[bold red]🔴 PENDING[/bold red]"
        
        table.add_row(status, feat['name'], feat['intent'])
        
    console.print(table)

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
