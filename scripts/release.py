#!/usr/bin/env python3
import sys
import os
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

if __name__ == "__main__":
    print("Preparing 1.0.0 Release...")
    
    # Check if tree is clean
    status = run_cmd("git status --porcelain")
    if status:
        print("Git tree is not clean. Commit changes first.")
        sys.exit(1)
        
    print("Tagging v1.0.0...")
    run_cmd("git tag -a v1.0.0 -m 'Release 1.0.0 - Autoresearch Superpowers Matrix'")
    
    print("Pushing tags to origin...")
    run_cmd("git push origin v1.0.0")
    
    print("Creating GitHub Release...")
    run_cmd('gh release create v1.0.0 --title "v1.0.0 - The Infinite Matrix" --notes "Initial production release of the Autoresearch Superpowers framework. Features V&V Gating, Hardware Piping, FastMCP integration, and recursive swarm evolution."')
    
    print("Release completed successfully.")
