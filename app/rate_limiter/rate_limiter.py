from .rate_limiting_algorithm import RateLimitingAlgorithm


class RateLimiter:
    def __init__(self, chosen_algorithm: RateLimitingAlgorithm):
        self.algorithm = chosen_algorithm

    def set_rate_limiting_algorithm(self, rate_limit_algo: RateLimitingAlgorithm):
        self.algorithm = rate_limit_algo

    def allow_request() -> bool:
        return self.algorithm.allow_request()
