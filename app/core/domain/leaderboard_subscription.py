import uuid
from abc import ABC, abstractmethod

from core.domain.entities.score import Score


class LeaderboardSubscription(ABC):
    """Suscripción viva al stream del leaderboard de una partida.

    Contrato neutral del dominio: lo produce el puerto outbound (publisher) y lo
    devuelve el puerto inbound (caso de uso de streaming). Vive en el dominio para
    que ninguno de los dos lados del hexágono dependa del otro.
    """

    @abstractmethod
    async def next_score(self) -> Score: ...

    @abstractmethod
    async def close(self) -> None: ...
