from typing import List

from pydantic import BaseModel, Field, field_validator
import re


class SubscriptionResponse(BaseModel):
    name: str = Field(description="Имя подписки юзера")
    url: str = Field(description="Ссылка этой подписки")

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    telegram_id: int = Field(description="Telegram ID пользователя")
    name: str = Field(description="Название подписки")
    url: str = Field(description="Ссылка на OLX с фильтрами или без")
    content: List[dict] = Field(default=[], description="Поле заполняет парсер данными с сайта")
    content_ids: List = Field(default=[], description="Список айди каждого обьекта контента")
    new_content_ids: List = Field(default=[], description="Только уникальные айди которых небыло в старом контенте")

    @field_validator("url")
    @classmethod
    def validate_olx_url(cls, v: str) -> str:
        olx_pattern = r"^https?://(?:www\.)?olx\.ua/.*"

        if not re.match(olx_pattern, v):
            raise ValueError("Ссылка должна быть валидным URL-адресом платформы OLX.ua")

        return v
