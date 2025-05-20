from core.domain.usecases.customer.create_customer_use_case import CreateCustomerUseCase
from core.domain.usecases.customer.list_customers_use_case import ListCustomersUseCase
from core.infra.repositories.customer_repository import CustomerRepository
from core.presentation.types.customer_types import (
    CustomerRequest,
    CustomerSingleResponse,
    CustomerErrorResponse,
)

class CustomerController:
    def __init__(self):
        self._customer_repository = CustomerRepository()
        self._create_customer_use_case = CreateCustomerUseCase(self._customer_repository)
        self._list_customers_use_case = ListCustomersUseCase(self._customer_repository)

    def create(self, request: CustomerRequest) -> CustomerSingleResponse | CustomerErrorResponse:
        try:
            # Create customer
            customer = self._create_customer_use_case.execute(
                name=request['name'],
                cpf=request['cpf']
            )

            return {
                'status_code': 201,
                'body': {
                    'id': customer.id,
                    'name': customer.name,
                    'cpf': customer.cpf
                }
            }

        except ValueError as e:
            return {
                'status_code': 400,
                'body': {'error': str(e)}
            }
        except Exception as e:
            return {
                'status_code': 500,
                'body': {'error': 'Internal server error'}
            }

    def create_customer(self, name: str, cpf: str):
        try:
            customer = self._create_customer_use_case.execute(name, cpf)
            return customer
        except Exception as e:
            raise

    def list_customers(self):
        try:
            customers = self._list_customers_use_case.execute()
            return customers
        except Exception as e:
            raise