from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: str
    detail: Optional[str] = None
    data: Optional[T] = None

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