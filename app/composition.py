from adapters.matchmaking.in_memory_matchmaking_provider import InMemoryMatchmakingProvider
from adapters.messaging.in_memory_leaderboard_publisher import InMemoryLeaderboardPublisher
from adapters.persistence.memory.store import InMemoryStore
from adapters.persistence.memory.unit_of_work import MemoryUnitOfWork
from core.application.game_service import GameService
from core.application.leaderboard_stream_service import LeaderboardStreamService
from core.application.match_service import MatchService
from core.application.matchmaking_service import MatchmakingService
from core.application.player_service import PlayerService
from core.application.score_service import ScoreService
from core.ports.inbound.game_use_case import GameUseCase
from core.ports.inbound.leaderboard_stream_use_case import LeaderboardStreamUseCase
from core.ports.inbound.match_use_case import MatchUseCase
from core.ports.inbound.matchmaking_use_case import MatchmakingUseCase
from core.ports.inbound.player_use_case import PlayerUseCase
from core.ports.inbound.score_use_case import ScoreUseCase
from core.ports.outbound.unit_of_work import UnitOfWork

from config import Settings, settings


class CompositionRoot:
    """Único módulo que conoce los adaptadores concretos.

    Elige el backend según `settings.persistence` (memory | postgres) y arma una
    *fábrica* de unidades de trabajo. Cada caso de uso recibe esa fábrica y abre
    su propia transacción: el límite transaccional pertenece a la aplicación, no
    a la web.
    """

    def __init__(self, settings: Settings = settings) -> None:
        self._settings = settings
        self._database = None
        self._store: InMemoryStore | None = None

        # Adaptadores singleton (no transaccionales).
        leaderboard_publisher = InMemoryLeaderboardPublisher()
        matchmaking_provider = InMemoryMatchmakingProvider()

        if settings.persistence == "postgres":
            from adapters.persistence.postgres.engine import Database

            self._database = Database(settings.database_url)
        else:
            self._store = InMemoryStore()

        # Casos de uso (singletons): reciben la fábrica de UoW por inyección.
        self.player_use_case: PlayerUseCase = PlayerService(self._unit_of_work)
        self.game_use_case: GameUseCase = GameService(self._unit_of_work)
        self.match_use_case: MatchUseCase = MatchService(self._unit_of_work)
        self.score_use_case: ScoreUseCase = ScoreService(self._unit_of_work, leaderboard_publisher)
        self.matchmaking_use_case: MatchmakingUseCase = MatchmakingService(
            self._unit_of_work, matchmaking_provider
        )

        # Streaming: solo publisher → sin sesión, singleton.
        self.leaderboard_stream_use_case: LeaderboardStreamUseCase = LeaderboardStreamService(
            leaderboard_publisher
        )

    def _unit_of_work(self) -> UnitOfWork:
        """Fábrica: una unidad de trabajo nueva por cada caso de uso."""
        if self._database is not None:
            from adapters.persistence.postgres.unit_of_work import PostgresUnitOfWork

            return PostgresUnitOfWork(self._database.session_factory)
        assert self._store is not None
        return MemoryUnitOfWork(self._store)

    async def startup(self) -> None:
        if self._database is not None:
            await self._database.create_schema()

    async def shutdown(self) -> None:
        if self._database is not None:
            await self._database.dispose()
