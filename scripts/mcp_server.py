#!/usr/bin/env python3
import sys
import os
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rotary-slider-matrix")

@mcp.tool()
def inject_intent(target_dir: str, feature_name: str, metric_sla: str) -> str:
    """Injects a new intent vector into the target project's feature map."""
    cli_path = os.path.join(os.path.dirname(__file__), 'cli.py')
    result = subprocess.run([sys.executable, cli_path, 'intent', target_dir, '--name', feature_name, '--metric', metric_sla], capture_output=True, text=True)
    return result.stdout

@mcp.tool()
def evaluate_gate(target_dir: str) -> str:
    """Manually evaluates a target project against its Evolution Gate."""
    cli_path = os.path.join(os.path.dirname(__file__), 'cli.py')
    result = subprocess.run([sys.executable, cli_path, 'gate', target_dir], capture_output=True, text=True)
    return result.stdout

@mcp.tool()
def read_status(target_dir: str) -> str:
    """Reads the current tally state of intent vectors for a target project."""
    cli_path = os.path.join(os.path.dirname(__file__), 'cli.py')
    result = subprocess.run([sys.executable, cli_path, 'status', target_dir], capture_output=True, text=True)
    return result.stdout

@mcp.tool()
def trigger_oracle(target_dir: str) -> str:
    """Invokes the AST Oracle to autonomously scan the codebase for bottlenecks and inject intents."""
    oracle_path = os.path.join(os.path.dirname(__file__), 'oracle.py')
    result = subprocess.run([sys.executable, oracle_path, target_dir], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    print("Starting RotarySlider MCP Server...")
    mcp.run(transport='stdio')

@mcp.tool()
def trigger_quantum_scan(target_dir: str) -> str:
    """Invokes the Quantum Gate to scan the codebase for pre-quantum cryptographic vulnerabilities (RSA, MD5)."""
    quantum_path = os.path.join(os.path.dirname(__file__), 'quantum_gate.py')
    result = subprocess.run([sys.executable, quantum_path, target_dir], capture_output=True, text=True)
    return result.stdout

@mcp.tool()
def push_yolo_button(target_dir: str) -> str:
    """Unleashes the Chaos Monkey, injecting extremely restrictive, chaotic intents into the matrix."""
    chaos_path = os.path.join(os.path.dirname(__file__), 'chaos_monkey.py')
    result = subprocess.run([sys.executable, chaos_path, target_dir], capture_output=True, text=True)
    return result.stdout
