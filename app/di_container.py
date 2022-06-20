from os import environ
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from redis import Redis

from business.interfaces.rate_limiter_base import Rate
from business.services.redis_cache import RedisService
from business.services.time_bucket_limit import TimeBucketRateLimit


class DIContainer(DeclarativeContainer):
    # Cache setup
    cache_host = environ.get("CACHE_HOST")
    cache_port = environ.get("CACHE_PORT")

    redis_client_factory = providers.Factory(Redis, cache_host, cache_port)
    cache_service_factory = providers.Factory(RedisService, client=redis_client_factory)

    # Rate limiter setup
    client_limit = Rate(requests=5, milliseconds=10000)
    client_limit_object = providers.Object(client_limit)
    rate_limiting_factory = providers.Factory(
        TimeBucketRateLimit,
        cache_service=cache_service_factory,
        default_client_limit=client_limit_object,
    )
