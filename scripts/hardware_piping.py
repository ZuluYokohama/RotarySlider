import os
import threading

class HardwarePipingManager:
    """
    Manages resource leasing (CPU, RAM, VRAM) for the recursive evolution matrix
    to prevent OOM errors and CPU throttling during parallel swarm execution.
    """
    def __init__(self, max_cpu=None):
        self.max_cpu = max_cpu or os.cpu_count() or 1
        self.allocated_cpu = 0
        self.lock = threading.Lock()

    def request_lease(self, cpu_req=1) -> bool:
        """Attempt to lease hardware resources for an agent."""
        with self.lock:
            if self.allocated_cpu + cpu_req <= self.max_cpu:
                self.allocated_cpu += cpu_req
                return True
            return False

    def release_lease(self, cpu_req=1):
        """Release hardware resources back to the pool."""
        with self.lock:
            self.allocated_cpu = max(0, self.allocated_cpu - cpu_req)
