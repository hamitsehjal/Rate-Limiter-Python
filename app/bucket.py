from queue import Queue

""" 

Thread-safety is ensured by:
- Using the lock for all state-changing operations
- Keeping critical sections (code within with self.lock:) as short as possible
- Ensuring that all paths that can modify shared state are protected by the lock
"""


class Bucket:
    def __init__(self, max_capacity=4):
        self.tokens = Queue(maxsize=max_capacity)

        # Fill the Bucket initially
        for _ in range(max_capacity):
            self.tokens.put(1)

    def check_size(self):
        return self.tokens.qsize()

    def is_empty(self):
        return self.tokens.empty()

    def is_full(self):
        return self.tokens.full()

    def remove_token(self):
        self.tokens.get()

    def add_token(self):
        self.tokens.put(1)
