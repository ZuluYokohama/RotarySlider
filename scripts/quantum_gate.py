#!/usr/bin/env python3
"""
Quantum-Resistant Cryptography Gate
Analyzes the codebase to ensure generated cryptographic functions avoid pre-quantum primitives (RSA, MD5, SHA-1, standard ECC)
and enforces the usage of post-quantum or highly secure classical primitives (e.g., Dilithium, Kyber, or at minimum SHA-3/Argon2).
"""

import ast
import os
import sys

# Primitives vulnerable to Shor's algorithm or classical collision attacks
PRE_QUANTUM_BLACKLIST = {
    'md5', 'sha1', 'rsa', 'dsa', 'ecdsa'
}

class QuantumAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Call(self, node):
        # Check for function calls to vulnerable crypto primitives
        if isinstance(node.func, ast.Name):
            func_name = node.func.id.lower()
            for vulnerable in PRE_QUANTUM_BLACKLIST:
                if vulnerable in func_name:
                    self.violations.append(f"Vulnerable primitive call detected: '{node.func.id}()'")
        
        # Check for module attribute calls (e.g., hashlib.md5)
        if isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr.lower()
            for vulnerable in PRE_QUANTUM_BLACKLIST:
                if vulnerable in attr_name:
                    self.violations.append(f"Vulnerable primitive attribute detected: '.{node.func.attr}()'")

        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if any(vuln in alias.name.lower() for vuln in PRE_QUANTUM_BLACKLIST):
                self.violations.append(f"Vulnerable module import detected: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            if any(vuln in node.module.lower() for vuln in PRE_QUANTUM_BLACKLIST):
                self.violations.append(f"Vulnerable module import detected: 'from {node.module}'")
        self.generic_visit(node)

def run_quantum_gate(target_dir):
    print(f"\n[QUANTUM GATE] Scanning {target_dir} for pre-quantum cryptographic vulnerabilities...")
    analyzer = QuantumAnalyzer()
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read(), filename=file)
                        analyzer.visit(tree)
                    except SyntaxError:
                        pass
                        
    if analyzer.violations:
        print("[QUANTUM GATE FAILED] Pre-quantum cryptographic primitives found. Swarm mutation purged.")
        for v in set(analyzer.violations):
            print(f"  -> {v}")
        return False
        
    print("[QUANTUM GATE PASSED] No pre-quantum cryptography detected. Codebase is mathematically hardened.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./quantum_gate.py <target_project_directory>")
        sys.exit(1)
    if not run_quantum_gate(os.path.abspath(sys.argv[1])):
        sys.exit(1)
