from dataclasses import dataclass
from datetime import datetime
from .customer import Customer
from .room import Room, RoomType
from .reservation_status import ReservationStatus

@dataclass
class Reservation:
    id: int = None
    customer: Customer = None
    number_of_guests: int = None
    room_type: RoomType = None
    number_of_days: int = None
    total_price: float = None
    status: ReservationStatus = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if not self.customer:
            raise ValueError("Customer is required")
        if not self.number_of_guests:
            raise ValueError("Number of guests is required")
        if not self.room_type:
            raise ValueError("Room type is required")
        if not self.number_of_days:
            raise ValueError("Number of days is required")
        if not self.status:
            self.status = ReservationStatus.RESERVED
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    def calculate_total_price(self) -> float:
        daily_rate = Room.get_daily_rate(self.room_type)
        return daily_rate * self.number_of_guests * self.number_of_days 