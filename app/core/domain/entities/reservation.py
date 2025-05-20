from datetime import datetime
from enum import Enum
from typing import Optional
from .room import Room


class ReservationStatus(Enum):
    RESERVED = "R"  # Reserved
    CHECKED_IN = "A"  # Active - Check-in completed
    CHECKED_OUT = "F"  # Finished - Check-out completed
    CANCELLED = "C"  # Cancelled


class Reservation:
    def __init__(
        self,
        id: Optional[int],
        customer_id: int,
        room_type: str,
        number_of_guests: int,
        number_of_days: int,
        total_value: float,
        status: ReservationStatus,
        created_at: datetime,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.customer_id = customer_id
        self.room_type = room_type
        self.number_of_guests = number_of_guests
        self.number_of_days = number_of_days
        self.total_value = total_value
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"Reservation(id={self.id}, customer_id={self.customer_id}, room_type='{self.room_type}', number_of_guests={self.number_of_guests}, number_of_days={self.number_of_days}, total_value={self.total_value}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})"

    def calculate_total_value(self, room_value: float) -> float:
        self.total_value = self.number_of_guests * self.number_of_days * room_value
        return self.total_value

    def calculate_total_price(self) -> float:
        daily_rate = Room.get_daily_rate(self.room_type)
        return daily_rate * self.number_of_guests * self.number_of_days
