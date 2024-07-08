from app.algorithms import (
    RateLimitingAlgorithm,
    TokenBucketAlgorithm,
    FixedWindowCounterAlgorithm,
)


def rate_limiting_factory(rate_algorithm: str) -> RateLimitingAlgorithm:
    match rate_algorithm:
        case "token_bucket":
            return TokenBucketAlgorithm()
        case "fixed_window_counter":
            return FixedWindowCounterAlgorithm()
