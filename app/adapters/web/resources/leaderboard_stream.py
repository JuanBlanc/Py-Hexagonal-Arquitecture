import falcon
import falcon.asgi

from adapters.web.schemas.score import ScoreResponse
from adapters.web.utils import parse_uuid
from core.ports.inbound.leaderboard_stream_use_case import LeaderboardStreamUseCase


class LeaderboardStream:
    """Adaptador WebSocket del stream del leaderboard.

    Solo depende del caso de uso de streaming (publisher), no de la base de datos,
    así que no participa en el Unit of Work por petición.
    """

    def __init__(self, leaderboard_stream_use_case: LeaderboardStreamUseCase) -> None:
        self.leaderboard_stream_use_case = leaderboard_stream_use_case

    async def on_websocket(
        self, req: falcon.Request, ws: falcon.asgi.WebSocket, game_id: str
    ) -> None:
        await ws.accept()
        subscription = self.leaderboard_stream_use_case.watch_leaderboard(parse_uuid(game_id))
        try:
            while True:
                score = await subscription.next_score()
                await ws.send_media(ScoreResponse.from_entity(score).model_dump(mode="json"))
        except falcon.WebSocketDisconnected:
            pass
        finally:
            await subscription.close()
