import uuid
from collections.abc import Sequence
from typing import Any

from core.domain.entities.player import Player
from core.domain.errors import DuplicateEntity, EntityNotFound
from core.ports.inbound.player_use_case import PlayerUseCase
from core.ports.outbound.unit_of_work import UnitOfWorkFactory


class PlayerService(PlayerUseCase):
    def __init__(self, unit_of_work: UnitOfWorkFactory) -> None:
        self._unit_of_work = unit_of_work

    async def register_player(self, username: str, display_name: str, region: str) -> Player:
        async with self._unit_of_work() as uow:
            already_registered = await uow.players.find_by_username(username)
            if already_registered is not None:
                raise DuplicateEntity(f"username already taken: {username}")
            new_player = Player(username=username, display_name=display_name, region=region)
            return await uow.players.add(new_player)

    async def get_player(self, player_id: uuid.UUID) -> Player:
        async with self._unit_of_work() as uow:
            player = await uow.players.get(player_id)
            if player is None:
                raise EntityNotFound(f"player not found: {player_id}")
            return player

    async def list_players(self, limit: int, offset: int) -> Sequence[Player]:
        async with self._unit_of_work() as uow:
            return await uow.players.list(limit, offset)

    async def update_player(self, player_id: uuid.UUID, changes: dict[str, Any]) -> Player:
        async with self._unit_of_work() as uow:
            player = await uow.players.get(player_id)
            if player is None:
                raise EntityNotFound(f"player not found: {player_id}")
            for field_name, new_value in changes.items():
                setattr(player, field_name, new_value)
            return await uow.players.update(player)

    async def delete_player(self, player_id: uuid.UUID) -> None:
        async with self._unit_of_work() as uow:
            player = await uow.players.get(player_id)
            if player is None:
                raise EntityNotFound(f"player not found: {player_id}")
            await uow.players.remove(player)
