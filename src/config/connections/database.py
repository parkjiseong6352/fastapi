from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from src.config.settings import get_settings


class DBConnection:
    def __init__(self) -> None:
        self.engine = None
        self._session = None

    def init_app(self, app: FastAPI) -> None:
        settings = get_settings()
        sqlalchemy_database_url = (
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )

        self.engine = create_engine(sqlalchemy_database_url)
        self._session = scoped_session(
            sessionmaker(autocommit=False ,autoflush=False, bind=self.engine)
        )

        @app.on_event("startup")
        def startup():
            self.engine.connect()

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self.engine.dispose()

    def get_session(self) -> Session:
        session = self._session()
        try:
            yield session
        finally:
            session.close()

    @property
    def session(self):
        return self.get_session


db = DBConnection()
Base = declarative_base()
