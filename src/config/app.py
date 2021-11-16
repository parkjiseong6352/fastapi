import logging.config

from fastapi import FastAPI

from src.api.auth.controllers import router as router_auth
from src.api.sample.controllers import router as router_sample
from src.api.user.controllers import router as router_user
from src.config.connections.database import db
from src.config.loggings import logging_config
from src.config.middlewares.logging import LoggingMiddleware
from src.common.exceptions.exception_handlers import exception_handlers
from src.common.response import APIResponse


def create_app():
    """
    FastAPI Application
    """

    app = FastAPI(
        default_response_class=APIResponse,
        exception_handlers=exception_handlers,
    )

    # Logging
    logging.config.dictConfig(logging_config)

    # Connection
    db.init_app(app)

    # Middlewares
    app.add_middleware(LoggingMiddleware)

    # Routers
    app.include_router(router_auth, prefix="/auth")
    app.include_router(router_sample, prefix="/test")
    app.include_router(router_user, prefix="/user")

    return app
