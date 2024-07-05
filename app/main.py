from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from refill import ip_to_bucket, lock, refill_thread

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rate Limiter Design System"}


@app.get("/unlimited")
async def unlimited():
    return {"message": "Unlimited! Let's Go!"}


@app.get("/limited")
async def limited(request: Request):
    ip_address = request.client.host
    with lock:
        bucket = ip_to_bucket[ip_address]
        if bucket.is_empty():
            return JSONResponse(
                content="Request BLOCKED: Too many Requests", status_code=429
            )
            raise HTTPException(status_code=429, detail="Too many requests!!")
        return JSONResponse(content="Request Passed")


if __name__ == "__main__":
    import uvicorn

    refill_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)


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
