from app.algorithms import RateLimitingAlgorithm, TokenBucketAlgorithm


def rate_limiting_factory(rate_algorithm: str) -> RateLimitingAlgorithm:
    match rate_algorithm:
        case "token_bucket_algorithm":
            return TokenBucketAlgorithm()
