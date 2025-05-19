from typing import Optional
from core.presentation.controllers.reservation_controller import ReservationController

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
            print(f"{i} - Nome: {customer['name']}, CPF: {customer['cpf']}")

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

    def create_reservation(self):
        details = self.get_reservation_details()
        if not details:
            return

        reservation = self._controller.create_reservation(
            customer_id=details["customer_id"],
            room_type=details["room_type"],
            number_of_guests=details["number_of_guests"],
            number_of_days=details["number_of_days"]
        )

        if reservation:
            print("\n\033[0;32mReserva criada com sucesso!\033[m")
            print(f"Valor total: R$ {reservation.total_value:.2f}")
        else:
            print("\n\033[0;31mErro ao criar reserva!\033[m") 