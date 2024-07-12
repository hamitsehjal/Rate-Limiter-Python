from app.algorithms import (
    RateLimitingAlgorithm,
    TokenBucketAlgorithm,
    FixedWindowCounterAlgorithm,
    SlidingWindowLog,
    SlidingWindowCounter,
)


def rate_limiting_factory(rate_algorithm: str) -> RateLimitingAlgorithm:
    match rate_algorithm:
        case "token_bucket":
            return TokenBucketAlgorithm()
        case "fixed_window_counter":
            return FixedWindowCounterAlgorithm()
        case "sliding_window_log":
            return SlidingWindowLog()
        case "sliding_window_counter":
            return SlidingWindowCounter()
