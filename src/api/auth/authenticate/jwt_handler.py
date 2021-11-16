from datetime import datetime, timedelta
import time
from typing import Dict

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError
from src.common.exceptions import APIException
from src.common.response.codes import Http4XX

from src.api.user.models import User


def encode_payloads(
    user: User, expiration_interval: timedelta, key: str, **kwargs
) -> str:
    expired_at = time.mktime(
        (datetime.now() + expiration_interval).timetuple()
    )
    data = {
        'pk': user.id,
        'user_name': user.user_name,
        'is_active': user.is_active,
        'exp': int(expired_at)
    }
    data.update(kwargs)
    return jwt.encode(payload=data, key=key, algorithm='HS256')


def decode_token(token: str, key: str) -> Dict:
    try:
        return jwt.decode(jwt=token, key=key, algorithms='HS256')
    except DecodeError:
        raise APIException(Http4XX.JWT_DecodeError)
    except ExpiredSignatureError:
        raise APIException(Http4XX.JWT_ExpiredSignature)
    except InvalidTokenError:
        raise APIException(Http4XX.JWT_InvalidTokenError)

