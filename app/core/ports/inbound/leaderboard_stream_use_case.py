import uuid
from abc import ABC, abstractmethod

from core.domain.leaderboard_subscription import LeaderboardSubscription


class LeaderboardStreamUseCase(ABC):
    """Caso de uso de streaming del leaderboard en tiempo real.

    Separado de ScoreUseCase porque solo necesita el publisher (no toca repos
    ni base de datos), de modo que el adaptador WebSocket no requiere sesión.
    """

    @abstractmethod
    def watch_leaderboard(self, game_id: uuid.UUID) -> LeaderboardSubscription: ...
