from typing import Optional
from core.domain.entities.reservation import Reservation
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
        room = self._room_repository.find_by_type(room_type)
        if not room:
            raise ValueError("Tipo de quarto inválido")

        # Cria a reserva
        reservation = Reservation(
            customer_id=customer_id,
            room_type=room_type,
            number_of_guests=number_of_guests,
            number_of_days=number_of_days
        )

        # Calcula o valor total
        reservation.calculate_total_value(room.daily_rate)

        # Salva a reserva
        return self._reservation_repository.create(reservation) 