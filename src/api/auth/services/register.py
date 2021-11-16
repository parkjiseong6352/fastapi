from datetime import datetime
from typing import Dict

import bcrypt
from sqlalchemy import exists
from sqlalchemy.orm.session import Session

from src.api.user.models import User
from src.common.exceptions import APIException
from src.common.response.codes import Http4XX
from src.config.settings import Settings
from ..authenticate.generations import create_token_response
from ..schemas import UserRegister


class RegisterManager:
    """회원가입 프로세스"""

    def __init__(self, user: UserRegister) -> None:
        self.user = user

    def validate(self, session: Session) -> None:
        if session.query(exists().where(
            User.user_email == self.user.user_email)
        ).scalar():
            raise APIException(Http4XX.REGISTERED_EMAIL)

        if self.user.password != self.user.password_check:
            raise APIException(Http4XX.INCORRECT_PASSWORD)

    def set_password(self) -> str:
        return bcrypt.hashpw(
            self.user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode()

    def create_user(self, session: Session, password: str) -> User:
        user = User(
            user_name=self.user.user_name,
            user_email=self.user.user_email,
            password=password,
            created_dtm=datetime.now(),
            updated_dtm=datetime.now(),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def create_token(self, settings: Settings, user: User) -> Dict:
        return create_token_response(settings, user)

    def run(self, session: Session, settings: Settings) -> Dict:
        self.validate(session)
        password = self.set_password()
        user = self.create_user(session, password)
        return self.create_token(settings, user)
