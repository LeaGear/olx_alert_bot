from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.db.user_table import User
from server.db.subscription_table import Subscription


async def get_user_subs_by_id(db: AsyncSession, user_id: int):
    db_user_id = select(User.id).where(User.telegram_id == user_id)

    query = select(Subscription).where(Subscription.user_id == db_user_id)

    result = await db.execute(query)

    return result.scalars().all()


async def create_subscription(db: AsyncSession, user_id: int, name: str, url: str):
    db_subscription = Subscription(
        user_id=user_id,
        name=name,
        url=url
    )
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    return db_subscription


async def delete_sub(db: AsyncSession, telegram_id: int, sub_name: str):
    db_user_id = select(User.id).where(User.telegram_id == telegram_id)

    query = select(Subscription).where(Subscription.user_id == db_user_id, Subscription.name == sub_name)
    result = await db.execute(query)
    sub = result.scalar_one_or_none()

    if not sub:
        return False

    await db.delete(sub)
    await db.commit()
    return True
