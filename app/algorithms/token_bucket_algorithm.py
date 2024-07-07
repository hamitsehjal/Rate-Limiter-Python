from queue import Queue
from time import time
from .rate_limiting_algorithm import RateLimitingAlgorithm
from asyncio import Lock
from app.logger import logger


class TokenBucketAlgorithm(RateLimitingAlgorithm):
    def __init__(self, capacity=10):
        self.max_capacity = capacity
        self.bucket = Queue(maxsize=capacity)

        for _ in range(self.max_capacity):
            self.bucket.put(1)

        self.refill_rate = 1  # in seconds
        self.refill_amount = 1
        self._last_updated = time()
        self.lock = Lock()

    @property
    def last_updated(self):
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated = value

    def check_size(self):
        return self.bucket.qsize()

    def is_bucket_full(self):
        return self.bucket.full()

    def is_bucket_empty(self):
        return self.bucket.empty()

    def remove_token_from_bucket(self):
        self.bucket.get()

    async def allow_request(self):
        """
        check if the incoming request is allowed or not

        update the token count
        if the bucket is empty, request is declined, return False
        else, remove 1 token and return True
        """
        async with self.lock:
            curr_time = time()
            elapsed_time_since_last_refill = curr_time - self.last_updated
            tokens_to_be_added = (
                int(elapsed_time_since_last_refill / self.refill_rate)
                * self.refill_amount
            )

            for _ in range(tokens_to_be_added):
                if not self.is_bucket_full():
                    self.bucket.put(1)

            self.last_updated = curr_time

            if self.is_bucket_empty():
                return False

            self.remove_token_from_bucket()
            return True
