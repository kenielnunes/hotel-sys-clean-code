from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from .customer import Customer
from .room import Room, RoomType

class ReservationStatus(Enum):
    RESERVED = "R"
    CHECKED_IN = "A"
    CANCELLED = "C"
    CHECKED_OUT = "F"

@dataclass
class Reservation:
    id: int = None
    customer_id: int = None
    room_type: str = None
    number_of_guests: int = None
    number_of_days: int = None
    total_value: float = None
    status: ReservationStatus = ReservationStatus.RESERVED
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        if not self.room_type:
            raise ValueError("Room type is required")
        if not self.number_of_guests:
            raise ValueError("Number of guests is required")
        if not self.number_of_days:
            raise ValueError("Number of days is required")
        if not self.status:
            self.status = ReservationStatus.RESERVED
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    def calculate_total_value(self, room_value: float) -> float:
        self.total_value = self.number_of_guests * self.number_of_days * room_value
        return self.total_value

    def calculate_total_price(self) -> float:
        daily_rate = Room.get_daily_rate(self.room_type)
        return daily_rate * self.number_of_guests * self.number_of_days 