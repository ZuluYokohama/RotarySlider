#!/usr/bin/env python3
"""
AAA Quality V&V (Verification & Validation)
Enforces industry-standard code quality, security, and complexity metrics.
Acts as a pre-gate before the Evolution Gate is even allowed to run.
"""

import sys
import os
import subprocess
import json

def run_command(cmd, cwd):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def check_flake8(target_dir):
    print("[AAA] Running Flake8 (PEP8 Compliance)...")
    # E501 = Line too long (we'll ignore for this strict test to avoid failing on standard generated code)
    code, stdout, _ = run_command("flake8 --ignore=E501 .", target_dir)
    if code != 0:
        print("[AAA FAILED] Flake8 violations detected:")
        print(stdout)
        return False
    print("[AAA PASSED] Flake8")
    return True

def check_bandit(target_dir):
    print("[AAA] Running Bandit (Security Vulnerabilities)...")
    # Bandit checks for hardcoded passwords, unsafe execs, etc.
    code, stdout, _ = run_command("bandit -r -q .", target_dir)
    if code != 0:
        print("[AAA FAILED] Bandit security vulnerabilities detected:")
        print(stdout)
        return False
    print("[AAA PASSED] Bandit Security")
    return True

def check_radon(target_dir):
    print("[AAA] Running Radon (Cyclomatic Complexity)...")
    # Fail if any function has a complexity score of 'C' or worse (score > 10)
    code, stdout, stderr = run_command("radon cc -nc .", target_dir)
    
    # radon cc -nc prints nothing if everything is A or B. 
    # If it prints anything, it means a function is too complex.
    if stdout.strip():
        print("[AAA FAILED] Radon Cyclomatic Complexity violation. Function is too complex:")
        print(stdout)
        return False
    print("[AAA PASSED] Radon Complexity (All functions <= B)")
    return True

def run_aaa_suite(target_dir):
    print(f"\n=== Booting AAA Quality V&V Suite on {target_dir} ===")
    
    checks = [
        check_flake8,
        check_bandit,
        check_radon
    ]
    
    for check in checks:
        if not check(target_dir):
            print("\n[GATE BLOCKED] AAA Quality standards not met. Swarm mutation purged.")
            sys.exit(1)
            
    print("\n[GATE PASSED] AAA Quality standards met. Code is pristine and secure.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./aaa_quality.py <target_project_directory>")
        sys.exit(1)
    run_aaa_suite(os.path.abspath(sys.argv[1]))
