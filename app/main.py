from core.infra.config.database import create_tables
from core.presentation.controllers.customer_controller import CustomerController
from core.presentation.controllers.reservation_controller import ReservationController
from core.presentation.views.customer_view import CustomerView
from core.presentation.views.reservation_view import ReservationView

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
        print("\n=== Sistema de Hotel ===")
        print("\nGerenciamento de Clientes")
        print("   1 - Cadastrar Cliente")
        print("   2 - Listar Clientes")
        print("\nGerenciamento de Reservas")
        print("   3 - Nova Reserva")
        print("   4 - Listar Reservas")
        print("   5 - Atualizar Reserva")
        print("\nOperações de Check-in/Check-out")
        print("   6 - Realizar Check-in")
        print("   7 - Realizar Check-out")
        print("\n0 - Sair")
        
        try:
            option = int(input("\nEscolha uma opção: "))
            
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
                print("\n\033[0;32mObrigado por usar!\033[m")
                break
            else:
                print("\n\033[0;31mOpção inválida!\033[m")
        except ValueError:
            print("\n\033[0;31mPor favor, digite um número válido!\033[m")

if __name__ == "__main__":
    main() 