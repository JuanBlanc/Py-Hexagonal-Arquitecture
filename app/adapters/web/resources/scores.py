import falcon
from pydantic import ValidationError

from adapters.web.schemas.score import ScoreResponse, SubmitScoreRequest
from adapters.web.utils import parse_uuid
from core.ports.inbound.score_use_case import ScoreUseCase


class MatchScoreCollection:
    def __init__(self, score_use_case: ScoreUseCase) -> None:
        self.score_use_case = score_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response, match_id: str) -> None:
        scores = await self.score_use_case.list_match_scores(parse_uuid(match_id))
        resp.media = [ScoreResponse.from_entity(score).model_dump(mode="json") for score in scores]

    async def on_post(self, req: falcon.Request, resp: falcon.Response, match_id: str) -> None:
        try:
            request_body = SubmitScoreRequest.model_validate(await req.get_media())
        except ValidationError as validation_error:
            raise falcon.HTTPBadRequest(description=str(validation_error))
        score = await self.score_use_case.submit_score(
            match_id=parse_uuid(match_id),
            player_id=request_body.player_id,
            points=request_body.points,
        )
        resp.media = ScoreResponse.from_entity(score).model_dump(mode="json")
        resp.status = falcon.HTTP_201


class GameLeaderboard:
    def __init__(self, score_use_case: ScoreUseCase) -> None:
        self.score_use_case = score_use_case

    async def on_get(self, req: falcon.Request, resp: falcon.Response, game_id: str) -> None:
        limit = req.get_param_as_int("limit", default=10)
        scores = await self.score_use_case.leaderboard(parse_uuid(game_id), limit)
        resp.media = [ScoreResponse.from_entity(score).model_dump(mode="json") for score in scores]
