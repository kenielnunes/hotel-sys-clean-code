from core.domain.usecases.customer.create_customer_use_case import CreateCustomerUseCase
from core.infra.repositories.customer_repository import CustomerRepository
from core.presentation.types.customer_types import (
    CustomerRequest,
    CustomerSingleResponse,
    CustomerErrorResponse,
)

class CustomerController:
    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.create_customer_use_case = CreateCustomerUseCase(self.customer_repository)

    def create(self, request: CustomerRequest) -> CustomerSingleResponse | CustomerErrorResponse:
        try:
            # Create customer
            customer = self.create_customer_use_case.execute(
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