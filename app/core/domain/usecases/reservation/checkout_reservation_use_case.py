from core.domain.entities.reservation import Reservation, ReservationStatus
from core.infra.repositories.reservation_repository import ReservationRepository


class CheckoutReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self._reservation_repository = reservation_repository

    def execute(self, reservation_id: int) -> Reservation:
        reservation = self._reservation_repository.find_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reserva não encontrada")

        if reservation.status != ReservationStatus.CHECKED_IN:
            raise ValueError(
                "Apenas reservas com check-in realizado podem fazer check-out"
            )

        reservation.status = ReservationStatus.CHECKED_OUT

        return self._reservation_repository.update(reservation)
