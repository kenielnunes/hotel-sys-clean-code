from typing import List
from core.domain.entities.customer import Customer
from core.infra.repositories.customer_repository import CustomerRepository

class ListCustomersUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    def execute(self) -> List[Customer]:
        return self._customer_repository.find_all() 