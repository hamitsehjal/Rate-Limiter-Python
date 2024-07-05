import threading
import time

""" 

Thread-safety is ensured by:
- Using the lock for all state-changing operations
- Keeping critical sections (code within with self.lock:) as short as possible
- Ensuring that all paths that can modify shared state are protected by the lock
"""


class Bucket:
    MAX_CAPACITY = 4

    def __init__(self):
        self.container = []
        self.lock = threading.Lock()

    def check_bucket_size(self):
        with self.lock:
            return len(self.container)

    def try_remove_token(self):
        with self.lock:
            if self.check_bucket_size() > 0:
                self.container.pop()
                return True
            else:
                return False

    def add_token(self):
        with self.lock:
            if self.check_bucket_size() < MAX_CAPACITY:
                self.container.append("*")


def refill_strategy(bucket_map: dict):
    while True:
        for ip, bucket in bucket_map.items():
            bucket.add_token()
        time.sleep(1)


def refill_thread(hashmap: dict):
    start_refill_thread = threading.Thread(
        target=refill_strategy, bucket_map=hashmap, daemon=True
    )
    start_refill_thread.start()


def get_or_create_bucket(ip: str, ip_to_bucket: dict):

    if ip not in ip_to_bucket:
        # create a new bucket and add entry to hashmap
        ip_to_bucket[ip] = Bucket()
    return ip_to_bucket[ip]
