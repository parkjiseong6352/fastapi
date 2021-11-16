import logging

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from src.common.response import APIResponse
from src.common.response.codes import Http4XX, Http5XX
from . import APIException

logger = logging.getLogger(__name__)


async def api_exception_handler(
    request: Request, exc: APIException
) -> APIResponse:
    logger.error(f"APIException - {exc}")
    return APIResponse(exc.error)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> APIResponse:
    logger.error(f"APIException - {exc}")
    return APIResponse(Http4XX.BAE_REQUEST, data=exc.errors())


async def default_exception_handler(
    request: Request, exc: Exception
) -> APIResponse:
    logger.error(f"APIException - {exc}")
    return APIResponse(Http5XX.SERVER_ERROR, data=exc.args[0])


exception_handlers = {
    APIException: api_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    Exception: default_exception_handler,
}
