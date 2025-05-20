from typing import List
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.infra.repositories.reservation_repository import ReservationRepository


class ListReservationsByStatusUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self._reservation_repository = reservation_repository

    def execute(self, status: ReservationStatus) -> List[Reservation]:
        return self._reservation_repository.find_by_status(status)
