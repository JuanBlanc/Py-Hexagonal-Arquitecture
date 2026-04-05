import uuid
from datetime import datetime

from pydantic import BaseModel

from core.domain.entities.game import Game


class AddGameRequest(BaseModel):
    title: str
    genre: str
    max_players: int


class GameResponse(BaseModel):
    game_id: uuid.UUID
    title: str
    genre: str
    max_players: int
    created_at: datetime | None

    @classmethod
    def from_entity(cls, game: Game) -> "GameResponse":
        return cls(
            game_id=game.game_id,
            title=game.title,
            genre=game.genre,
            max_players=game.max_players,
            created_at=game.created_at,
        )
