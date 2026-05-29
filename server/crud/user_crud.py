import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.db.user_table import User


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.telegram_id == user_id)
    logging.error(f"USER NOT FOUND: {user_id}___________________{query}---------------------------")
    result = await db.execute(query)
    logging.error(result.scalar_one_or_none())
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_id: int):
    db_user = User(telegram_id=user_id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
