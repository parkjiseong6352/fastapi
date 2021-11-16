from datetime import datetime

from sqlalchemy.orm.session import Session

from src.common.exceptions import APIException
from src.common.response.codes import Http4XX
from .models import Parent
from .schemas import ParentCreate


def create_parent(parent: ParentCreate, db: Session) -> Parent:
    instance = Parent(
        parent_name=parent.parent_name,
        created_dtm=datetime.now(),
        updated_dtm=datetime.now()
    )
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_parent(idx: int, db: Session) -> Parent:
    data = db.query(Parent).filter(Parent.id == idx).first()
    if not data:
        raise APIException(Http4XX.BAE_REQUEST)
    return data
