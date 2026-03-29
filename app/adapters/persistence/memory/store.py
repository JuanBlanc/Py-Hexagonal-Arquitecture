import uuid

from core.domain.entities.game import Game
from core.domain.entities.match import Match
from core.domain.entities.player import Player
from core.domain.entities.score import Score


class InMemoryStore:
    def __init__(self) -> None:
        self.players: dict[uuid.UUID, Player] = {}
        self.games: dict[uuid.UUID, Game] = {}
        self.matches: dict[uuid.UUID, Match] = {}
        self.scores: dict[uuid.UUID, Score] = {}
