from typing import List
from datetime import datetime
from core.domain.entities.room import Room, RoomType
from core.infra.repositories.room_repository import RoomRepository

class ListRoomsUseCase:
    def __init__(self, room_repository: RoomRepository):
        self._room_repository = room_repository

    def execute(self) -> List[Room]:
        return self._room_repository.find_all() 