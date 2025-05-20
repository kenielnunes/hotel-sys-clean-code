from typing import Optional, List
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.domain.entities.room import RoomType
from core.presentation.controllers.reservation_controller import ReservationController


class ReservationView:
    def __init__(self, reservation_controller: ReservationController):
        self._reservation_controller = reservation_controller

    def show_customers(self):
        customers = self._reservation_controller.list_customers()
        if not customers:
            print("\n\033[0;31mNenhum cliente cadastrado!\033[m")
            return None

        print("\n=== Clientes Cadastrados ===")
        for i, customer in enumerate(customers, 1):
            print(f"{i} - Nome: {customer.name}, CPF: {customer.cpf}")

        while True:
            try:
                escolha = int(
                    input("\nSelecione o número do cliente (ou 0 para voltar): ")
                )
                if escolha == 0:
                    return None
                if 1 <= escolha <= len(customers):
                    return customers[escolha - 1]
                print("\033[0;31mOpção inválida!\033[m")
            except ValueError:
                print("\033[0;31mPor favor, digite um número válido!\033[m")

    def show_rooms(self):
        rooms = self._reservation_controller.list_rooms()
        print("\n=== Tipos de Quartos Disponíveis ===")
        for i, room in enumerate(rooms, 1):
            print(f"{i} - {room['description']} (R$ {room['daily_rate']}/dia)")

        while True:
            try:
                room = int(input("\nSelecione o tipo de quarto (ou 0 para voltar): "))
                if room == 0:
                    return None
                if 1 <= room <= len(rooms):
                    return rooms[room - 1]
                print("\033[0;31mOpção inválida!\033[m")
            except ValueError:
                print("\033[0;31mPor favor, digite um número válido!\033[m")

    def get_reservation_details(self):
        print("\n=== Nova Reserva ===")

        # Seleciona cliente
        customer = self.show_customers()
        if not customer:
            return None

        # Seleciona quarto
        room = self.show_rooms()
        if not room:
            return None

        # Número de hóspedes
        while True:
            try:
                number_of_guests = int(input("\nNúmero de hóspedes: "))
                if number_of_guests > 0:
                    break
                print("\033[0;31mO número de hóspedes deve ser maior que zero!\033[m")
            except ValueError:
                print("\033[0;31mPor favor, digite um número válido!\033[m")

        # Número de dias
        while True:
            try:
                number_of_days = int(input("Número de dias: "))
                if number_of_days > 0:
                    break
                print("\033[0;31mO número de dias deve ser maior que zero!\033[m")
            except ValueError:
                print("\033[0;31mPor favor, digite um número válido!\033[m")

        return {
            "customer_id": customer["id"],
            "room_type": room["type"],
            "number_of_guests": number_of_guests,
            "number_of_days": number_of_days,
        }

    def list_reservations(self):
        print("\n=== Lista de Reservas ===")
        reservations = self._reservation_controller.list_reservations()

        if not reservations:
            print("\n\033[0;31mNenhuma reserva encontrada!\033[m")
            return

        for reservation in reservations:
            customer = next(
                (
                    c
                    for c in self._reservation_controller.list_customers()
                    if c.id == reservation.customer_id
                ),
                None,
            )
            customer_name = customer.name if customer else "Cliente não encontrado"

            print(f"\nID: {reservation.id}")
            print(f"Cliente: {customer_name}")
            print(f"Quarto: {reservation.room_type}")
            print(f"Hóspedes: {reservation.number_of_guests}")
            print(f"Dias: {reservation.number_of_days}")
            print(f"Valor Total: R$ {reservation.total_value:.2f}")
            print(f"Status: {reservation.status.value}")
            print(
                f"Data de Criação: {reservation.created_at.strftime('%d/%m/%Y %H:%M')}"
            )

    def create_reservation(self):
        print("\n=== Nova Reserva ===")

        # Lista clientes
        customers = self._reservation_controller.list_customers()
        if not customers:
            print("\n\033[0;31mNenhum cliente cadastrado!\033[m")
            return

        print("\nClientes disponíveis:")
        for customer in customers:
            print(f"{customer.id} - {customer.name} (CPF: {customer.cpf})")

        # Seleciona cliente
        customer_id = int(input("\nSelecione o ID do cliente: "))
        if not any(c.id == customer_id for c in customers):
            print("\n\033[0;31mCliente não encontrado!\033[m")
            return

        # Lista quartos
        rooms = self._reservation_controller.list_rooms()
        if not rooms:
            print("\n\033[0;31mNenhum quarto disponível!\033[m")
            return

        print("\nTipos de quarto disponíveis:")
        for room in rooms:
            print(f"{room.type} - {room.type.value} (R$ {room.daily_rate:.2f}/dia)")

        # Seleciona tipo de quarto
        room_type = input("\nSelecione o tipo de quarto (S/D/P): ").upper()
        if room_type not in ["S", "D", "P"]:
            print("\n\033[0;31mTipo de quarto inválido!\033[m")
            return

        # Número de hóspedes
        number_of_guests = int(input("\nNúmero de hóspedes: "))
        if number_of_guests < 1:
            print("\n\033[0;31mNúmero de hóspedes inválido!\033[m")
            return

        # Número de dias
        number_of_days = int(input("\nNúmero de dias: "))
        if number_of_days < 1:
            print("\n\033[0;31mNúmero de dias inválido!\033[m")
            return

        try:
            reservation = self._reservation_controller.create_reservation(
                customer_id=customer_id,
                room_type=room_type,
                number_of_guests=number_of_guests,
                number_of_days=number_of_days,
            )
            print(f"\n\033[0;32mReserva criada com sucesso! ID: {reservation.id}\033[m")
        except Exception as e:
            print(f"\n\033[0;31mErro ao criar reserva: {str(e)}\033[m")

    def update_reservation(self):
        print("\n=== Atualizar Reserva ===")
        reservations = self._reservation_controller.list_reservations()

        if not reservations:
            print("\n\033[0;31mNenhuma reserva encontrada!\033[m")
            return

        print("\nReservas disponíveis:")
        for reservation in reservations:
            customer = next(
                (
                    c
                    for c in self._reservation_controller.list_customers()
                    if c.id == reservation.customer_id
                ),
                None,
            )
            customer_name = customer.name if customer else "Cliente não encontrado"

            print(f"\nID: {reservation.id}")
            print(f"Cliente: {customer_name}")
            print(f"Quarto: {reservation.room_type}")
            print(f"Status: {reservation.status.value}")

        reservation_id = int(input("\nSelecione o ID da reserva: "))
        if not any(r.id == reservation_id for r in reservations):
            print("\n\033[0;31mReserva não encontrada!\033[m")
            return

        # Lista quartos
        rooms = self._reservation_controller.list_rooms()
        if not rooms:
            print("\n\033[0;31mNenhum quarto disponível!\033[m")
            return

        print("\nTipos de quarto disponíveis:")
        for room in rooms:
            print(f"{room.type} - {room.type.value} (R$ {room.daily_rate:.2f}/dia)")

        # Seleciona tipo de quarto
        room_type = input(
            "\nSelecione o tipo de quarto (S/D/P) ou pressione Enter para manter: "
        ).upper()
        if room_type and room_type not in ["S", "D", "P"]:
            print("\n\033[0;31mTipo de quarto inválido!\033[m")
            return

        # Número de hóspedes
        number_of_guests_str = input(
            "\nNúmero de hóspedes ou pressione Enter para manter: "
        )
        number_of_guests = int(number_of_guests_str) if number_of_guests_str else None
        if number_of_guests is not None and number_of_guests < 1:
            print("\n\033[0;31mNúmero de hóspedes inválido!\033[m")
            return

        # Número de dias
        number_of_days_str = input("\nNúmero de dias ou pressione Enter para manter: ")
        number_of_days = int(number_of_days_str) if number_of_days_str else None
        if number_of_days is not None and number_of_days < 1:
            print("\n\033[0;31mNúmero de dias inválido!\033[m")
            return

        try:
            reservation = self._reservation_controller.update_reservation(
                reservation_id=reservation_id,
                room_type=room_type if room_type else None,
                number_of_guests=number_of_guests,
                number_of_days=number_of_days,
            )
            print(
                f"\n\033[0;32mReserva atualizada com sucesso! ID: {reservation.id}\033[m"
            )
        except Exception as e:
            print(f"\n\033[0;31mErro ao atualizar reserva: {str(e)}\033[m")

    def checkin_reservation(self):
        print("\n=== Realizar Check-in ===")
        # Lista apenas reservas com status RESERVED
        reservations = self._reservation_controller.list_reservations_by_status(
            ReservationStatus.RESERVED
        )

        if not reservations:
            print("\n\033[0;31mNenhuma reserva pendente de check-in!\033[m")
            return

        print("\nReservas pendentes de check-in:")
        for reservation in reservations:
            customer = next(
                (
                    c
                    for c in self._reservation_controller.list_customers()
                    if c.id == reservation.customer_id
                ),
                None,
            )
            customer_name = customer.name if customer else "Cliente não encontrado"

            print(f"\nID: {reservation.id}")
            print(f"Cliente: {customer_name}")
            print(f"Quarto: {reservation.room_type}")
            print(f"Hóspedes: {reservation.number_of_guests}")
            print(f"Dias: {reservation.number_of_days}")
            print(f"Valor Total: R$ {reservation.total_value:.2f}")

        reservation_id = int(input("\nSelecione o ID da reserva para check-in: "))
        if not any(r.id == reservation_id for r in reservations):
            print(
                "\n\033[0;31mReserva não encontrada ou não está pendente de check-in!\033[m"
            )
            return

        try:
            reservation = self._reservation_controller.checkin_reservation(
                reservation_id
            )
            print(
                f"\n\033[0;32mCheck-in realizado com sucesso! ID: {reservation.id}\033[m"
            )
        except Exception as e:
            print(f"\n\033[0;31mErro ao realizar check-in: {str(e)}\033[m")

    def checkout_reservation(self):
        print("\n=== Realizar Check-out ===")
        # Lista apenas reservas com status CHECKED_IN
        reservations = self._reservation_controller.list_reservations_by_status(
            ReservationStatus.CHECKED_IN
        )

        if not reservations:
            print("\n\033[0;31mNenhuma reserva pendente de check-out!\033[m")
            return

        print("\nReservas pendentes de check-out:")
        for reservation in reservations:
            customer = next(
                (
                    c
                    for c in self._reservation_controller.list_customers()
                    if c.id == reservation.customer_id
                ),
                None,
            )
            customer_name = customer.name if customer else "Cliente não encontrado"

            print(f"\nID: {reservation.id}")
            print(f"Cliente: {customer_name}")
            print(f"Quarto: {reservation.room_type}")
            print(f"Hóspedes: {reservation.number_of_guests}")
            print(f"Dias: {reservation.number_of_days}")
            print(f"Valor Total: R$ {reservation.total_value:.2f}")

        reservation_id = int(input("\nSelecione o ID da reserva para check-out: "))
        if not any(r.id == reservation_id for r in reservations):
            print(
                "\n\033[0;31mReserva não encontrada ou não está pendente de check-out!\033[m"
            )
            return

        try:
            reservation = self._reservation_controller.checkout_reservation(
                reservation_id
            )
            print(
                f"\n\033[0;32mCheck-out realizado com sucesso! ID: {reservation.id}\033[m"
            )
        except Exception as e:
            print(f"\n\033[0;31mErro ao realizar check-out: {str(e)}\033[m")

    def _show_room_types(self):
        print("\nTipos de quarto disponíveis:")
        rooms = self._reservation_controller.list_rooms()
        for room in rooms:
            print(f"{room.type.value} - R$ {room.daily_rate:.2f} por dia")
