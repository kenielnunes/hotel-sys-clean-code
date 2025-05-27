from typing import Optional
from datetime import datetime
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.domain.entities.room import RoomType
from core.infra.repositories.reservation_repository import ReservationRepository
from core.infra.repositories.room_repository import RoomRepository


class UpdateReservationUseCase:
    def __init__(
        self,
        reservation_repository: ReservationRepository,
        room_repository: RoomRepository,
    ):
        self._reservation_repository = reservation_repository
        self._room_repository = room_repository
        self._reservation: Optional[Reservation] = None
        self._reservation_id: Optional[int] = None

    def with_reservation(self, reservation_id: int) -> 'UpdateReservationUseCase':
        self._reservation_id = reservation_id
        self._reservation = self._reservation_repository.find_by_id(reservation_id)
        if not self._reservation:
            raise ValueError("Reserva não encontrada")
        return self

    def update_room_type(self, room_type: str) -> 'UpdateReservationUseCase':
        if not self._reservation:
            raise ValueError("Reserva não inicializada. Use with_reservation() primeiro.")
        
        # Converte para string se for um enum RoomType
        if isinstance(room_type, RoomType):
            room_type = room_type.value
        
        room = self._room_repository.find_by_type(room_type)
        if not room:
            raise ValueError("Tipo de quarto inválido")
        
        self._reservation.room_type = room_type
        return self

    def update_number_of_guests(self, number_of_guests: int) -> 'UpdateReservationUseCase':
        if not self._reservation:
            raise ValueError("Reserva não inicializada. Use with_reservation() primeiro.")
        
        if number_of_guests <= 0:
            raise ValueError("Número de hóspedes deve ser maior que zero")
        
        self._reservation.number_of_guests = number_of_guests
        return self

    def update_number_of_days(self, number_of_days: int) -> 'UpdateReservationUseCase':
        if not self._reservation:
            raise ValueError("Reserva não inicializada. Use with_reservation() primeiro.")
        
        if number_of_days <= 0:
            raise ValueError("Número de dias deve ser maior que zero")
        
        self._reservation.number_of_days = number_of_days
        return self

    def _recalculate_total_value(self) -> None:
        if not self._reservation:
            return
        
        room = self._room_repository.find_by_type(self._reservation.room_type)
        daily_rate = float(room.daily_rate)
        guests = int(self._reservation.number_of_guests)
        days = int(self._reservation.number_of_days)
        self._reservation.total_value = daily_rate * guests * days

    def save(self) -> Reservation:
        if not self._reservation:
            raise ValueError("Reserva não inicializada. Use with_reservation() primeiro.")
        
        self._recalculate_total_value()
        self._reservation.updated_at = datetime.now()
        return self._reservation_repository.update(self._reservation)
