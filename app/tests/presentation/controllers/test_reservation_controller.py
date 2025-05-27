import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from core.presentation.controllers.reservation_controller import ReservationController
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.domain.entities.customer import Customer
from core.domain.entities.room import Room, RoomType


class TestReservationController:
    @pytest.fixture
    def reservation_controller(self):
        return ReservationController()

    @pytest.fixture
    def mock_customer(self):
        return Customer(
            id=1,
            name="Test Customer",
            cpf="123.456.789-00",
            created_at=datetime.now()
        )

    @pytest.fixture
    def mock_room(self):
        return Room(
            id=1,
            type=RoomType.STANDARD,
            daily_rate=100.00,
            created_at=datetime.now()
        )

    @pytest.fixture
    def mock_reservation(self, mock_customer, mock_room):
        return Reservation(
            id=1,
            customer_id=mock_customer.id,
            room_type=mock_room.type.value,
            number_of_guests=2,
            number_of_days=3,
            total_value=600.00,
            status=ReservationStatus.RESERVED,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def test_create_reservation_success(self, reservation_controller, mock_reservation):
        with patch.object(
            reservation_controller._create_reservation_use_case,
            'execute',
            return_value=mock_reservation
        ):
            result = reservation_controller.create_reservation(
                customer_id=1,
                room_type="STANDARD",
                number_of_guests=2,
                number_of_days=3
            )

            assert result == mock_reservation
            assert result.id == mock_reservation.id
            assert result.customer_id == mock_reservation.customer_id
            assert result.room_type == mock_reservation.room_type
            assert result.number_of_guests == mock_reservation.number_of_guests
            assert result.number_of_days == mock_reservation.number_of_days
            assert result.total_value == mock_reservation.total_value
            assert result.status == mock_reservation.status

    def test_create_reservation_error(self, reservation_controller):
        with patch.object(
            reservation_controller._create_reservation_use_case,
            'execute',
            side_effect=ValueError("Cliente não encontrado")
        ):
            with pytest.raises(ValueError) as exc_info:
                reservation_controller.create_reservation(
                    customer_id=999,
                    room_type="STANDARD",
                    number_of_guests=2,
                    number_of_days=3
                )
            assert str(exc_info.value) == "Cliente não encontrado"

    def test_update_reservation_success(self, reservation_controller, mock_reservation):
        with patch.object(
            reservation_controller._update_reservation_use_case,
            'with_reservation',
            return_value=reservation_controller._update_reservation_use_case
        ) as mock_with_reservation, \
        patch.object(
            reservation_controller._update_reservation_use_case,
            'update_room_type',
            return_value=reservation_controller._update_reservation_use_case
        ) as mock_update_room_type, \
        patch.object(
            reservation_controller._update_reservation_use_case,
            'update_number_of_guests',
            return_value=reservation_controller._update_reservation_use_case
        ) as mock_update_guests, \
        patch.object(
            reservation_controller._update_reservation_use_case,
            'update_number_of_days',
            return_value=reservation_controller._update_reservation_use_case
        ) as mock_update_days, \
        patch.object(
            reservation_controller._update_reservation_use_case,
            'save',
            return_value=mock_reservation
        ) as mock_save:
            result = reservation_controller.update_reservation(
                reservation_id=1,
                room_type="DELUXE",
                number_of_guests=3,
                number_of_days=4
            )

            assert result == mock_reservation
            mock_with_reservation.assert_called_once_with(1)
            mock_update_room_type.assert_called_once_with("DELUXE")
            mock_update_guests.assert_called_once_with(3)
            mock_update_days.assert_called_once_with(4)
            mock_save.assert_called_once()

    def test_update_reservation_error(self, reservation_controller):
        with patch.object(
            reservation_controller._update_reservation_use_case,
            'with_reservation',
            side_effect=ValueError("Reserva não encontrada")
        ):
            with pytest.raises(ValueError) as exc_info:
                reservation_controller.update_reservation(
                    reservation_id=999,
                    room_type="DELUXE"
                )
            assert str(exc_info.value) == "Reserva não encontrada"

    def test_list_reservations_success(self, reservation_controller, mock_reservation):
        mock_reservations = [mock_reservation]
        with patch.object(
            reservation_controller._list_reservations_use_case,
            'execute',
            return_value=mock_reservations
        ):
            result = reservation_controller.list_reservations()

            assert result == mock_reservations
            assert len(result) == 1
            assert result[0].id == mock_reservation.id

    def test_list_reservations_by_status_success(self, reservation_controller, mock_reservation):
        mock_reservations = [mock_reservation]
        with patch.object(
            reservation_controller._list_reservations_by_status_use_case,
            'execute',
            return_value=mock_reservations
        ):
            result = reservation_controller.list_reservations_by_status(ReservationStatus.RESERVED)

            assert result == mock_reservations
            assert len(result) == 1
            assert result[0].status == ReservationStatus.RESERVED

    def test_checkin_reservation_success(self, reservation_controller, mock_reservation):
        mock_reservation.status = ReservationStatus.CHECKED_IN
        with patch.object(
            reservation_controller._checkin_reservation_use_case,
            'execute',
            return_value=mock_reservation
        ):
            result = reservation_controller.checkin_reservation(1)

            assert result == mock_reservation
            assert result.status == ReservationStatus.CHECKED_IN

    def test_checkout_reservation_success(self, reservation_controller, mock_reservation):
        mock_reservation.status = ReservationStatus.CHECKED_OUT
        with patch.object(
            reservation_controller._checkout_reservation_use_case,
            'execute',
            return_value=mock_reservation
        ):
            result = reservation_controller.checkout_reservation(1)

            assert result == mock_reservation
            assert result.status == ReservationStatus.CHECKED_OUT

    def test_list_customers_success(self, reservation_controller, mock_customer):
        mock_customers = [mock_customer]
        with patch.object(
            reservation_controller._list_customers_use_case,
            'execute',
            return_value=mock_customers
        ):
            result = reservation_controller.list_customers()

            assert result == mock_customers
            assert len(result) == 1
            assert result[0].id == mock_customer.id

    def test_list_rooms_success(self, reservation_controller, mock_room):
        mock_rooms = [mock_room]
        with patch.object(
            reservation_controller._list_rooms_use_case,
            'execute',
            return_value=mock_rooms
        ):
            result = reservation_controller.list_rooms()

            assert result == mock_rooms
            assert len(result) == 1
            assert result[0].id == mock_room.id 