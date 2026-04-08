import falcon.asgi

from adapters.web.resources.players import PlayerCollection, PlayerItem
from core.ports.inbound.player_use_case import PlayerUseCase


def register(app: falcon.asgi.App, player_use_case: PlayerUseCase) -> None:
    app.add_route("/players", PlayerCollection(player_use_case))
    app.add_route("/players/{player_id}", PlayerItem(player_use_case))
