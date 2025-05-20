from typing import Optional, List
from core.domain.entities.reservation import Reservation, ReservationStatus
from core.domain.entities.room import RoomType
from core.presentation.controllers.reservation_controller import ReservationController
from datetime import datetime, timedelta


class ReservationView:
    def __init__(self, reservation_controller: ReservationController):
        self._reservation_controller = reservation_controller

    def print_header(self, title: str):
        print("\n\033[1;36m" + "=" * 60)
        print(" " * 15 + title + " " * 15)
        print("=" * 60 + "\033[m")

    def get_valid_input(self, prompt: str, validator=None) -> str:
        while True:
            value = input(f"\033[1;37m{prompt}\033[m").strip()
            if not value:
                print("\033[1;31mEste campo é obrigatório!\033[m")
                continue
            if validator and not validator(value):
                print("\033[1;31mValor inválido! Tente novamente.\033[m")
                continue
            return value

    def get_valid_date(self, prompt: str, min_date: Optional[datetime] = None) -> datetime:
        while True:
            date_str = self.get_valid_input(prompt)
            try:
                # Converte a string para data
                date = datetime.strptime(date_str, "%d/%m/%Y")
                
                # Obtém a data atual (sem hora)
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                
                # Compara apenas as datas (sem hora)
                if date.date() < today.date():
                    print("\033[1;31mNão é possível fazer reservas para datas passadas!\033[m")
                    continue
                    
                if min_date and date.date() <= min_date.date():
                    print("\033[1;31mA data de saída deve ser posterior à data de entrada!\033[m")
                    continue
                    
                return date
            except ValueError:
                print("\033[1;31mData inválida! Use o formato DD/MM/AAAA.\033[m")

    def get_valid_room_type(self) -> RoomType:
        print("\n\033[1;37mTipos de quarto disponíveis:\033[m")
        print("\033[1;37m1 - Standard (R$ 100,00/dia)")
        print("2 - Deluxe (R$ 200,00/dia)")
        print("3 - Premium (R$ 300,00/dia)\033[m")

        while True:
            option = self.get_valid_input("\nEscolha o tipo de quarto (1-3): ")
            if option == "1":
                return RoomType.STANDARD
            elif option == "2":
                return RoomType.DELUXE
            elif option == "3":
                return RoomType.PREMIUM
            print("\033[1;31mOpção inválida! Escolha 1, 2 ou 3.\033[m")

    def get_valid_number(self, prompt: str, min_value: int = 1) -> int:
        while True:
            try:
                value = int(self.get_valid_input(prompt))
                if value < min_value:
                    print(f"\033[1;31mO valor deve ser maior ou igual a {min_value}!\033[m")
                    continue
                return value
            except ValueError:
                print("\033[1;31mPor favor, digite um número válido!\033[m")

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
        self.print_header("LISTA DE RESERVAS")
        
        try:
            reservations = self._reservation_controller.list_reservations()
            if not reservations:
                print("\n\033[1;33mNenhuma reserva encontrada.\033[m")
                return

            print("\n\033[1;37mReservas encontradas:\033[m")
            for reservation in reservations:
                customer = next(
                    (
                        cus
                        for cus in self._reservation_controller.list_customers()
                        if cus.id == reservation.customer_id
                    ),
                    None,
                )
                customer_name = customer.name if customer else "Cliente não encontrado"

                print(f"\n\033[1;37mID: {reservation.id}")
                print(f"Cliente: {customer_name}")
                print(f"Quarto: {reservation.room_type}")
                print(f"Número de hóspedes: {reservation.number_of_guests}")
                print(f"Número de dias: {reservation.number_of_days}")
                print(f"Status: {reservation.status.name}")
                print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

        except Exception as e:
            print(f"\n\033[1;31mErro ao listar reservas: {str(e)}\033[m")

    def create_reservation(self):
        self.print_header("NOVA RESERVA")
        
        try:
            # Lista clientes para seleção
            customers = self._reservation_controller.list_customers()
            if not customers:
                print("\n\033[1;33mNenhum cliente cadastrado. Cadastre um cliente primeiro.\033[m")
                return

            print("\n\033[1;37mSelecione o cliente:\033[m")
            for customer in customers:
                print(f"\n\033[1;37mID: {customer.id}")
                print(f"Nome: {customer.name}")
                print(f"CPF: {customer.cpf}\033[m")

            customer_id = int(self.get_valid_input("\nDigite o ID do cliente: "))
            
            # Seleciona tipo de quarto
            room_type = self.get_valid_room_type()
            
            # Número de hóspedes
            number_of_guests = self.get_valid_number("Número de hóspedes: ")
            
            # Data de entrada e saída
            check_in = self.get_valid_date("Data de entrada (DD/MM/AAAA): ")
            check_out = self.get_valid_date("Data de saída (DD/MM/AAAA): ", min_date=check_in)

            # Calcula o número de dias
            number_of_days = (check_out - check_in).days

            # Cria a reserva
            reservation = self._reservation_controller.create_reservation(
                customer_id=customer_id,
                room_type=room_type,
                number_of_guests=number_of_guests,
                number_of_days=number_of_days
            )

            print(f"\n\033[1;32mReserva criada com sucesso!\033[m")
            print(f"\n\033[1;37mDados da reserva:")
            print(f"ID: {reservation.id}")
            print(f"Cliente: {reservation.customer.name}")
            print(f"Quarto: {reservation.room.type.name}")
            print(f"Número de hóspedes: {number_of_guests}")
            print(f"Check-in: {check_in.strftime('%d/%m/%Y')}")
            print(f"Check-out: {check_out.strftime('%d/%m/%Y')}")
            print(f"Número de dias: {number_of_days}")
            print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

        except ValueError as e:
            print(f"\n\033[1;31mErro ao criar reserva: {str(e)}\033[m")
        except Exception as e:
            print(f"\n\033[1;31mErro inesperado: {str(e)}\033[m")

    def update_reservation(self):
        self.print_header("ATUALIZAR RESERVA")
        
        try:
            # Lista reservas para seleção
            reservations = self._reservation_controller.list_reservations()
            if not reservations:
                print("\n\033[1;33mNenhuma reserva encontrada.\033[m")
                return

            print("\n\033[1;37mSelecione a reserva para atualizar:\033[m")
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

                print(f"\n\033[1;37mID: {reservation.id}")
                print(f"Cliente: {customer_name}")
                print(f"Quarto: {reservation.room_type}")
                print(f"Número de hóspedes: {reservation.number_of_guests}")
                print(f"Número de dias: {reservation.number_of_days}")
                print(f"Status: {reservation.status.name}")
                print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

            reservation_id = int(self.get_valid_input("\nDigite o ID da reserva: "))
            
            # Seleciona novo tipo de quarto
            room_type = self.get_valid_room_type()
            
            # Número de hóspedes
            number_of_guests = self.get_valid_number("Novo número de hóspedes: ")
            
            # Novas datas
            check_in = self.get_valid_date("Nova data de entrada (DD/MM/AAAA): ")
            check_out = self.get_valid_date("Nova data de saída (DD/MM/AAAA): ", min_date=check_in)

            # Calcula o número de dias
            number_of_days = (check_out - check_in).days

            # Atualiza a reserva
            reservation = self._reservation_controller.update_reservation(
                reservation_id=reservation_id,
                room_type=room_type,
                number_of_guests=number_of_guests,
                number_of_days=number_of_days
            )

            print(f"\n\033[1;32mReserva atualizada com sucesso!\033[m")
            print(f"\n\033[1;37mDados atualizados:")
            print(f"ID: {reservation.id}")
            print(f"Cliente: {reservation.customer.name}")
            print(f"Quarto: {reservation.room.type.name}")
            print(f"Número de hóspedes: {number_of_guests}")
            print(f"Número de dias: {number_of_days}")
            print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

        except ValueError as e:
            print(f"\n\033[1;31mErro ao atualizar reserva: {str(e)}\033[m")
        except Exception as e:
            print(f"\n\033[1;31mErro inesperado: {str(e)}\033[m")

    def checkin_reservation(self):
        self.print_header("CHECK-IN")
        
        try:
            # Lista reservas pendentes
            reservations = self._reservation_controller.list_reservations()
            if not reservations:
                print("\n\033[1;33mNenhuma reserva encontrada.\033[m")
                return

            print("\n\033[1;37mReservas pendentes:\033[m")
            for reservation in reservations:
                if reservation.status.name == "PENDING":
                    customer = next(
                        (
                            c
                            for c in self._reservation_controller.list_customers()
                            if c.id == reservation.customer_id
                        ),
                        None,
                    )
                    customer_name = customer.name if customer else "Cliente não encontrado"

                    print(f"\n\033[1;37mID: {reservation.id}")
                    print(f"Cliente: {customer_name}")
                    print(f"Quarto: {reservation.room_type}")
                    print(f"Número de dias: {reservation.number_of_days}")
                    print(f"Status: {reservation.status.name}")
                    print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

            reservation_id = int(self.get_valid_input("\nDigite o ID da reserva para check-in: "))
            
            # Realiza o check-in
            reservation = self._reservation_controller.checkin_reservation(reservation_id)

            print(f"\n\033[1;32mCheck-in realizado com sucesso!\033[m")
            print(f"\n\033[1;37mDados da reserva:")
            print(f"ID: {reservation.id}")
            print(f"Cliente: {reservation.customer.name}")
            print(f"Quarto: {reservation.room.type.name}")
            print(f"Número de dias: {reservation.number_of_days}")
            print(f"Status: {reservation.status.name}")
            print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

        except ValueError as e:
            print(f"\n\033[1;31mErro ao realizar check-in: {str(e)}\033[m")
        except Exception as e:
            print(f"\n\033[1;31mErro inesperado: {str(e)}\033[m")

    def checkout_reservation(self):
        self.print_header("CHECK-OUT")
        
        try:
            # Lista reservas em andamento
            reservations = self._reservation_controller.list_reservations()
            if not reservations:
                print("\n\033[1;33mNenhuma reserva encontrada.\033[m")
                return

            print("\n\033[1;37mReservas em andamento:\033[m")
            for reservation in reservations:
                if reservation.status.name == "CHECKED_IN":
                    customer = next(
                        (
                            cus
                            for cus in self._reservation_controller.list_customers()
                            if cus.id == reservation.customer_id
                        ),
                        None,
                    )
                    customer_name = customer.name if customer else "Cliente não encontrado"

                    print(f"\n\033[1;37mID: {reservation.id}")
                    print(f"Cliente: {customer_name}")
                    print(f"Quarto: {reservation.room_type}")
                    print(f"Número de hóspedes: {reservation.number_of_guests}")
                    print(f"Número de dias: {reservation.number_of_days}")
                    print(f"Status: {reservation.status.name}")
                    print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

            reservation_id = int(self.get_valid_input("\nDigite o ID da reserva para check-out: "))
            
            # Realiza o check-out
            reservation = self._reservation_controller.checkout_reservation(reservation_id)

            # Busca o cliente para exibição
            customer = next(
                (
                    cus
                    for cus in self._reservation_controller.list_customers()
                    if cus.id == reservation.customer_id
                ),
                None,
            )
            customer_name = customer.name if customer else "Cliente não encontrado"

            print(f"\n\033[1;32mCheck-out realizado com sucesso!\033[m")
            print(f"\n\033[1;37mDados da reserva:")
            print(f"ID: {reservation.id}")
            print(f"Cliente: {customer_name}")
            print(f"Quarto: {reservation.room_type}")
            print(f"Número de hóspedes: {reservation.number_of_guests}")
            print(f"Número de dias: {reservation.number_of_days}")
            print(f"Status: {reservation.status.name}")
            print(f"Valor total: R$ {reservation.total_value:.2f}\033[m")

        except ValueError as e:
            print(f"\n\033[1;31mErro ao realizar check-out: {str(e)}\033[m")
        except Exception as e:
            print(f"\n\033[1;31mErro inesperado: {str(e)}\033[m")

    def _show_room_types(self):
        print("\nTipos de quarto disponíveis:")
        rooms = self._reservation_controller.list_rooms()
        for room in rooms:
            print(f"{room.type.value} - R$ {room.daily_rate:.2f} por dia")
