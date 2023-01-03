from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
# from database import SessionLocal, engine
# from async_database import SessionLocal, engine
from sqlalchemy.ext.asyncio import AsyncSession
from async_database import DBConnection


app = FastAPI()
db = DBConnection()
db.init_app()
@app.post("/users/")
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(db.get_session)):
    coroutine_result = await crud.get_user_by_email(session, email=user.email)
    db_user = coroutine_result.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    data = await crud.create_user(session=session, user=user)
    return data


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(db.get_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{email}")
async def read_user(email: str, session: AsyncSession = Depends(db.get_session)):
    coroutine_reuslt = await crud.get_user_by_email(session, email=email)
    db_user = coroutine_reuslt.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(db.get_session)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(db.get_session)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
