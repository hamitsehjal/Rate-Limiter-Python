from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.refill import lock, ip_to_bucket, refill_thread
from app.logger import logger


app = FastAPI()

refill_thread.start()


@app.get("/")
async def root():
    return {"message": "Rate Limiter Design System"}


@app.get("/unlimited")
async def unlimited():
    return {"message": "Unlimited! Let's Go!"}


@app.get("/limited")
async def limited(request: Request):
    ip_address = request.client.host
    logger.debug(f"IP Address = {ip_address}")
    with lock:
        bucket = ip_to_bucket[ip_address]
        logger.debug(f"Item in Buckets - {bucket.check_size()}")
        if bucket.is_empty():
            return JSONResponse(
                content="Rate limit exceeded: Too many Requests", status_code=429
            )
        bucket.remove_token()
        return JSONResponse(content="Request processed")


"""
Approach - 1 (Multi-threading)
How are we refilling the buckets ??
- Directly adds one token per iteration of the refill_buckets loop.

DRAWBACK: 
Currently we are expecting that all the token count of all the buckets in the hashmap (refill_buckets method) will be done withing 1 second. This could be true when hashmap is of smaller size, but with increased system load or other factors, the refill_buckets method might not run exactly every second 

TRADE-OFFS:
- Less precise if the refill_buckets function doesn't run exactly every second.
- Doesn't accommodate variable refill rates without modification.
- Won't "catch up" if the refill function is delayed for some reason.

"""
