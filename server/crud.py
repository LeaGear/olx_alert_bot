from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.models.subscription import User, Subscription


async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.telegram_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_id: int):
    db_user = User(telegram_id=user_id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

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
