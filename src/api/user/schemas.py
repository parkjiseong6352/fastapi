from pydantic.main import BaseModel


class User(BaseModel):
    pk: int
    user_name: str
    user_email: str
