import uuid
from collections.abc import Sequence

from core.domain.entities.player import Player
from core.domain.errors import EntityNotFound
from core.ports.inbound.matchmaking_use_case import MatchmakingUseCase
from core.ports.outbound.matchmaking_provider import MatchmakingProvider
from core.ports.outbound.unit_of_work import UnitOfWorkFactory


class MatchmakingService(MatchmakingUseCase):
    def __init__(
        self,
        unit_of_work: UnitOfWorkFactory,
        matchmaking_provider: MatchmakingProvider,
    ) -> None:
        self._unit_of_work = unit_of_work
        self.matchmaking_provider = matchmaking_provider

    async def find_opponents(self, player_id: uuid.UUID, desired_count: int) -> Sequence[Player]:
        async with self._unit_of_work() as uow:
            player = await uow.players.get(player_id)
            if player is None:
                raise EntityNotFound(f"player not found: {player_id}")
            candidate_pool = await uow.players.list(limit=1000, offset=0)
        return await self.matchmaking_provider.select_opponents(player, candidate_pool, desired_count)
