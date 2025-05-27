from typing import Optional
from datetime import datetime
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.domain.entities.room import Room, RoomType
from core.infra.repositories.reservation_repository import ReservationRepository
from core.infra.repositories.customer_repository import CustomerRepository
from core.infra.repositories.room_repository import RoomRepository


class CreateReservationUseCase:
    def __init__(
        self,
        reservation_repository: ReservationRepository,
        customer_repository: CustomerRepository,
        room_repository: RoomRepository,
    ):
        self._reservation_repository = reservation_repository
        self._customer_repository = customer_repository
        self._room_repository = room_repository

    def execute(
        self,
        customer_id: int,
        room_type: str,
        number_of_guests: int,
        number_of_days: int,
    ) -> Optional[Reservation]:
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError("Cliente não encontrado")

        room_type = room_type.upper()
        if room_type not in [t.value for t in RoomType]:
            raise ValueError("Tipo de quarto inválido")

        # Calcula o valor total
        daily_rate = Room.get_daily_rate(room_type)
        print(f"Daily rate for {room_type}: R$ {daily_rate:.2f}")
        total_value = daily_rate * number_of_guests * number_of_days
        print(
            f"Total value: R$ {total_value:.2f} ({daily_rate} * {number_of_guests} * {number_of_days})"
        )

        reservation = Reservation.create()\
            .with_customer_id(customer_id)\
            .with_room_type(room_type)\
            .with_number_of_guests(number_of_guests)\
            .with_number_of_days(number_of_days)\
            .with_total_value(total_value)\
            .with_status(ReservationStatus.RESERVED)\
            .with_created_at(datetime.now())\
            .with_updated_at(datetime.now())\
            .build()

        saved_reservation = self._reservation_repository.create(reservation)
        print(f"Saved reservation total value: R$ {saved_reservation.total_value:.2f}")
        return saved_reservation
