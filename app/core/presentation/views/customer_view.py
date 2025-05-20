from typing import Optional
from core.presentation.controllers.customer_controller import CustomerController
from utils.cpf_validator import cpf_validator


class CustomerView:
    def __init__(self, customer_controller: CustomerController):
        self._customer_controller = customer_controller

    def get_valid_input(self, prompt: str, validator=None) -> str:
        while True:
            value = input(prompt).strip()
            if not value:
                print("\033[91mEste campo é obrigatório!\033[0m")
                continue
            if validator and not validator(value):
                print("\033[91mValor inválido! Tente novamente.\033[0m")
                continue
            return value

    def create_customer(self):
        print("\n=== Cadastrar Cliente ===")

        name = input("\nNome do cliente: ")
        if not name:
            print("\n\033[0;31mNome é obrigatório!\033[m")
            return

        cpf = input("CPF do cliente: ")
        if not cpf:
            print("\n\033[0;31mCPF é obrigatório!\033[m")
            return

        try:
            customer = self._customer_controller.create_customer(name, cpf)
            print(
                f"\n\033[0;32mCliente cadastrado com sucesso! ID: {customer.id}\033[m"
            )
        except ValueError as e:
            print(f"\n\033[0;31mErro ao cadastrar cliente: {str(e)}\033[m")

    def list_customers(self):
        print("\n=== Lista de Clientes ===")
        customers = self._customer_controller.list_customers()

        if not customers:
            print("\n\033[0;31mNenhum cliente cadastrado!\033[m")
            return

        for customer in customers:
            print(f"\nID: {customer.id}")
            print(f"Nome: {customer.name}")
            print(f"CPF: {customer.cpf}")
            print(f"Data de Cadastro: {customer.created_at.strftime('%d/%m/%Y %H:%M')}")
