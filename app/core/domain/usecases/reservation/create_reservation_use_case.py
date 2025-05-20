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
        room_repository: RoomRepository
    ):
        self._reservation_repository = reservation_repository
        self._customer_repository = customer_repository
        self._room_repository = room_repository

    def execute(
        self,
        customer_id: int,
        room_type: str,
        number_of_guests: int,
        number_of_days: int
    ) -> Optional[Reservation]:
        # Verifica se o cliente existe
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError("Cliente não encontrado")

        # Verifica se o tipo de quarto é válido
        room_type = room_type.upper()
        if room_type not in [t.value for t in RoomType]:
            raise ValueError("Tipo de quarto inválido")

        # Calcula o valor total
        daily_rate = Room.get_daily_rate(room_type)
        print(f"Daily rate for {room_type}: R$ {daily_rate:.2f}")
        total_value = daily_rate * number_of_guests * number_of_days
        print(f"Total value: R$ {total_value:.2f} ({daily_rate} * {number_of_guests} * {number_of_days})")

        reservation = Reservation(
            id=None,  # Será definido pelo banco de dados
            customer_id=customer_id,
            room_type=room_type,
            number_of_guests=number_of_guests,
            number_of_days=number_of_days,
            total_value=total_value,
            status=ReservationStatus.RESERVED,  # Status inicial
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        saved_reservation = self._reservation_repository.create(reservation)
        print(f"Saved reservation total value: R$ {saved_reservation.total_value:.2f}")
        return saved_reservation 