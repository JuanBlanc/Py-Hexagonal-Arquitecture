import falcon.asgi

from adapters.web.resources.games import GameCollection, GameItem
from core.ports.inbound.game_use_case import GameUseCase


def register(app: falcon.asgi.App, game_use_case: GameUseCase) -> None:
    app.add_route("/games", GameCollection(game_use_case))
    app.add_route("/games/{game_id}", GameItem(game_use_case))
