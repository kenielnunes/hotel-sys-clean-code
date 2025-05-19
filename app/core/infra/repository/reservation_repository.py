from typing import Optional, List
from datetime import datetime
from core.domain.entities.reservation import Reservation
from core.domain.entities.reservation_status import ReservationStatus
from core.domain.entities.room import RoomType
from .base_repository import BaseRepository
from .customer_repository import CustomerRepository

class ReservationRepository(BaseRepository[Reservation]):
    def __init__(self):
        super().__init__("reservations")
        self.customer_repository = CustomerRepository()

    def create(self, reservation: Reservation) -> Reservation:
        cursor = self._get_cursor()
        cursor.execute(
            """
            INSERT INTO reservations 
            (customer_id, number_of_guests, room_type, number_of_days, total_price, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                reservation.customer.id,
                reservation.number_of_guests,
                reservation.room_type.value,
                reservation.number_of_days,
                reservation.total_price,
                reservation.status.value
            )
        )
        self._commit()
        reservation.id = cursor.lastrowid
        return reservation

    def update(self, reservation: Reservation) -> Reservation:
        cursor = self._get_cursor()
        cursor.execute(
            """
            UPDATE reservations 
            SET customer_id = ?, number_of_guests = ?, room_type = ?, 
                number_of_days = ?, total_price = ?, status = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                reservation.customer.id,
                reservation.number_of_guests,
                reservation.room_type.value,
                reservation.number_of_days,
                reservation.total_price,
                reservation.status.value,
                datetime.now(),
                reservation.id
            )
        )
        self._commit()
        return reservation

    def find_by_customer_id(self, customer_id: int) -> List[Reservation]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM reservations WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def find_by_status(self, status: ReservationStatus) -> List[Reservation]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM reservations WHERE status = ?", (status.value,))
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def _map_row_to_entity(self, row) -> Reservation:
        customer = self.customer_repository.find_by_id(row[1])
        return Reservation(
            id=row[0],
            customer=customer,
            number_of_guests=row[2],
            room_type=RoomType(row[3]),
            number_of_days=row[4],
            total_price=row[5],
            status=ReservationStatus(row[6]),
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        ) 