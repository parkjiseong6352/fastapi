from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.config.connections.database import Base


class User(Base):
    __tablename__ = "t_user"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(length=31))
    user_email = Column(String(length=254), unique=True)
    password = Column(String(length=100))
    created_dtm = Column(DateTime)
    updated_dtm = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
