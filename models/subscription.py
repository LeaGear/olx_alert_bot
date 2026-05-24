from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Subscription:
    user_id: int
    name: str
    url: str

    content: List[dict] = field(default_factory=list)
    content_hash: Optional[str] = None

