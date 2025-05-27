from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from .room import Room


class ReservationStatus(Enum):
    RESERVED = "R"  # Reserved
    CHECKED_IN = "A"  # Active - Check-in completed
    CHECKED_OUT = "F"  # Finished - Check-out completed
    CANCELLED = "C"  # Cancelled


@dataclass
class Reservation:
    id: Optional[int] = None
    customer_id: int = None
    room_type: str = None
    number_of_guests: int = None
    number_of_days: int = None
    total_value: float = None
    status: ReservationStatus = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        if not self.room_type:
            raise ValueError("Room type is required")
        if not self.number_of_guests or self.number_of_guests <= 0:
            raise ValueError("Number of guests must be greater than 0")
        if not self.number_of_days or self.number_of_days <= 0:
            raise ValueError("Number of days must be greater than 0")
        if not self.status:
            self.status = ReservationStatus.RESERVED
        if not self.created_at:
            self.created_at = datetime.now()

    @classmethod
    def create(cls) -> 'Reservation':
        return cls()

    def with_id(self, id: int) -> 'Reservation':
        self.id = id
        return self

    def with_customer_id(self, customer_id: int) -> 'Reservation':
        self.customer_id = customer_id
        return self

    def with_room_type(self, room_type: str) -> 'Reservation':
        self.room_type = room_type
        return self

    def with_number_of_guests(self, number_of_guests: int) -> 'Reservation':
        self.number_of_guests = number_of_guests
        return self

    def with_number_of_days(self, number_of_days: int) -> 'Reservation':
        self.number_of_days = number_of_days
        return self

    def with_total_value(self, total_value: float) -> 'Reservation':
        self.total_value = total_value
        return self

    def with_status(self, status: ReservationStatus) -> 'Reservation':
        self.status = status
        return self

    def with_created_at(self, created_at: datetime) -> 'Reservation':
        self.created_at = created_at
        return self

    def with_updated_at(self, updated_at: datetime) -> 'Reservation':
        self.updated_at = updated_at
        return self

    def build(self) -> 'Reservation':
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        if not self.room_type:
            raise ValueError("Room type is required")
        if not self.number_of_guests or self.number_of_guests <= 0:
            raise ValueError("Number of guests must be greater than 0")
        if not self.number_of_days or self.number_of_days <= 0:
            raise ValueError("Number of days must be greater than 0")
        if not self.status:
            self.status = ReservationStatus.RESERVED
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.total_value:
            self.calculate_total_value(Room.get_daily_rate(self.room_type))
        return self

    def calculate_total_value(self, room_value: float) -> float:
        self.total_value = self.number_of_guests * self.number_of_days * room_value
        return self.total_value

    def calculate_total_price(self) -> float:
        daily_rate = Room.get_daily_rate(self.room_type)
        return daily_rate * self.number_of_guests * self.number_of_days
