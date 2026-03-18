import uuid
from collections.abc import Sequence

from core.domain.entities.game import Game
from core.domain.errors import EntityNotFound
from core.ports.inbound.game_use_case import GameUseCase
from core.ports.outbound.unit_of_work import UnitOfWorkFactory


class GameService(GameUseCase):
    def __init__(self, unit_of_work: UnitOfWorkFactory) -> None:
        self._unit_of_work = unit_of_work

    async def add_game(self, title: str, genre: str, max_players: int) -> Game:
        async with self._unit_of_work() as uow:
            new_game = Game(title=title, genre=genre, max_players=max_players)
            return await uow.games.add(new_game)

    async def get_game(self, game_id: uuid.UUID) -> Game:
        async with self._unit_of_work() as uow:
            game = await uow.games.get(game_id)
            if game is None:
                raise EntityNotFound(f"game not found: {game_id}")
            return game

    async def list_games(self, limit: int, offset: int) -> Sequence[Game]:
        async with self._unit_of_work() as uow:
            return await uow.games.list(limit, offset)

    async def remove_game(self, game_id: uuid.UUID) -> None:
        async with self._unit_of_work() as uow:
            game = await uow.games.get(game_id)
            if game is None:
                raise EntityNotFound(f"game not found: {game_id}")
            await uow.games.remove(game)
