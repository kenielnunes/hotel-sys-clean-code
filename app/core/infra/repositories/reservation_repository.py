from typing import Optional, List
from datetime import datetime
from core.domain.entities.reservation import Reservation, ReservationStatus
from .base_repository import BaseRepository

class ReservationRepository(BaseRepository[Reservation]):
    def __init__(self):
        super().__init__("reservations")

    def create(self, reservation: Reservation) -> Reservation:
        cursor = self._get_cursor()
        cursor.execute(
            """
            INSERT INTO reservations (
                customer_id, room_type, number_of_guests,
                number_of_days, total_value, status,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reservation.customer_id,
                reservation.room_type,
                reservation.number_of_guests,
                reservation.number_of_days,
                reservation.total_value,
                reservation.status.value,
                datetime.now(),
                datetime.now()
            )
        )
        self._commit()
        reservation.id = cursor.lastrowid
        return reservation

    def find_by_id(self, id: int) -> Optional[Reservation]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM reservations WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._map_row_to_entity(row) if row else None

    def find_by_customer_id(self, customer_id: int) -> List[Reservation]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM reservations WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def update_status(self, id: int, status: ReservationStatus) -> Optional[Reservation]:
        cursor = self._get_cursor()
        cursor.execute(
            "UPDATE reservations SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, datetime.now(), id)
        )
        self._commit()
        return self.find_by_id(id)

    def _map_row_to_entity(self, row) -> Reservation:
        return Reservation(
            id=row[0],
            customer_id=row[1],
            room_type=row[2],
            number_of_guests=row[3],
            number_of_days=row[4],
            total_value=row[5],
            status=ReservationStatus(row[6]),
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        ) 