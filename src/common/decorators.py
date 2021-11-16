from functools import wraps
from inspect import iscoroutinefunction
import logging

from src.common.exceptions import APIException
from src.common.response import APIResponse
from src.common.response.codes import Http5XX

logger = logging.getLogger(__name__)


def handle_exception(func):
    if iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> APIResponse:
            try:
                return await func(*args, **kwargs)

            except APIException as e:
                logger.error(f"{func.__qualname__} - {e}")
                return APIResponse(e.error)

            except Exception as e:
                logger.error(f"{func.__qualname__} - {e}")
                return APIResponse(Http5XX.UNKNOWN_ERROR, data=e.args[0])

    else:
        @wraps(func)
        def wrapper(*args, **kwargs) -> APIResponse:
            try:
                return func(*args, **kwargs)

            except APIException as e:
                logger.error(f"{func.__qualname__} - {e}")
                return APIResponse(e.error)

            except Exception as e:
                logger.error(f"{func.__qualname__} - {e}")
                return APIResponse(Http5XX.UNKNOWN_ERROR, data=e.args[0])

    return wrapper
