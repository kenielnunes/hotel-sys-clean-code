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
    description: str = None
    daily_rate: float = None

    def __post_init__(self):
        if not self.type:
            raise ValueError("Room type is required")
        if not self.description:
            self.description = self._get_description()
        if not self.daily_rate:
            self.daily_rate = self._get_daily_rate()

    def _get_description(self) -> str:
        descriptions = {
            RoomType.STANDARD: "Quarto Standard",
            RoomType.DELUXE: "Quarto Deluxe",
            RoomType.PREMIUM: "Quarto Premium"
        }
        return descriptions.get(self.type, "Tipo de quarto desconhecido")

    def _get_daily_rate(self) -> float:
        rates = {
            RoomType.STANDARD: 100.0,
            RoomType.DELUXE: 200.0,
            RoomType.PREMIUM: 300.0
        }
        return rates.get(self.type, 0.0)

    @staticmethod
    def get_daily_rate(type: RoomType) -> float:
        rates = {
            RoomType.STANDARD: 100.0,
            RoomType.DELUXE: 200.0,
            RoomType.PREMIUM: 300.0
        }
        return rates.get(type, 0.0) 