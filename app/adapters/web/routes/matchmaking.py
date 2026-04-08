import falcon.asgi

from adapters.web.resources.matchmaking import OpponentSuggestions
from core.ports.inbound.matchmaking_use_case import MatchmakingUseCase


def register(app: falcon.asgi.App, matchmaking_use_case: MatchmakingUseCase) -> None:
    app.add_route("/players/{player_id}/opponents", OpponentSuggestions(matchmaking_use_case))
