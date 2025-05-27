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
        """Inicializa o caso de uso com uma reserva existente."""
        self._reservation_id = reservation_id
        self._reservation = self._reservation_repository.find_by_id(reservation_id)
        if not self._reservation:
            raise ValueError("Reserva não encontrada")
        return self

    def update_room_type(self, room_type: str) -> 'UpdateReservationUseCase':
        self._validate_reservation_initialized()
        room_type = self._normalize_room_type(room_type)
        self._validate_room_type(room_type)
        
        self._update_reservation(room_type=room_type)
        return self

    def update_number_of_guests(self, number_of_guests: int) -> 'UpdateReservationUseCase':
        self._validate_reservation_initialized()
        self._validate_positive_number(number_of_guests, "Número de hóspedes")
        
        self._update_reservation(number_of_guests=number_of_guests)
        return self

    def update_number_of_days(self, number_of_days: int) -> 'UpdateReservationUseCase':
        """Atualiza o número de dias da reserva."""
        self._validate_reservation_initialized()
        self._validate_positive_number(number_of_days, "Número de dias")
        
        self._update_reservation(number_of_days=number_of_days)
        return self

    def save(self) -> Reservation:
        """Salva as alterações da reserva."""
        self._validate_reservation_initialized()
        self._recalculate_total_value()
        return self._reservation_repository.update(self._reservation)

    def _validate_reservation_initialized(self) -> None:
        """Valida se a reserva foi inicializada."""
        if not self._reservation:
            raise ValueError("Reserva não inicializada. Use with_reservation() primeiro.")

    def _normalize_room_type(self, room_type: str) -> str:
        """Normaliza o tipo de quarto para o formato esperado."""
        if isinstance(room_type, RoomType):
            return room_type.value
        return room_type.upper()

    def _validate_room_type(self, room_type: str) -> None:
        """Valida se o tipo de quarto existe."""
        room = self._room_repository.find_by_type(room_type)
        if not room:
            raise ValueError("Tipo de quarto inválido")

    def _validate_positive_number(self, number: int, field_name: str) -> None:
        if number <= 0:
            raise ValueError(f"{field_name} deve ser maior que zero")

    def _update_reservation(self, **kwargs) -> None:
        self._reservation = self._create_updated_reservation(**kwargs)

    def _create_updated_reservation(self, **kwargs) -> Reservation:
        """Cria uma nova instância da reserva com os valores atualizados."""
        return Reservation.create()\
            .with_id(self._reservation.id)\
            .with_customer_id(self._reservation.customer_id)\
            .with_room_type(kwargs.get('room_type', self._reservation.room_type))\
            .with_number_of_guests(kwargs.get('number_of_guests', self._reservation.number_of_guests))\
            .with_number_of_days(kwargs.get('number_of_days', self._reservation.number_of_days))\
            .with_status(self._reservation.status)\
            .with_created_at(self._reservation.created_at)\
            .with_updated_at(datetime.now())\
            .build()

    def _recalculate_total_value(self) -> None:
        if not self._reservation:
            return
        
        room = self._room_repository.find_by_type(self._reservation.room_type)
        total_value = self._calculate_total_value(
            daily_rate=float(room.daily_rate),
            guests=int(self._reservation.number_of_guests),
            days=int(self._reservation.number_of_days)
        )
        
        self._update_reservation(total_value=total_value)

    def _calculate_total_value(self, daily_rate: float, guests: int, days: int) -> float:
        return daily_rate * guests * days
