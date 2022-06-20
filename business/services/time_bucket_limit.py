from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from business.interfaces.cache_base import CacheBase
from business.interfaces.rate_limiter_base import Rate, RateLimiterBase, RequestContext
from exceptions.rate_limit import LimitExceededException


@dataclass
class TimeBucketContext(RequestContext):
    client: str


class TimeBucketRateLimit(RateLimiterBase):
    def __init__(
        self,
        cache_service: CacheBase,
        default_client_limit: Rate,
        key_prefix: str = "rate_limit_",
    ):
        self.cache_service = cache_service
        self.default_client_limit = default_client_limit
        self.key_prefix = key_prefix

    async def can_request(self, context: TimeBucketContext) -> bool:
        client_key: str = f"{self.key_prefix}{context.client}"

        # TODO Turn to bytes on set_response_callback
        current_requests_bytes: Optional[bytes] = self.cache_service.get(client_key)
        current_requests: Optional[int] = (
            int(current_requests_bytes) if current_requests_bytes else None
        )
        if current_requests is not None and current_requests <= 0:
            return False

        return True

    async def request(self, context: TimeBucketContext):
        client_key: str = f"{self.key_prefix}{context.client}"
        if not await self.can_request(context):
            expiry_time: datetime = self.cache_service.expiry_time(client_key)
            raise LimitExceededException(next_allowed=expiry_time)

        # TODO Turn to bytes on set_response_callback
        current_requests_bytes: Optional[bytes] = self.cache_service.get(client_key)
        current_requests: Optional[int] = (
            int(current_requests_bytes) if current_requests_bytes else None
        )
        if current_requests is None:
            client_limit: Rate = self.default_client_limit
            current_requests = client_limit.requests
            self.cache_service.set(
                client_key,
                current_requests,
                expires_in_ms=client_limit.milliseconds,
            )

        new_requests: int = current_requests - 1
        try:
            self.cache_service.set(client_key, new_requests, keep_ttl=True)
        finally:
            ...
