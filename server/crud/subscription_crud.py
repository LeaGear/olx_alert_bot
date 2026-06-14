from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select

from server.db.subscription_table import Subscription


async def update_subscriptions(db: AsyncSession, data_from_parser: List):
    for sub_data in data_from_parser:
        query = select(Subscription).where(Subscription.id == sub_data.get('id'),
                                           Subscription.name == sub_data.get("name"))
        result = await db.execute(query)
        db_sub = result.scalar_one_or_none()

        if db_sub:
            db_sub.content = sub_data.get("content")
            flag_modified(db_sub, "content")

            db_sub.content_ids = sub_data.get("content_ids")
            flag_modified(db_sub, "content_ids")

            db_sub.new_content_ids = sub_data.get("new_content_ids")
            flag_modified(db_sub, "new_content_ids")

    await db.commit()


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
