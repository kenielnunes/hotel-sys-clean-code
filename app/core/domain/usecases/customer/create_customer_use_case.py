from typing import Optional
from core.domain.entities.customer import Customer
from core.infra.repositories.customer_repository import CustomerRepository
from utils.cpf_validator import cpf_validator

class CreateCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def execute(self, name: str, cpf: str) -> Optional[Customer]:
        # Validate CPF
        if not cpf_validator(cpf):
            raise ValueError("Invalid CPF")

        existing_customer = self.customer_repository.find_by_cpf(cpf)
        
        if existing_customer:
            raise ValueError("Customer with this CPF already exists")

        customer = Customer(name=name, cpf=cpf)
        return self.customer_repository.create(customer) 