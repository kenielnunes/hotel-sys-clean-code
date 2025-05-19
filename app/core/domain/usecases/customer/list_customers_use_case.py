from typing import List, Dict

from core.infra.repositories.customer_repository import CustomerRepository

class ListCustomersUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    def execute(self) -> List[Dict]:
        customers = self._customer_repository.find_all()
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "cpf": customer.cpf
            }
            for customer in customers
        ] 