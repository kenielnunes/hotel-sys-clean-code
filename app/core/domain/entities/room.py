from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import Dict


class RoomType(Enum):
    STANDARD = "S"  # Standard Room
    DELUXE = "D"  # Deluxe Room
    PREMIUM = "P"  # Premium Room


@dataclass
class Room:
    id: int
    type: RoomType
    daily_rate: float
    created_at: datetime

    def __post_init__(self):
        if not self.type:
            raise ValueError("Room type is required")
        if not self.daily_rate:
            self.daily_rate = self._get_daily_rate()

    def _get_description(self) -> str:
        descriptions = {
            RoomType.STANDARD: "Standard Room",
            RoomType.DELUXE: "Deluxe Room",
            RoomType.PREMIUM: "Premium Room",
        }
        return descriptions.get(self.type, "Unknown room type")

    def _get_daily_rate(self) -> float:
        rates = {
            RoomType.STANDARD: 100.0,
            RoomType.DELUXE: 200.0,
            RoomType.PREMIUM: 300.0,
        }
        return rates.get(self.type, 0.0)

    @staticmethod
    def get_daily_rate(room_type: str) -> float:
        rates = {
            RoomType.STANDARD.value: 100.0,
            RoomType.DELUXE.value: 200.0,
            RoomType.PREMIUM.value: 300.0,
        }
        room_type = room_type.upper()
        if room_type not in rates:
            raise ValueError(f"Invalid room type: {room_type}")
        return rates[room_type]

    @staticmethod
    def get_description(room_type: str) -> str:
        descriptions = {
            RoomType.STANDARD.value: "Standard Room",
            RoomType.DELUXE.value: "Deluxe Room",
            RoomType.PREMIUM.value: "Premium Room",
        }
        room_type = room_type.upper()
        if room_type not in descriptions:
            raise ValueError(f"Invalid room type: {room_type}")
        return descriptions[room_type]
