import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from hardware_piping import HardwarePipingManager

class TestHardwarePipingManager(unittest.TestCase):
    def test_lease_and_release(self):
        manager = HardwarePipingManager(max_cpu=4)
        self.assertTrue(manager.request_lease(2))
        self.assertFalse(manager.request_lease(3))
        manager.release_lease(2)
        self.assertTrue(manager.request_lease(3))

    def test_garbage_collection(self):
        manager = HardwarePipingManager()
        # Ensure it doesn't crash and returns an int
        reclaimed = manager.collect_garbage()
        self.assertIsInstance(reclaimed, int)

    def test_vram_flush(self):
        manager = HardwarePipingManager()
        # Should gracefully return boolean without crashing even if PyTorch isn't present
        success = manager.flush_vram()
        self.assertIsInstance(success, bool)

if __name__ == '__main__':
    unittest.main()
