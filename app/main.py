from core.infra.config.database import create_tables
from core.presentation.controllers.customer_controller import CustomerController
from core.presentation.controllers.reservation_controller import ReservationController
from core.presentation.views.customer_view import CustomerView
from core.presentation.views.reservation_view import ReservationView


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

    while True:
        print_header("SISTEMA DE HOTEL")
        
        print("\n\033[1;33mGerenciamento de Clientes\033[m")
        print_menu_option(1, "Cadastrar Cliente")
        print_menu_option(2, "Listar Clientes")
        
        print("\n\033[1;33mGerenciamento de Reservas\033[m")
        print_menu_option(3, "Nova Reserva")
        print_menu_option(4, "Listar Reservas")
        print_menu_option(5, "Atualizar Reserva")
        
        print("\n\033[1;33mOperações de Check-in/Check-out\033[m")
        print_menu_option(6, "Realizar Check-in")
        print_menu_option(7, "Realizar Check-out")
        
        print("\n\033[1;31m" + "=" * 60)
        print_menu_option(0, "Sair do Sistema")
        print("=" * 60 + "\033[m")

        try:
            option = int(input("\n\033[1;37mEscolha uma opção: \033[m"))

            if option == 1:
                customer_view.create_customer()
            elif option == 2:
                customer_view.list_customers()
            elif option == 3:
                reservation_view.create_reservation()
            elif option == 4:
                reservation_view.list_reservations()
            elif option == 5:
                reservation_view.update_reservation()
            elif option == 6:
                reservation_view.checkin_reservation()
            elif option == 7:
                reservation_view.checkout_reservation()
            elif option == 0:
                print("\n\033[1;32mObrigado por usar o Sistema de Hotel!\033[m")
                break
            else:
                print("\n\033[1;31mOpção inválida! Por favor, escolha uma opção válida.\033[m")
        except ValueError:
            print("\n\033[1;31mPor favor, digite um número válido!\033[m")


if __name__ == "__main__":
    main()
