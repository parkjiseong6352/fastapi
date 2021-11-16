from typing import Dict
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from src.api.user.models import User
from src.common.authorization import JWTAuthorization
from src.config.connections.database import db
from src.config.settings import Settings, get_settings
from src.api.auth.authenticate.generations import generate_access_token
from src.api.auth.authenticate.jwt_handler import decode_token
from src.api.auth.schemas import RefreshToken

jwt_token_scheme = JWTAuthorization()


def _get_user_from_token(
    token: str, session: Session, settings: Settings
) -> User:
    payload = decode_token(token, settings.SECRET_KEY)
    return session.query(User).filter(User.id == payload.get("pk")).first()


async def generate_from_refresh_token(
    body: RefreshToken,
    session: Session = Depends(db.session),
    settings: Settings = Depends(get_settings),
) -> Dict:
    user = _get_user_from_token(body.refresh, session, settings)
    return {
        "access": generate_access_token(settings, user),
        "refresh": body.refresh
    }


async def get_user_from_authorization(
    refresh_token: str = Depends(jwt_token_scheme),
    session: Session = Depends(db.session),
    settings: Settings = Depends(get_settings),
) -> User:
    return _get_user_from_token(refresh_token, session, settings)

