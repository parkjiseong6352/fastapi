from typing import Optional

from fastapi.openapi.models import HTTPBearer
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from src.common.exceptions import APIException
from src.common.response.codes import Http4XX


class JWTAuthorization(SecurityBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: Optional[bool] = True,
    ) -> None:
        self.model = HTTPBearer(
            bearerFormat=bearerFormat, description=description
        )
        self.scheme_name = self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not authorization or scheme.upper() != "JWT":
            if self.auto_error:
                raise APIException(Http4XX.UNAUTHORIZED)
            else:
                return None
        return credentials
