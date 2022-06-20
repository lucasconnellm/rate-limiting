from logging import Logger, getLogger
from typing import Any, Awaitable, Callable, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request, Response
from starlette.datastructures import Address

from app.di_container import DIContainer
from business.interfaces.rate_limiter_base import RateLimiterBase
from business.services.time_bucket_limit import TimeBucketContext
from exceptions.rate_limit import LimitExceededException

logger: Logger = getLogger(__name__)


@inject
async def throttle(
    request: Request,
    call_next: Callable[[Request], Awaitable[Any]],
    rate_limiter: RateLimiterBase = Depends(Provide[DIContainer.rate_limiting_factory]),
) -> Response:
    # TODO use header values to identify IP (or other identifiers for limiting)
    client_address: Optional[Address] = request.client
    client_ip = client_address.host if client_address else "1.2.3.4"

    try:
        context: TimeBucketContext = TimeBucketContext(client=client_ip)
        await rate_limiter.request(context)
        response: Response = await call_next(request)
    except LimitExceededException as lee:
        # TODO clean up
        return Response(
            f"You shall not pass! (until {lee.next_allowed})",
            status_code=429,
            media_type="text/plain",
        )
    except Exception as e:
        # TODO clean up
        logger.exception(str(e))
        return Response(str(e), status_code=500)
    else:
        return response
