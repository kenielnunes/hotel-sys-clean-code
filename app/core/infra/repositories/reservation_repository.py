from typing import Optional, List
from datetime import datetime
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.domain.entities.room import RoomType
from .base_repository import BaseRepository

class ReservationRepository(BaseRepository[Reservation]):
    def __init__(self):
        super().__init__("reservations")

    def create(self, reservation: Reservation) -> Reservation:
        cursor = self._get_cursor()
        print(f"Creating reservation with total value: R$ {reservation.total_value:.2f}")
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
                reservation.created_at,
                reservation.updated_at
            )
        )
        self._commit()
        reservation.id = cursor.lastrowid
        print(f"Reservation created with ID {reservation.id} and total value: R$ {reservation.total_value:.2f}")
        return reservation

    def update(self, reservation: Reservation) -> Reservation:
        cursor = self._get_cursor()
        cursor.execute(
            """
            UPDATE reservations SET
                customer_id = ?,
                room_type = ?,
                number_of_guests = ?,
                number_of_days = ?,
                total_value = ?,
                status = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                reservation.customer_id,
                reservation.room_type,
                reservation.number_of_guests,
                reservation.number_of_days,
                reservation.total_value,
                reservation.status.value,
                datetime.now(),
                reservation.id
            )
        )
        self._commit()
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

    def find_all(self) -> List[Reservation]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM reservations ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def find_by_status(self, status: ReservationStatus) -> List[Reservation]:
        cursor = self._get_cursor()
        cursor.execute(
            "SELECT * FROM reservations WHERE status = ? ORDER BY created_at DESC",
            (status.value,)
        )
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
        # Maps room type code to type name
        room_type_map = {
            "S": "Standard",
            "D": "Deluxe",
            "P": "Premium"
        }
        
        # Ensures fields are in the correct order
        reservation = Reservation(
            id=row[0],                    # id
            customer_id=row[1],           # customer_id
            room_type=room_type_map.get(row[2], row[2]),  # room_type
            number_of_guests=row[3],      # number_of_guests
            number_of_days=row[4],        # number_of_days
            total_value=float(row[5]),    # total_value
            status=ReservationStatus(row[6]),  # status
            created_at=datetime.fromisoformat(row[7]),  # created_at
            updated_at=datetime.fromisoformat(row[8]) if row[8] else None   # updated_at
        )
        print(f"Mapped reservation {reservation.id} with total value: R$ {reservation.total_value:.2f}")
        return reservation 