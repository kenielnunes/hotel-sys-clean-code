from typing import Optional
from core.domain.entities.reservation import Reservation
from core.domain.usecases.reservation.create_reservation_use_case import CreateReservationUseCase
from core.domain.usecases.customer.list_customers_use_case import ListCustomersUseCase
from core.domain.usecases.room.list_rooms_use_case import ListRoomsUseCase

class ReservationController:
    def __init__(
        self,
        create_reservation_use_case: CreateReservationUseCase,
        list_customers_use_case: ListCustomersUseCase,
        list_rooms_use_case: ListRoomsUseCase
    ):
        self._create_reservation_use_case = create_reservation_use_case
        self._list_customers_use_case = list_customers_use_case
        self._list_rooms_use_case = list_rooms_use_case

    def list_customers(self):
        return self._list_customers_use_case.execute()

    def list_rooms(self):
        return self._list_rooms_use_case.execute()

    def create_reservation(
        self,
        customer_id: int,
        room_type: str,
        number_of_guests: int,
        number_of_days: int
    ) -> Optional[Reservation]:
        try:
            return self._create_reservation_use_case.execute(
                customer_id=customer_id,
                room_type=room_type,
                number_of_guests=number_of_guests,
                number_of_days=number_of_days
            )
        except ValueError as e:
            print(f"\033[0;31mErro: {str(e)}\033[m")
            return None 