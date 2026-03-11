import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Game:
    title: str
    genre: str
    max_players: int
    game_id: uuid.UUID | None = field(default=None)
    created_at: datetime | None = field(default=None)
