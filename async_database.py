from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
from asyncio import current_task
import models


class DBConnection:
    def __init__(self):
        self.engine = None
        self._session = None

    def init_app(self):
        self.engine = create_async_engine(
            url="mysql+aiomysql://root:root@localhost:3308/jiseong?charset=utf8",
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)
        self._session = async_scoped_session(
            session_factory=SessionLocal,
            scopefunc=current_task,
        )
        # models.Base.metadata.create_all(bind=self.engine)

    # Dependency
    async def get_session(self) -> AsyncSession:
        async with self._session() as session:
            try:
                yield session
            finally:
                await session.close()
        await self._session.remove()


    @property
    def session(self):
        return self.get_session