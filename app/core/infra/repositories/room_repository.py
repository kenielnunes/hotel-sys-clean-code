from typing import Optional, List
from datetime import datetime
from core.domain.entities.room import Room, RoomType
from .base_repository import BaseRepository


class RoomRepository(BaseRepository[Room]):
    def __init__(self):
        super().__init__("rooms")

    def create(self, room: Room) -> Room:
        cursor = self._get_cursor()
        cursor.execute(
            "INSERT INTO rooms (type, daily_rate) VALUES (?, ?)",
            (room.type.code, room.daily_rate),
        )
        self._commit()
        room.id = cursor.lastrowid
        return room

    def update(self, room: Room) -> Room:
        cursor = self._get_cursor()
        cursor.execute(
            "UPDATE rooms SET type = ?, daily_rate = ? WHERE id = ?",
            (room.type.code, room.daily_rate, room.id),
        )
        self._commit()
        return room

    def find_by_type(self, room_type: str) -> Optional[Room]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM rooms WHERE type = ?", (room_type,))
        row = cursor.fetchone()
        return self._map_row_to_entity(row) if row else None

    def find_all(self) -> List[Room]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM rooms ORDER BY type")
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def _map_row_to_entity(self, row) -> Room:
        # Mapeia o código do tipo de quarto para o enum RoomType
        room_type_map = {
            "S": RoomType.STANDARD,
            "D": RoomType.DELUXE,
            "P": RoomType.PREMIUM,
        }
        return Room(
            id=row[0],
            type=room_type_map[row[1]],
            daily_rate=float(row[2]),
            created_at=datetime.fromisoformat(row[3]),
        )
