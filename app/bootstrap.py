from fastapi import FastAPI

from app.di_container import DIContainer
from app.middleware import rate_limit_middleware
from app.routes import root


class Bootstrap:
    @classmethod
    def create_app(cls) -> FastAPI:
        app: FastAPI = FastAPI()

        # Instantiate dependency injection container
        container = DIContainer()
        container.init_resources()
        container.wire(
            modules=[
                root,
                rate_limit_middleware,
            ]
        )

        # Wire up middleware
        app.middleware("http")(rate_limit_middleware.throttle)

        # Wire up routes
        app.include_router(root.root_router)

        return app
