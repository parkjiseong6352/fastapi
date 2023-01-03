from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_DATABASE_URL = "mysql+pymysql://root:root@localhost:3308/jiseong?charset=utf8"
engine = create_engine(MYSQL_DATABASE_URL, encoding='utf-8')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(
    url="mysql+aiomysql://root:root@localhost:3308/jiseong?charset=utf8",
)