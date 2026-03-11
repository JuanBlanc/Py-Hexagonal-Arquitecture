import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Player:
    username: str
    display_name: str
    region: str
    level: int = 1
    player_id: uuid.UUID | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
