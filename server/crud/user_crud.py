import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.db.user_table import User


async def get_db_user_id(db: AsyncSession, user_id: int):
    query = select(User.id).where(User.telegram_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_id: int):
    db_user = User(telegram_id=user_id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
