import falcon
from pydantic import ValidationError

from adapters.web.schemas.player import PlayerResponse, RegisterPlayerRequest, UpdatePlayerRequest
from adapters.web.utils import parse_uuid
from core.ports.inbound.player_use_case import PlayerUseCase


class PlayerCollection:
    def __init__(self, player_use_case: PlayerUseCase) -> None:
        self.player_use_case = player_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        limit = req.get_param_as_int("limit", default=100)
        offset = req.get_param_as_int("offset", default=0)
        players = await self.player_use_case.list_players(limit, offset)
        resp.media = [PlayerResponse.from_entity(player).model_dump(mode="json") for player in players]

    async def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            request_body = RegisterPlayerRequest.model_validate(await req.get_media())
        except ValidationError as validation_error:
            raise falcon.HTTPBadRequest(description=str(validation_error))
        player = await self.player_use_case.register_player(
            username=request_body.username,
            display_name=request_body.display_name,
            region=request_body.region,
        )
        resp.media = PlayerResponse.from_entity(player).model_dump(mode="json")
        resp.status = falcon.HTTP_201


class PlayerItem:
    def __init__(self, player_use_case: PlayerUseCase) -> None:
        self.player_use_case = player_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        player = await self.player_use_case.get_player(parse_uuid(player_id))
        resp.media = PlayerResponse.from_entity(player).model_dump(mode="json")

    async def on_patch(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        try:
            request_body = UpdatePlayerRequest.model_validate(await req.get_media())
        except ValidationError as validation_error:
            raise falcon.HTTPBadRequest(description=str(validation_error))
        player = await self.player_use_case.update_player(
            parse_uuid(player_id), request_body.model_dump(exclude_unset=True)
        )
        resp.media = PlayerResponse.from_entity(player).model_dump(mode="json")

    async def on_delete(self, req: falcon.Request, resp: falcon.Response, player_id: str) -> None:
        await self.player_use_case.delete_player(parse_uuid(player_id))
        resp.status = falcon.HTTP_204
