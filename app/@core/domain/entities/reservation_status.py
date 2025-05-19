from enum import Enum

class ReservationStatus(Enum):
    RESERVED = "R"  # Reserved
    CHECKED_IN = "A"  # Active/Checked In
    CANCELLED = "C"  # Cancelled
    CHECKED_OUT = "F"  # Finished/Checked Out

    @classmethod
    def from_str(cls, status: str) -> 'ReservationStatus':
        for enum_status in cls:
            if enum_status.value == status.upper():
                return enum_status
        raise ValueError(f"Invalid reservation status: {status}") 