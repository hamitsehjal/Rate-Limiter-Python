from fastapi import FastAPI, HTTPException, Request
from bucket import Bucket, refill_thread
import threading

app = FastAPI()

ip_to_bucket = {}
ip_to_bucket_lock = threading.Lock()


@app.get("/")
async def root():
    return {"message": "Rate Limiter Design System"}


@app.get("/unlimited")
async def unlimited():
    return {"message": "Unlimited! Let's Go!"}


@app.get("/limited")
async def limited(request: Request):
    # Get the IP Address
    ip = request.client.host

    # Thread-safe Bucket creation and retrieval
    with ip_to_bucket_lock:
        # check if there is existing bucket for IP Address
        # if no, create a new Bucket
        if ip in ip_to_bucket:
            # get the bucket
            bucket = ip_to_bucket.get(ip)
        else:
            # create a new Bucket object
            bucket = Bucket()
            # add entry to hashmap
            ip_to_bucket[ip] = bucket

    # Atomic Operation to check and remove token
    if not bucket.try_remove_token():
        raise HTTPException(
            status_code=429, detail="Too many requests! I'm Limited, don't over use me!"
        )

    return {"message": "Request Completed"}


if __name__ == "__main__":
    import uvicorn

    refill_thread()
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Bucket Class
""" 
- private 
  - attribute (deque)
  - MAX_CAPACITY

- check bucket size
- add token to bucket 
- remove token from the bucket 
- return MAX_CAPACITY
"""

"""
  
def refill_buckets():
  while true:
    - for ip,bucket in ip_to_bucket.items():
      - if bucket.size() < MAX_CAPACITY:
        - bucket.add(token)
    - time.sleep(1)

Approach - 1 (Multi-threading)
How are we refilling the buckets ??
- Directly adds one token per iteration of the refill_buckets loop.

DRAWBACK: 
Currently we are expecting that all the token count of all the buckets in the hashmap (refill_buckets method) will be done withing 1 second. This could be true when hashmap is of smaller size, but with increased system load or other factors, the refill_buckets method might not run exactly every second 

TRADE-OFFS:
- Less precise if the refill_buckets function doesn't run exactly every second.
- Doesn't accommodate variable refill rates without modification.
- Won't "catch up" if the refill function is delayed for some reason.

Why global thread??
- prevent race conditions
- multiple requests from same IP. We might end up creating multiple same IP's
"""
