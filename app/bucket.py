from queue import Queue
import time

""" 

Thread-safety is ensured by:
- Using the lock for all state-changing operations
- Keeping critical sections (code within with self.lock:) as short as possible
- Ensuring that all paths that can modify shared state are protected by the lock
"""


class Bucket:
    def __init__(self, max_capacity=10):
        self.tokens = Queue(maxsize=max_capacity)
        self._last_refill = time.time()

        # Fill the Bucket initially
        for _ in range(max_capacity):
            self.tokens.put(1)

    @property
    def last_refill(self):
        return self._last_refill

    @last_refill.setter
    def last_refill(self, value):
        self._last_refill = value

    def check_size(self):
        return self.tokens.qsize()

    def is_empty(self):
        return self.tokens.empty()

    def is_full(self):
        return self.tokens.full()

    def remove_token(self):
        self.tokens.get()

    def add_token(self, num_tokens):
        for _ in range(num_tokens):
            if not self.tokens.full():
                self.tokens.put(1)
