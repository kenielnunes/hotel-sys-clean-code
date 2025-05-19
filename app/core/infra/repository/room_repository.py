from typing import Optional, List
from core.domain.entities.room import Room, RoomType
from .base_repository import BaseRepository

class RoomRepository(BaseRepository[Room]):
    def __init__(self):
        super().__init__("rooms")

    def create(self, room: Room) -> Room:
        cursor = self._get_cursor()
        cursor.execute(
            "INSERT INTO rooms (type, daily_rate) VALUES (?, ?)",
            (room.type.value, room.daily_rate)
        )
        self._commit()
        room.id = cursor.lastrowid
        return room

    def update(self, room: Room) -> Room:
        cursor = self._get_cursor()
        cursor.execute(
            "UPDATE rooms SET type = ?, daily_rate = ? WHERE id = ?",
            (room.type.value, room.daily_rate, room.id)
        )
        self._commit()
        return room

    def find_by_type(self, room_type: RoomType) -> Optional[Room]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM rooms WHERE type = ?", (room_type.value,))
        row = cursor.fetchone()
        return self._map_row_to_entity(row) if row else None

    def _map_row_to_entity(self, row) -> Room:
        return Room(
            id=row[0],
            type=RoomType(row[1]),
            daily_rate=row[2]
        ) 