import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from hardware_piping import HardwarePipingManager

class TestHardwarePipingManager(unittest.TestCase):
    def test_lease_and_release(self):
        # Mock a 4-core system
        manager = HardwarePipingManager(max_cpu=4)
        
        # Lease 2 cores (Success)
        self.assertTrue(manager.request_lease(2), "Should successfully lease 2 cores")
        
        # Attempt to lease 3 more cores (Fail: 2 + 3 > 4)
        self.assertFalse(manager.request_lease(3), "Should fail to lease exceeding cores")
        
        # Release 2 cores
        manager.release_lease(2)
        
        # Attempt to lease 3 cores again (Success: 0 + 3 <= 4)
        self.assertTrue(manager.request_lease(3), "Should successfully lease after releasing")

if __name__ == '__main__':
    unittest.main()
