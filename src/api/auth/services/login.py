from typing import Dict

import bcrypt
from sqlalchemy.orm.session import Session

from src.api.user.models import User
from src.common.exceptions import APIException
from src.common.response.codes import Http4XX
from src.config.settings import Settings
from ..authenticate.generations import create_token_response
from ..schemas import UserLogin


class LoginManager:
    """로그인 프로세스"""

    def __init__(self, user: UserLogin) -> None:
        self.user = user

    def get_user(self, session: Session) -> User:
        user = session.query(User).filter(
            User.user_email == self.user.user_email
        ).first()
        if not user:
            raise APIException(Http4XX.INVALID_EMAIL)
        return user

    def check_password(self, password: str) -> None:
        if not bcrypt.checkpw(
            self.user.password.encode("utf-8"), password.encode("utf-8")
        ):
            raise APIException(Http4XX.INCORRECT_PASSWORD)

    def create_token(self, settings: Settings, user: User) -> Dict:
        return create_token_response(settings, user)

    def run(self, session: Session, settings) -> Dict:
        user = self.get_user(session)
        self.check_password(user.password)
        return self.create_token(settings, user)
