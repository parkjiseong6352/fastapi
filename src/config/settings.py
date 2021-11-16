from datetime import timedelta
from functools import lru_cache
import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


class Settings(BaseSettings):
    """
    :Logic
        1. 기본적으로 .env 파일을 최우선 순위로 일어와 환경변수 세팅 (FASTAPI_ENV 와 무관)
        2. .env가 없는 경우엔 FASTAPI_ENV 에 해당되는 환경으로 세팅
        3. 아무 설정이 안 되어 있으면 기본값으로 local 환경으로 세팅
    """
    BASE_DIR: str = BASE_DIR
    APP_ENV: str
    DEBUG: bool = False

    SECRET_KEY: str

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    JWT_ACCESS_EXPIRED_INTERVAL: timedelta = timedelta(hours=12)
    JWT_REFRESH_EXPIRED_INTERVAL: timedelta = timedelta(days=180)

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    env = os.getenv("FASTAPI_ENV", "local")
    print(f"ENV:\t {env}")
    return Settings(_env_file=f".env.{env}")
