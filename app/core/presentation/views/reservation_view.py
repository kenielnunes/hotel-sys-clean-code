from typing import Optional
from core.domain.entities.reservation import Reservation
from core.presentation.controllers.reservation_controller import ReservationController
from core.domain.entities.reservation import ReservationStatus

class ReservationView:
    def __init__(self, controller: ReservationController):
        self._controller = controller

    def show_customers(self):
        customers = self._controller.list_customers()
        if not customers:
            print("\n\033[0;31mNenhum cliente cadastrado!\033[m")
            return None

        print("\n=== Clientes Cadastrados ===")
        for i, customer in enumerate(customers, 1):
            print(f"{i} - Nome: {customer.name}, CPF: {customer.cpf}")

        while True:
            try:
                escolha = int(input("\nSelecione o número do cliente (ou 0 para voltar): "))
                if escolha == 0:
                    return None
                if 1 <= escolha <= len(customers):
                    return customers[escolha - 1]
                print("\033[0;31mOpção inválida!\033[m")
            except ValueError:
                print("\033[0;31mPor favor, digite um número válido!\033[m")

    def show_rooms(self):
        rooms = self._controller.list_rooms()
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
            "number_of_days": number_of_days
        }

    def list_reservations(self) -> None:
        print("\n=== Lista de Reservas ===")
        
        reservations = self._controller.list_reservations()
        if not reservations:
            print("\n\033[0;31mNenhuma reserva encontrada!\033[m")
            return

        print("\n{:<5} {:<20} {:<10} {:<10} {:<10} {:<15} {:<10}".format(
            "ID", "Cliente", "Quarto", "Hóspedes", "Dias", "Valor Total", "Status"
        ))
        print("-" * 80)

        for reservation in reservations:
            customer = next((c for c in self._controller.list_customers() if c.id == reservation.customer_id), None)
            customer_name = customer.name if customer else "Cliente não encontrado"
            
            # Garante que os campos estejam na ordem correta
            print("{:<5} {:<20} {:<10} {:<10} {:<10} R$ {:<12.2f} {:<10}".format(
                reservation.id,                # ID
                customer_name[:20],           # Cliente
                reservation.room_type,        # Quarto
                reservation.number_of_guests, # Hóspedes
                reservation.number_of_days,   # Dias
                reservation.total_value,      # Valor Total
                reservation.status.value      # Status
            ))

    def create_reservation(self):
        print("\n=== Nova Reserva ===")
        
        # Lista clientes disponíveis
        customers = self._controller.list_customers()
        if not customers:
            print("\nNenhum cliente cadastrado!")
            return

        print("\nClientes disponíveis:")
        for customer in customers:
            print(f"ID: {customer.id} - Nome: {customer.name} - CPF: {customer.cpf}")

        # Seleciona cliente
        customer_id = int(input("\nDigite o ID do cliente: "))

        # Lista quartos disponíveis
        rooms = self._controller.list_rooms()
        print("\nTipos de quarto disponíveis:")
        for room in rooms:
            print(f"Tipo: {room.type.value} - Diária: R$ {room.daily_rate:.2f}")

        # Seleciona tipo de quarto
        room_type = input("\nDigite o tipo do quarto (S/D/P): ").upper()
        while room_type not in ["S", "D", "P"]:
            print("Tipo de quarto inválido!")
            room_type = input("Digite o tipo do quarto (S/D/P): ").upper()

        # Número de hóspedes
        number_of_guests = int(input("\nDigite o número de hóspedes: "))
        while number_of_guests < 1:
            print("Número de hóspedes inválido!")
            number_of_guests = int(input("Digite o número de hóspedes: "))

        # Número de dias
        number_of_days = int(input("\nDigite o número de dias: "))
        while number_of_days < 1:
            print("Número de dias inválido!")
            number_of_days = int(input("Digite o número de dias: "))

        try:
            reservation = self._controller.create_reservation(
                customer_id=customer_id,
                room_type=room_type,
                number_of_guests=number_of_guests,
                number_of_days=number_of_days
            )
            print(f"\nReserva criada com sucesso! ID: {reservation.id}")
        except ValueError as e:
            print(f"\nErro ao criar reserva: {str(e)}")

    def update_reservation(self):
        print("\n=== Atualizar Reserva ===")
        
        # Lista todas as reservas
        reservations = self._controller.list_reservations()
        if not reservations:
            print("\nNenhuma reserva encontrada!")
            return

        print("\nReservas disponíveis:")
        for reservation in reservations:
            # Busca o cliente pelo ID
            customer = next((c for c in self._controller.list_customers() if c.id == reservation.customer_id), None)
            customer_name = customer.name if customer else "Cliente não encontrado"
            
            print(f"ID: {reservation.id} - Cliente: {customer_name} - Quarto: {reservation.room_type} - Status: {reservation.status.value}")

        # Seleciona reserva
        reservation_id = int(input("\nDigite o ID da reserva: "))

        print("\nO que deseja atualizar?")
        print("1 - Tipo de quarto")
        print("2 - Número de hóspedes")
        print("3 - Número de dias")
        
        option = int(input("\nDigite a opção: "))
        
        try:
            if option == 1:
                rooms = self._controller.list_rooms()
                print("\nTipos de quarto disponíveis:")
                for room in rooms:
                    print(f"Tipo: {room.type.value} - Diária: R$ {room.daily_rate:.2f}")
                
                room_type = input("\nDigite o novo tipo de quarto (S/D/P): ").upper()
                while room_type not in ["S", "D", "P"]:
                    print("Tipo de quarto inválido!")
                    room_type = input("Digite o tipo do quarto (S/D/P): ").upper()
                
                reservation = self._controller.update_reservation(
                    reservation_id=reservation_id,
                    room_type=room_type
                )
            elif option == 2:
                number_of_guests = int(input("\nDigite o novo número de hóspedes: "))
                while number_of_guests < 1:
                    print("Número de hóspedes inválido!")
                    number_of_guests = int(input("Digite o número de hóspedes: "))
                
                reservation = self._controller.update_reservation(
                    reservation_id=reservation_id,
                    number_of_guests=number_of_guests
                )
            elif option == 3:
                number_of_days = int(input("\nDigite o novo número de dias: "))
                while number_of_days < 1:
                    print("Número de dias inválido!")
                    number_of_days = int(input("Digite o número de dias: "))
                
                reservation = self._controller.update_reservation(
                    reservation_id=reservation_id,
                    number_of_days=number_of_days
                )
            else:
                print("\nOpção inválida!")
                return

            print(f"\nReserva atualizada com sucesso! ID: {reservation.id}")
        except ValueError as e:
            print(f"\nErro ao atualizar reserva: {str(e)}")

    def checkin_reservation(self):
        print("\n=== Realizar Check-in ===")
        
        # Lista todas as reservas
        reservations = self._controller.list_reservations()
        if not reservations:
            print("\nNenhuma reserva encontrada!")
            return

        print("\nReservas disponíveis:")
        for reservation in reservations:
            # Busca o cliente pelo ID
            customer = next((c for c in self._controller.list_customers() if c.id == reservation.customer_id), None)
            customer_name = customer.name if customer else "Cliente não encontrado"
            
            print(f"ID: {reservation.id} - Cliente: {customer_name} - Quarto: {reservation.room_type} - Status: {reservation.status.value}")

        # Seleciona reserva
        reservation_id = int(input("\nDigite o ID da reserva para check-in: "))
        
        try:
            reservation = self._controller.checkin_reservation(reservation_id)
            print("\nCheck-in realizado com sucesso!")
        except ValueError as e:
            print(f"\nErro ao realizar check-in: {str(e)}")

    def checkout_reservation(self):
        print("\n=== Realizar Check-out ===")
        
        # Lista todas as reservas
        reservations = self._controller.list_reservations()
        if not reservations:
            print("\nNenhuma reserva encontrada!")
            return

        print("\nReservas disponíveis:")
        for reservation in reservations:
            # Busca o cliente pelo ID
            customer = next((c for c in self._controller.list_customers() if c.id == reservation.customer_id), None)
            customer_name = customer.name if customer else "Cliente não encontrado"
            
            print(f"ID: {reservation.id} - Cliente: {customer_name} - Quarto: {reservation.room_type} - Status: {reservation.status.value}")

        # Seleciona reserva
        reservation_id = int(input("\nDigite o ID da reserva para check-out: "))
        
        try:
            reservation = self._controller.checkout_reservation(reservation_id)
            print("\nCheck-out realizado com sucesso!")
        except ValueError as e:
            print(f"\nErro ao realizar check-out: {str(e)}")

    def _show_room_types(self):
        print("\nTipos de quarto disponíveis:")
        rooms = self._controller.list_rooms()
        for room in rooms:
            print(f"{room.type.value} - R$ {room.daily_rate:.2f} por dia") 