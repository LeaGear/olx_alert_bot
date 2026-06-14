from typing import List
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.base import Base

#Create user table schema
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="user", cascade="all, delete-orphan")
