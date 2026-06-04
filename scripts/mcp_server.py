#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RotarySlider")

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

if __name__ == "__main__":
    print("Starting MCP Server...")
    mcp.run(transport='stdio')
