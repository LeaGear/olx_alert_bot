from typing import Optional, List
from sqlalchemy import BigInteger, ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.base import Base

#Subscription table schema
class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150))
    url: Mapped[str] = mapped_column(String(1000))
    content: Mapped[Optional[List]] = mapped_column(JSON, default=list)
    content_ids : Mapped[Optional[List]] = mapped_column(JSON, default=list)
    new_content_ids : Mapped[Optional[List]] = mapped_column(JSON, default=list)

    user: Mapped["User"] = relationship(back_populates="subscriptions")
