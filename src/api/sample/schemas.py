from datetime import datetime
from pydantic.main import BaseModel


class Parent(BaseModel):
    id: int
    parent_name: str
    created_dtm: datetime 
    updated_dtm: datetime

    class Config:
        orm_model = True


class ParentCreate(BaseModel):
    parent_name: str
