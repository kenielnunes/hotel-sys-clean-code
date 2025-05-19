from dataclasses import dataclass
from enum import Enum

class RoomType(Enum):
    STANDARD = "S"
    DELUXE = "D"
    PREMIUM = "P"

@dataclass
class Room:
    id: int = None
    type: RoomType = None
    daily_rate: float = None

    def __post_init__(self):
        if not self.type:
            raise ValueError("Room type is required")
        if not self.daily_rate:
            raise ValueError("Daily rate is required")

    @staticmethod
    def get_daily_rate(type: RoomType) -> float:
        rates = {
            RoomType.STANDARD: 100.0,
            RoomType.DELUXE: 200.0,
            RoomType.PREMIUM: 300.0
        }
        return rates.get(type, 0.0) 