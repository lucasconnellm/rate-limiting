from datetime import datetime
from typing import Any, Dict, Optional

from redis import Redis

from business.interfaces.cache_base import CacheBase


class RedisService(CacheBase):
    def __init__(self, client: Redis):
        self.client = client

    def set(
        self,
        k: str,
        v: Any,
        expires_in_ms: Optional[int] = None,
        keep_ttl: bool = False,
    ) -> bool:
        # TODO use a dataclass if kwargs are gonna be this messy
        kwargs: Dict[str, Any] = {}
        if expires_in_ms:
            kwargs.update(px=expires_in_ms)
        if keep_ttl:
            kwargs.update(keepttl=keep_ttl)
        return bool(self.client.set(k, v, **kwargs))

    def get(self, k: str) -> Any:
        return self.client.get(k)

    def ttl(self, k: str) -> int:
        return self.client.ttl(k)

    def time(self) -> int:
        s, _ = self.client.time()
        return s

    def expiry_time(self, k) -> datetime:
        return datetime.fromtimestamp(self.time() + self.ttl(k))
