from abc import ABC, abstractmethod
from collections.abc import Callable
from types import TracebackType

from core.ports.outbound.game_repository import GameRepository
from core.ports.outbound.match_repository import MatchRepository
from core.ports.outbound.player_repository import PlayerRepository
from core.ports.outbound.score_repository import ScoreRepository


class UnitOfWork(ABC):
    """Puerto de salida: límite transaccional sobre los repositorios.

    Es un context manager async. El caso de uso (capa de aplicación) decide el
    límite de la transacción abriéndolo: confirma al salir bien y revierte ante
    cualquier excepción. El núcleo posee esta interfaz; cada adaptador de
    persistencia la implementa (memoria, postgres).
    """

    players: PlayerRepository
    games: GameRepository
    matches: MatchRepository
    scores: ScoreRepository

    async def __aenter__(self) -> "UnitOfWork":
        await self._begin()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self._close()

    @abstractmethod
    async def _begin(self) -> None:
        """Inicia la unidad de trabajo y deja listos los repositorios."""

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def _close(self) -> None: ...


# El núcleo recibe una fábrica (no una instancia): cada caso de uso abre su
# propia unidad de trabajo, de forma segura ante concurrencia.
UnitOfWorkFactory = Callable[[], UnitOfWork]
