from typing import Dict

from src.api.user.models import User
from src.config.settings import Settings
from .jwt_handler import encode_payloads


def generate_access_token(settings: Settings, user: User) -> str:
    payloads = {
        "user": user,
        "expiration_interval": settings.JWT_ACCESS_EXPIRED_INTERVAL,
        "key": settings.SECRET_KEY,
    }
    return encode_payloads(**payloads)


def generate_refresh_token(settings: Settings, user: User) -> str:
    return encode_payloads(
        user, settings.JWT_REFRESH_EXPIRED_INTERVAL, settings.SECRET_KEY
    )


def create_token_response(settings: Settings, user: User) -> Dict:
    return {
        "access": generate_access_token(settings, user),
        "refresh": generate_refresh_token(settings, user),
    }
