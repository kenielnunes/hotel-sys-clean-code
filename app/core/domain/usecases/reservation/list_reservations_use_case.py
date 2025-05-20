from typing import List
from core.domain.entities.reservation import Reservation
from core.infra.repositories.reservation_repository import ReservationRepository

class ListReservationsUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self._reservation_repository = reservation_repository

    def execute(self) -> List[Reservation]:
        return self._reservation_repository.find_all() 