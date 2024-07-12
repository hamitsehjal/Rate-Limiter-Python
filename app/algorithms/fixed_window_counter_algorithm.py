"""
Window Size: 1 minute(60 seconds)
Limit(threshold): 60 requests 

Start time of current window 
Hashmap: start time of window --> counter

Algorithm Design

Request comes in:
- Get the current timestamp
- Calculate the start-timestamp of the current window
- Using hashmap that maps "start-timestamp" ---> "counter", we check if the counter exists
    - If yes, we extract counter for the current window
    - else, we create a new instance of the counter

- increment the counter 
- check if counter < limit
    - if true, allow the request
    - if false, deny the request

1. The expression (currentTimestamp % windowSizeInMillis) gives you the offset from the last window start.

2. Subtracting this offset from the current timestamp effectively "rounds down" to the start of the current window.

Cleaning Old-entries:
1. Periodic Cleanup
2. Lazy expiration


Two Different Approaches
1. Background Process for Resetting 
    Pros:
        1. Simple to understand and implement 
        2. Consistent time windows 
        3. Low overhead per request 

    Cons: 
        1. Consumes resources even when there are no requests 
        2. Potential for race conditions if not implemented carefully
        3. Doesn't scale well for Distributed Environments 

2. On-Demand Calculation
    Pros: 
        1. uses resources only when needed
        2. Can easily adapt to Distributed Systems
    
    Cons:
        1. Slightly higher overhead per request 
        2. Required careful handling of time calculations


    Implementation - 1:
    - maintain a reference of window_start_time (initially set to curr time in seconds)
    - For every request, find the difference btw curr_time - window_start_time 
    - if that diff >= WINDOW_SIZE:
        - reset the counter
        - update the window_start_time 

    Implementation - 2:
    - Use a Hashmap(window_start_timestamp) --> Counter 
    - clean up old entries 
        - in each request or,
        - periodically
    
    
"""

from .rate_limiting_algorithm import RateLimitingAlgorithm
import time
from asyncio import Lock


class FixedWindowCounterAlgorithm(RateLimitingAlgorithm):
    def __init__(self, WINDOW_SIZE=60, WINDOW_LIMIT=60):
        self.counter = 0
        self.WINDOW_SIZE = WINDOW_SIZE
        self.window_start_time = time.time()
        self.LIMIT = WINDOW_LIMIT
        self.lock = Lock()

    async def allow_request(self) -> bool:
        async with self.lock:
            curr_time = time.time()
            if curr_time - self.window_start_time >= self.WINDOW_SIZE:
                # window expired, reset it
                self.counter = 0
                self.window_start_time = curr_time

            if self.counter >= self.LIMIT:
                return False
            self.counter += 1
            return True
