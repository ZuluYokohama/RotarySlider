#!/usr/bin/env python3
"""
The Akashic Records (Evolutionary Memory)
An SQLite-backed memory store that records the DNA (SHA-256 hash) of every failed mutation,
along with the exact AAA/SLA failure reason. 
This prevents the infinite recursive swarm from attempting the same flawed logic twice.
"""

import sqlite3
import hashlib
import os
import sys

def get_db_path(target_dir):
    return os.path.join(target_dir, '.akashic.db')

def init_db(target_dir):
    conn = sqlite3.connect(get_db_path(target_dir))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS failed_mutations (
            hash TEXT PRIMARY KEY,
            failure_stage TEXT,
            error_log TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def hash_file_content(filepath):
    """Generates a SHA-256 hash of the file's AST/content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def record_failure(target_dir, filepath, failure_stage, error_log):
    file_hash = hash_file_content(filepath)
    if not file_hash:
        return
        
    init_db(target_dir)
    conn = sqlite3.connect(get_db_path(target_dir))
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO failed_mutations (hash, failure_stage, error_log)
            VALUES (?, ?, ?)
        ''', (file_hash, failure_stage, error_log))
        conn.commit()
        print(f"[AKASHIC] Recorded failed mutation DNA to evolutionary memory. (Stage: {failure_stage})")
    except sqlite3.IntegrityError:
        print("[AKASHIC] FATAL: Swarm attempted a previously failed mutation. The Matrix is looping.")
    finally:
        conn.close()

def check_if_failed_before(target_dir, filepath):
    """Returns the failure reason if this code state has failed before."""
    file_hash = hash_file_content(filepath)
    if not file_hash:
        return None
        
    init_db(target_dir)
    conn = sqlite3.connect(get_db_path(target_dir))
    cursor = conn.cursor()
    cursor.execute('SELECT failure_stage, error_log FROM failed_mutations WHERE hash = ?', (file_hash,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"stage": row[0], "log": row[1]}
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./akashic_records.py <target_dir> <command> [args...]")
        sys.exit(1)
        
    target = os.path.abspath(sys.argv[1])
    cmd = sys.argv[2]
    
    if cmd == "check" and len(sys.argv) == 4:
        res = check_if_failed_before(target, sys.argv[3])
        if res:
            print(f"PREVIOUSLY FAILED at {res['stage']}:\n{res['log']}")
            sys.exit(1)
        else:
            print("CLEAN")
            sys.exit(0)
    elif cmd == "record" and len(sys.argv) == 6:
        record_failure(target, sys.argv[3], sys.argv[4], sys.argv[5])
