from typing import List, Dict
from core.domain.entities.room import Room, RoomType
from core.infra.repositories.room_repository import RoomRepository

class ListRoomsUseCase:
    def __init__(self, room_repository: RoomRepository):
        self._room_repository = room_repository

    def execute(self) -> List[Dict]:
        # Cria uma lista de quartos com todos os tipos disponíveis
        rooms = [
            Room(type=RoomType.STANDARD),
            Room(type=RoomType.DELUXE),
            Room(type=RoomType.PREMIUM)
        ]
        
        return [
            {
                "type": room.type.value,
                "description": room.description,
                "daily_rate": room.daily_rate
            }
            for room in rooms
        ] 