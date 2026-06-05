import subprocess
import time
import sys
import os

def run_aaa_gate():
    # Call the RotarySlider AAA suite
    current_dir = os.getcwd()
    aaa_script = os.path.join('${ROTARY_PATH}', 'scripts', 'aaa_quality.py')
    result = subprocess.run(['python3', aaa_script, current_dir], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        return False
    print(result.stdout)
    return True

def run_tests():
    # Attempt to find a standard test runner
    if os.path.exists('pytest.ini') or os.path.exists('tests'):
        result = subprocess.run(['python3', '-m', 'pytest', '-q'], capture_output=True, text=True)
    else:
        # Fallback to discovering unittests
        result = subprocess.run(['python3', '-m', 'unittest', 'discover'], capture_output=True, text=True)
    return result.returncode == 0

if __name__ == '__main__':
    print("[V&V] Initiating AAA Pre-Gate...")
    if not run_aaa_gate():
        sys.exit(1)
        
    print("[V&V] Running baseline tests...")
    if not run_tests():
        print("[GATE FAILED] Correctness check failed. Tests did not pass.")
        sys.exit(1)
    
    print("[GATE PASSED] Innovation meets all V&V criteria.")
    sys.exit(0)
