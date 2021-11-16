from sqlalchemy import Column, DateTime, Integer, String

from src.config.connections.database import Base


class Parent(Base):
    __tablename__ = "parent"

    id = Column(Integer, primary_key=True)
    parent_name = Column(String, nullable=True)
    created_dtm = Column(DateTime, nullable=True)
    updated_dtm = Column(DateTime, nullable=True)
