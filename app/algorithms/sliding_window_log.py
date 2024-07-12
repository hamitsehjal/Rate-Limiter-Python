from collections import deque
from asyncio import Lock
from time import time, ctime
from app.logger import logger
from .rate_limiting_algorithm import RateLimitingAlgorithm


class SlidingWindowLog(RateLimitingAlgorithm):
    def __init__(self, window_size=10, limit=30):
        self.logs = deque()
        self.lock = Lock()
        self.window_size = window_size
        self.max_requests = limit

    def remove_outdated_entries(self, key):
        while True:
            if self.logs and self.logs[0] <= key:
                self.logs.popleft()
            else:
                return

    async def allow_request(self) -> bool:
        async with self.lock:
            curr_time = time()
            start_time_curr_window = curr_time - self.window_size
            logger.info(
                f"Start Time of Current Window: {ctime(start_time_curr_window)}"
            )
            if self.logs:
                self.remove_outdated_entries(key=start_time_curr_window)

            self.logs.append(curr_time)
            logger.debug(f"Size of Logs Collection: {len(self.logs)}")
            if len(self.logs) > self.max_requests:
                return False
            return True
