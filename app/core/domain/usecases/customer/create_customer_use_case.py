from datetime import datetime
from core.domain.entities.customer import Customer
from core.infra.repositories.customer_repository import CustomerRepository
from utils.cpf_validator import cpf_validator


class CreateCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    def execute(self, name: str, cpf: str) -> Customer:
        if not cpf_validator(cpf):
            raise ValueError("CPF inválido")

        existing_customer = self._customer_repository.find_by_cpf(cpf)

        if existing_customer:
            raise ValueError("CPF já cadastrado")

        customer = Customer(id=None, name=name, cpf=cpf, created_at=datetime.now())

        try:
            saved_customer = self._customer_repository.create(customer)
            return saved_customer
        except Exception as e:
            raise
