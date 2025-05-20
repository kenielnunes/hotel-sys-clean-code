from typing import Optional
from datetime import datetime
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.infra.repositories.reservation_repository import ReservationRepository
from core.infra.repositories.room_repository import RoomRepository

class UpdateReservationUseCase:
    def __init__(
        self,
        reservation_repository: ReservationRepository,
        room_repository: RoomRepository
    ):
        self._reservation_repository = reservation_repository
        self._room_repository = room_repository

    def execute(
        self,
        reservation_id: int,
        room_type: Optional[str] = None,
        number_of_guests: Optional[int] = None,
        number_of_days: Optional[int] = None
    ) -> Optional[Reservation]:
        # Busca a reserva existente
        reservation = self._reservation_repository.find_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reserva não encontrada")

        # Atualiza os campos se fornecidos
        if room_type:
            # Valida se o tipo de quarto existe
            room = self._room_repository.find_by_type(room_type)
            if not room:
                raise ValueError("Tipo de quarto inválido")
            reservation.room_type = room_type

        if number_of_guests:
            if number_of_guests <= 0:
                raise ValueError("Número de hóspedes deve ser maior que zero")
            reservation.number_of_guests = number_of_guests

        if number_of_days:
            if number_of_days <= 0:
                raise ValueError("Número de dias deve ser maior que zero")
            reservation.number_of_days = number_of_days

        # Recalcula o valor total
        room = self._room_repository.find_by_type(reservation.room_type)
        daily_rate = float(room.daily_rate)
        guests = int(reservation.number_of_guests)
        days = int(reservation.number_of_days)
        reservation.total_value = daily_rate * guests * days

        return self._reservation_repository.update(reservation) 