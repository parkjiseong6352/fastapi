from pydantic.main import BaseModel


class UserRegister(BaseModel):
    user_name: str
    user_email: str
    password: str
    password_check: str


class UserLogin(BaseModel):
    user_email: str
    password: str


class RefreshToken(BaseModel):
    refresh: str
