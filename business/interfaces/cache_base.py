from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional


class CacheBase(ABC):
    @abstractmethod
    def set(
        self,
        k: str,
        v: Any,
        expires_in_ms: Optional[int] = None,
        keep_ttl: bool = False,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def get(self, k: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def ttl(self, k: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def time(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def expiry_time(self, k: str) -> datetime:
        raise NotImplementedError
