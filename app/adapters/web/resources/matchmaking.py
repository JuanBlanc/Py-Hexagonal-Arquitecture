import falcon

from adapters.web.schemas.player import PlayerResponse
from adapters.web.utils import parse_uuid
from core.ports.inbound.matchmaking_use_case import MatchmakingUseCase


class OpponentSuggestions:
    def __init__(self, matchmaking_use_case: MatchmakingUseCase) -> None:
        self.matchmaking_use_case = matchmaking_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        desired_count = req.get_param_as_int("count", default=5)
        opponents = await self.matchmaking_use_case.find_opponents(
            parse_uuid(player_id), desired_count
        )
        resp.media = [
            PlayerResponse.from_entity(opponent).model_dump(mode="json") for opponent in opponents
        ]
