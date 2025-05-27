from core.infra.config.database import create_tables
from core.presentation.controllers.customer_controller import CustomerController
from core.presentation.controllers.reservation_controller import ReservationController
from core.presentation.views.customer_view import CustomerView
from core.presentation.views.reservation_view import ReservationView
from typing import Dict, Callable


class MenuOption:
    def __init__(self, text: str, action: Callable[[], None]):
        self.text = text
        self.action = action


class HotelSystemMenu:
    def __init__(self, customer_view: CustomerView, reservation_view: ReservationView):
        self.customer_view = customer_view
        self.reservation_view = reservation_view
        self.options: Dict[int, MenuOption] = self._initialize_options()

    def _initialize_options(self) -> Dict[int, MenuOption]:
        return {
            1: MenuOption("Cadastrar Cliente", self.customer_view.create_customer),
            2: MenuOption("Listar Clientes", self.customer_view.list_customers),
            3: MenuOption("Nova Reserva", self.reservation_view.create_reservation),
            4: MenuOption("Listar Reservas", self.reservation_view.list_reservations),
            5: MenuOption("Atualizar Reserva", self.reservation_view.update_reservation),
            6: MenuOption("Realizar Check-in", self.reservation_view.checkin_reservation),
            7: MenuOption("Realizar Check-out", self.reservation_view.checkout_reservation),
            0: MenuOption("Sair do Sistema", lambda: None)
        }

    def display_menu(self) -> None:
        print_header("SISTEMA DE HOTEL")
        
        print("\n\033[1;33mGerenciamento de Clientes\033[m")
        print_menu_option(1, self.options[1].text)
        print_menu_option(2, self.options[2].text)
        
        print("\n\033[1;33mGerenciamento de Reservas\033[m")
        print_menu_option(3, self.options[3].text)
        print_menu_option(4, self.options[4].text)
        print_menu_option(5, self.options[5].text)
        
        print("\n\033[1;33mOperações de Check-in/Check-out\033[m")
        print_menu_option(6, self.options[6].text)
        print_menu_option(7, self.options[7].text)
        
        print("\n\033[1;31m" + "=" * 60)
        print_menu_option(0, self.options[0].text)
        print("=" * 60 + "\033[m")

    def handle_option(self, option: int) -> bool:
        if option not in self.options:
            print("\n\033[1;31mOpção inválida! Por favor, escolha uma opção válida.\033[m")
            return True

        if option == 0:
            print("\n\033[1;32mObrigado por usar o Sistema de Hotel!\033[m")
            return False

        self.options[option].action()
        return True


def print_header(title: str):
    print("\n\033[1;36m" + "=" * 60)
    print(" " * 15 + title + " " * 15)
    print("=" * 60 + "\033[m")


def print_menu_option(number: int, text: str):
    print(f"\033[1;37m[{number}]\033[m {text}")


def main():
    # Create database tables
    create_tables()

    # Inicializa os controladores
    customer_controller = CustomerController()
    reservation_controller = ReservationController()

    # Inicializa as views
    customer_view = CustomerView(customer_controller)
    reservation_view = ReservationView(reservation_controller)

    menu = HotelSystemMenu(customer_view, reservation_view)

    while True:
        menu.display_menu()
        
        try:
            option = int(input("\n\033[1;37mEscolha uma opção: \033[m"))
            if not menu.handle_option(option):
                break
        except ValueError:
            print("\n\033[1;31mPor favor, digite um número válido!\033[m")


if __name__ == "__main__":
    main()
