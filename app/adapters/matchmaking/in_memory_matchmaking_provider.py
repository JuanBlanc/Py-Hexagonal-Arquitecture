from collections.abc import Sequence

from core.domain.entities.player import Player
from core.ports.outbound.matchmaking_provider import MatchmakingProvider


class InMemoryMatchmakingProvider(MatchmakingProvider):
    async def select_opponents(
        self, player: Player, candidate_pool: Sequence[Player], desired_count: int
    ) -> Sequence[Player]:
        eligible_opponents = [
            candidate
            for candidate in candidate_pool
            if candidate.player_id != player.player_id and candidate.region == player.region
        ]
        ranked_by_level_proximity = sorted(
            eligible_opponents, key=lambda candidate: abs(candidate.level - player.level)
        )
        return ranked_by_level_proximity[:desired_count]
