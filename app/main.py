from utils.cpf_validator import cpf_validator
from core.infra.config.database import create_tables
from core.infra.repositories.customer_repository import CustomerRepository
from core.infra.repositories.room_repository import RoomRepository
from core.infra.repositories.reservation_repository import ReservationRepository
from core.domain.usecases.reservation.create_reservation import CreateReservationUseCase
from core.domain.usecases.customer.list_customers import ListCustomersUseCase
from core.domain.usecases.room.list_rooms import ListRoomsUseCase
from core.presentation.controllers.customer_controller import CustomerController
from core.presentation.controllers.reservation_controller import ReservationController
from core.presentation.views.customer_view import CustomerView
from core.presentation.views.reservation_view import ReservationView

def main():
    # Create database tables
    create_tables()
    
    # Inicializa os repositórios
    customer_repository = CustomerRepository()
    room_repository = RoomRepository()
    reservation_repository = ReservationRepository()

    # Inicializa os use cases
    create_reservation_use_case = CreateReservationUseCase(
        reservation_repository=reservation_repository,
        customer_repository=customer_repository,
        room_repository=room_repository
    )
    list_customers_use_case = ListCustomersUseCase(customer_repository)
    list_rooms_use_case = ListRoomsUseCase(room_repository)

    # Inicializa os controladores
    customer_controller = CustomerController()
    reservation_controller = ReservationController(
        create_reservation_use_case=create_reservation_use_case,
        list_customers_use_case=list_customers_use_case,
        list_rooms_use_case=list_rooms_use_case
    )

    # Inicializa as views
    customer_view = CustomerView(customer_controller)
    reservation_view = ReservationView(reservation_controller)

    while True:
        print("\n=== Sistema de Hotel ===")
        print("1 - Cadastrar Cliente")
        print("2 - Nova Reserva")
        print("3 - Sair")
        
        try:
            opcao = int(input("\nEscolha uma opção: "))
            
            if opcao == 1:
                customer_view.create_customer()
            elif opcao == 2:
                reservation_view.create_reservation()
            elif opcao == 3:
                print("\n\033[0;32mObrigado por usar o sistema!\033[m")
                break
            else:
                print("\n\033[0;31mOpção inválida!\033[m")
        except ValueError:
            print("\n\033[0;31mPor favor, digite um número válido!\033[m")

if __name__ == "__main__":
    main() 