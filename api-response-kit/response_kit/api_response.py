from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    status: str = Field(description="Статус ответа сервера - успех/ошибка")
    detail: Optional[str] = Field(default=None, description="Детали ошибки или успеха")
    data: Optional[T] = Field(default=None, description="Переданные данные")

    @property
    def ok(self) -> bool:
        return self.status == "success"


class Detail:
    NOT_FOUND = "not_found"
    SERVER_DOWN = "server_down"
    INVALID_DATA = "invalid_data"
    SUB_ADDED = "sub_added_successfully"
    SUB_DELETED = "sub_deleted_successfully"
    UNKNOWN = "unknown_error"
