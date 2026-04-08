import falcon
from pydantic import ValidationError

from adapters.web.schemas.game import AddGameRequest, GameResponse
from adapters.web.utils import parse_uuid
from core.ports.inbound.game_use_case import GameUseCase


class GameCollection:
    def __init__(self, game_use_case: GameUseCase) -> None:
        self.game_use_case = game_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        limit = req.get_param_as_int("limit", default=100)
        offset = req.get_param_as_int("offset", default=0)
        games = await self.game_use_case.list_games(limit, offset)
        resp.media = [GameResponse.from_entity(game).model_dump(mode="json") for game in games]

    async def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            request_body = AddGameRequest.model_validate(await req.get_media())
        except ValidationError as validation_error:
            raise falcon.HTTPBadRequest(description=str(validation_error))
        game = await self.game_use_case.add_game(
            title=request_body.title,
            genre=request_body.genre,
            max_players=request_body.max_players,
        )
        resp.media = GameResponse.from_entity(game).model_dump(mode="json")
        resp.status = falcon.HTTP_201


class GameItem:
    def __init__(self, game_use_case: GameUseCase) -> None:
        self.game_use_case = game_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response, game_id: str) -> None:
        game = await self.game_use_case.get_game(parse_uuid(game_id))
        resp.media = GameResponse.from_entity(game).model_dump(mode="json")

    async def on_delete(self, req: falcon.Request, resp: falcon.Response, game_id: str) -> None:
        await self.game_use_case.remove_game(parse_uuid(game_id))
        resp.status = falcon.HTTP_204
