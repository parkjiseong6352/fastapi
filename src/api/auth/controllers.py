from typing import Dict

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from src.common.dependencies import generate_from_refresh_token
from src.common.response import APIResponse
from src.common.response.codes import Http2XX
from src.config.connections.database import db
from src.config.settings import Settings, get_settings
from .schemas import UserLogin, UserRegister
from .services.login import LoginManager
from .services.register import RegisterManager

router = APIRouter()


@router.post("/register")
async def register(
    body: UserRegister,
    session: Session = Depends(db.session),
    settings: Settings = Depends(get_settings),
) -> APIResponse:
    """회원가입"""
    return APIResponse(
        Http2XX.CREATED, data=RegisterManager(body).run(session, settings)
    )


@router.post("/login")
async def login(
    body: UserLogin,
    session: Session = Depends(db.session),
    settings: Settings = Depends(get_settings),
) -> APIResponse:
    """로그인"""
    return APIResponse(
        Http2XX.SUCCESS, data=LoginManager(body).run(session, settings)
    )


@router.post("/refresh")
async def refresh_token(
    data: Dict = Depends(generate_from_refresh_token)
) -> APIResponse:
    """토큰 갱신"""
    return APIResponse(Http2XX.SUCCESS, data=data)
