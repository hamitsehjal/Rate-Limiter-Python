""" 
- Keep a request counter for the previous and current fixed windows
- Leverage information from the previous fixed window to calculate the available limit at the current timestamp

How do we count the available limit at current timestamp

- number of requests in the current fixed window 
- number of requests in the previous fixed window 
- weight of the previous fixed window 

Weight of previous fixed window =(window_size - time_consumed_from_current_window)/window_size 

limit_available = requests_in_previous_window * weight_previous_window + requests_in_current_window
"""

from .rate_limiting_algorithm import RateLimitingAlgorithm
import time
from asyncio import Lock


class SlidingWindowCounter(RateLimitingAlgorithm):
    def __init__(self, window_size=60, max_requests=60):
        self.lock = Lock()
        self.previous_counter = 0  # number of requests in previous window
        self.current_counter = 0  # number of requests in current window
        self.current_window_started = time.monotonic()
        self.window_size = window_size
        self.max_requests = max_requests

    async def allow_request(self) -> bool:
        async with self.lock:
            curr_time = time.monotonic()
            total_time_elapsed = curr_time - self.current_window_started
            time_elapsed_in_current_window = total_time_elapsed % self.window_size

            # Handle multiple window rollovers
            windows_passed = int(total_time_elapsed / self.window_size)
            if windows_passed > 0:
                self.previous_counter = (
                    self.current_counter if windows_passed == 1 else 0
                )
                self.current_counter = 0

                self.current_window_started = curr_time - time_elapsed_in_current_window

            weight_previous_window = max(
                0,
                (self.window_size - time_elapsed_in_current_window) / self.window_size,
            )

            limit_available = (
                self.previous_counter * weight_previous_window
            ) + self.current_counter

            if limit_available < self.max_requests:
                self.current_counter += 1
                return True
            return False
