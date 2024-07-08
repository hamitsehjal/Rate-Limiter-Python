from abc import ABC, abstractmethod


class RateLimitingAlgorithm(ABC):
    """Base class for Rate Limiting Algorithm"""

    @abstractmethod
    async def allow_request(self) -> bool:
        pass
