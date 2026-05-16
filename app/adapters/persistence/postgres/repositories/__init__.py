from adapters.persistence.postgres.repositories.game_repository import PostgresGameRepository
from adapters.persistence.postgres.repositories.match_repository import PostgresMatchRepository
from adapters.persistence.postgres.repositories.player_repository import PostgresPlayerRepository
from adapters.persistence.postgres.repositories.score_repository import PostgresScoreRepository

__all__ = [
    "PostgresGameRepository",
    "PostgresMatchRepository",
    "PostgresPlayerRepository",
    "PostgresScoreRepository",
]
