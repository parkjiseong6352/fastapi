from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

import models, schemas
from models import User, Item


def get_user(session: AsyncSession, user_id: int):
    # return db.query.User).filter(User.id == user_id).first()
    pass

async def get_user_by_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    coroutine_result = await session.execute(query)
    return coroutine_result


def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


async def create_user(session: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"  
    insert_query = insert(User).values(email=user.email, hashed_password=fake_hashed_password)
    await session.execute(insert_query)
    await session.commit()
    coroutine_result = await get_user_by_email(session, user.email)
    user = coroutine_result.scalars().first()
    return user

def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
