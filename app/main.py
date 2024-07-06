from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# from threading import Lock
from asyncio import Lock
from app.rate_limiter import RateLimiter, RateLimitingFactory
from app.logger import logger

app = FastAPI()

ip_to_locks = {}  # mapping ip_address to Lock
ip_to_rate_limiter = {}  # mapping ip address to instance of Rate Limiter
ip_locks_creation_lock = Lock()


@app.get("/")
async def root():
    return {"message": "Rate Limiter Design System"}


@app.get("/unlimited")
async def unlimited():
    return {"message": "Unlimited! Let's Go!"}


@app.get("/limited")
async def limited(request: Request, algo=None):
    # get the client's ip address
    ip_address = request.client.host
    logger.debug(f"IP Address = {ip_address}")

    async with ip_locks_creation_lock:
        if ip_address not in ip_to_locks:
            ip_to_locks[ip_address] = Lock()

    async with ip_to_locks[ip_address]:
        if ip_address not in ip_to_rate_limiter:
            # instantiate a Rate Limiting Algorithm based on query parameter
            rate_limiting_algorithm = RateLimitingFactory(rate_algorithm=algo)

            # instantiate a Rate Limiter an create an entry in hashmap
            ip_to_rate_limiter[ip_address] = RateLimiter(
                chosen_algorithm=rate_limiting_algorithm
            )

    if not ip_to_rate_limiter[ip_address].allow_request():
        # Decline request
        return JSONResponse(
            content="Rate Limited Exceed: Too many Requests!", status_code=429
        )

    return JSONResponse(content="This API offers limited Use!!")
