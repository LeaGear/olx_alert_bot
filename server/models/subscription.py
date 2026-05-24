from dataclasses import dataclass, field
from typing import Optional, List
from sqlalchemy import BigInteger, ForeignKey, String, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from server.database import Base

class User(Base):
    __tablename__ = "users"

    telegram_id:Mapped[int] = mapped_column(BigInteger, primary_key=True)

    subscriptions:Mapped[List['Subscription']] = relationship(back_populates ="user", cascade = "all, delete-orphan")



class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int]= mapped_column(primary_key = True, autoincrement = True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete = "CASCADE"))

    name: Mapped[str] = mapped_column(String(150))
    url: Mapped[str] = mapped_column(String(1000))

    content: Mapped[Optional[List]] = mapped_column(JSON, default=list)
    content_hash: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    user: Mapped["User"] = relationship(back_populates = "subscriptions")

@dataclass
class Subscription:
    user_id: int
    name: str
    url: str

    content: List[dict] = field(default_factory=list)
    content_hash: Optional[str] = None

