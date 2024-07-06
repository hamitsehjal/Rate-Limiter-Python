from .token_bucket_algorithm import RateLimitingAlgorithm, TokenBucketAlgorithm


def rate_limiting_factory(rate_algorithm: str) -> RateLimitingAlgorithm:
    match algo:
        case "token_bucket_algorithm":
            return TokenBucketAlgorithm()
