from typing import List, Optional
from core.domain.entities.customer import Customer
from core.domain.entities.room import Room
from core.domain.entities.reservation import Reservation
from core.domain.usecases.reservation.create_reservation_use_case import CreateReservationUseCase
from core.domain.usecases.reservation.update_reservation_use_case import UpdateReservationUseCase
from core.domain.usecases.reservation.list_reservations_use_case import ListReservationsUseCase
from core.domain.usecases.reservation.checkin_reservation_use_case import CheckinReservationUseCase
from core.domain.usecases.reservation.checkout_reservation_use_case import CheckoutReservationUseCase
from core.domain.usecases.customer.list_customers_use_case import ListCustomersUseCase
from core.domain.usecases.room.list_rooms_use_case import ListRoomsUseCase
from core.infra.repositories.reservation_repository import ReservationRepository
from core.infra.repositories.customer_repository import CustomerRepository
from core.infra.repositories.room_repository import RoomRepository

class ReservationController:
    def __init__(self):
        # Inicializa os repositórios
        self._reservation_repository = ReservationRepository()
        self._customer_repository = CustomerRepository()
        self._room_repository = RoomRepository()

        # Inicializa os casos de uso
        self._create_reservation_use_case = CreateReservationUseCase(
            self._reservation_repository,
            self._customer_repository,
            self._room_repository
        )
        self._update_reservation_use_case = UpdateReservationUseCase(
            self._reservation_repository,
            self._room_repository
        )
        self._list_reservations_use_case = ListReservationsUseCase(self._reservation_repository)
        self._checkin_reservation_use_case = CheckinReservationUseCase(self._reservation_repository)
        self._checkout_reservation_use_case = CheckoutReservationUseCase(self._reservation_repository)
        self._list_customers_use_case = ListCustomersUseCase(self._customer_repository)
        self._list_rooms_use_case = ListRoomsUseCase(self._room_repository)

    def create_reservation(
        self,
        customer_id: int,
        room_type: str,
        number_of_guests: int,
        number_of_days: int
    ) -> Reservation:
        return self._create_reservation_use_case.execute(
            customer_id=customer_id,
            room_type=room_type,
            number_of_guests=number_of_guests,
            number_of_days=number_of_days
        )

    def update_reservation(
        self,
        reservation_id: int,
        room_type: Optional[str] = None,
        number_of_guests: Optional[int] = None,
        number_of_days: Optional[int] = None
    ) -> Optional[Reservation]:
        return self._update_reservation_use_case.execute(
            reservation_id=reservation_id,
            room_type=room_type,
            number_of_guests=number_of_guests,
            number_of_days=number_of_days
        )

    def list_reservations(self) -> List[Reservation]:
        return self._list_reservations_use_case.execute()

    def checkin_reservation(self, reservation_id: int):
        return self._checkin_reservation_use_case.execute(reservation_id)

    def checkout_reservation(self, reservation_id: int):
        return self._checkout_reservation_use_case.execute(reservation_id)

    def list_customers(self) -> List[Customer]:
        return self._list_customers_use_case.execute()

    def list_rooms(self) -> List[Room]:
        return self._list_rooms_use_case.execute() 