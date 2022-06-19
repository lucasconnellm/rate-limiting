from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Rate:
    requests: int
    milliseconds: int


@dataclass
class RequestContext:
    ...


class RateLimiterBase(ABC):
    @abstractmethod
    async def can_request(self, context: RequestContext) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def request(self, context: RequestContext):
        raise NotImplementedError
