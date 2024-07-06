from abc import ABC, abstractmethod


class RateLimitingAlgorithm(ABC):
    """Base class for Rate Limiting Algorithm"""

    @abstractmethod
    def allow_request(self):
        pass
