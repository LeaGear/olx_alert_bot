from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.db.subscription_table import Subscription


async def get_all_subs(db: AsyncSession):
    query = select(Subscription)
    result = await db.execute(query)
    db_all = result.scalars().all()
    return db_all


async def get_user_subs_by_id(db: AsyncSession, user_db_id: int):

    query = select(Subscription).where(Subscription.user_id == user_db_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_subscription(db: AsyncSession, user_db_id: int, name: str, url: str):
    db_subscription = Subscription(
        user_id=user_db_id,
        name=name,
        url=url
    )
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    return db_subscription


async def delete_sub(db: AsyncSession, user_db_id: int, sub_name: str):

    query = select(Subscription).where(Subscription.user_id == user_db_id, Subscription.name == sub_name)
    result = await db.execute(query)
    sub = result.scalar_one_or_none()

    if not sub:
        return False

    await db.delete(sub)
    await db.commit()
    return True
