from fastapi import APIRouter
from fastapi.param_functions import Depends

from src.common.dependencies import get_user_from_authorization
from src.common.response import APIResponse
from src.common.response.codes import Http2XX
from .models import User
from . import schemas

router = APIRouter()


@router.get("/info", response_model=schemas.User, response_model_exclude={"password"})
async def register(
    user: User = Depends(get_user_from_authorization)
) -> APIResponse:
    """회원 조회"""
    return APIResponse(Http2XX.SUCCESS, data=user)
