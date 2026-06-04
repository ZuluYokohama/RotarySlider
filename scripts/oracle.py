#!/usr/bin/env python3
import ast
import os
import sys
import json

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_For(self, node):
        # Detect nested loops indicating O(N^2) or worse complexity
        for child in ast.walk(node):
            if isinstance(child, ast.For) and child != node:
                if self.current_function:
                    self.issues.append({
                        "feature": f"Optimize {self.current_function}()",
                        "intent": "Reduce O(N^2) nested loop to O(N) or O(1)"
                    })
                break
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detect naked recursion (potential O(2^N) like naive Fibonacci)
        if isinstance(node.func, ast.Name) and node.func.id == self.current_function:
            self.issues.append({
                "feature": f"Memoize {self.current_function}()",
                "intent": "Apply DP/Memoization to naked recursion"
            })
        self.generic_visit(node)

def run_oracle(target_dir):
    print(f"[ORACLE] Scanning Abstract Syntax Trees in {target_dir}...")
    analyzer = ComplexityAnalyzer()
    
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
                        
    if not analyzer.issues:
        print("[ORACLE] Codebase is mathematically pure. No structural bottlenecks detected.")
        return

    # Deduplicate issues
    unique_issues = {f['feature']: f['intent'] for f in analyzer.issues}
    
    # Inject into feature_map.json
    map_path = os.path.join(target_dir, 'feature_map.json')
    data = {"features": []}
    if os.path.exists(map_path):
        with open(map_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    existing_features = {f['name'] for f in data['features']}
    injected_count = 0
    
    for feature, intent in unique_issues.items():
        if feature not in existing_features:
            data['features'].append({
                "name": feature,
                "intent": intent,
                "status": "pending"
            })
            injected_count += 1
            print(f"  -> [INJECTED] {feature}: {intent}")

    if injected_count > 0:
        with open(map_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[ORACLE] Successfully injected {injected_count} new MaxVal intents into the matrix.")
    else:
        print("[ORACLE] Bottlenecks detected, but intents are already tracked in the matrix.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./oracle.py <target_project_directory>")
        sys.exit(1)
    run_oracle(os.path.abspath(sys.argv[1]))
