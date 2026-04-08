import falcon
from pydantic import ValidationError

from adapters.web.schemas.match import CreateMatchRequest, MatchResponse
from adapters.web.utils import parse_uuid
from core.ports.inbound.match_use_case import MatchUseCase


class MatchCollection:
    def __init__(self, match_use_case: MatchUseCase) -> None:
        self.match_use_case = match_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        limit = req.get_param_as_int("limit", default=100)
        offset = req.get_param_as_int("offset", default=0)
        matches = await self.match_use_case.list_matches(limit, offset)
        resp.media = [MatchResponse.from_entity(match).model_dump(mode="json") for match in matches]

    async def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            request_body = CreateMatchRequest.model_validate(await req.get_media())
        except ValidationError as validation_error:
            raise falcon.HTTPBadRequest(description=str(validation_error))
        match = await self.match_use_case.create_match(
            game_id=request_body.game_id,
            host_player_id=request_body.host_player_id,
        )
        resp.media = MatchResponse.from_entity(match).model_dump(mode="json")
        resp.status = falcon.HTTP_201


class MatchItem:
    def __init__(self, match_use_case: MatchUseCase) -> None:
        self.match_use_case = match_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response, match_id: str) -> None:
        match = await self.match_use_case.get_match(parse_uuid(match_id))
        resp.media = MatchResponse.from_entity(match).model_dump(mode="json")


class MatchLifecycle:
    def __init__(self, match_use_case: MatchUseCase) -> None:
        self.match_use_case = match_use_case

    async def on_post_start(self, req: falcon.Request, resp: falcon.Response, match_id: str) -> None:
        match = await self.match_use_case.start_match(parse_uuid(match_id))
        resp.media = MatchResponse.from_entity(match).model_dump(mode="json")

    async def on_post_finish(self, req: falcon.Request, resp: falcon.Response, match_id: str) -> None:
        match = await self.match_use_case.finish_match(parse_uuid(match_id))
        resp.media = MatchResponse.from_entity(match).model_dump(mode="json")

    async def on_post_abort(self, req: falcon.Request, resp: falcon.Response, match_id: str) -> None:
        match = await self.match_use_case.abort_match(parse_uuid(match_id))
        resp.media = MatchResponse.from_entity(match).model_dump(mode="json")
