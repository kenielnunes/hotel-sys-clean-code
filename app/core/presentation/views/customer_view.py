from typing import Optional
from core.presentation.controllers.customer_controller import CustomerController
from utils.cpf_validator import cpf_validator


class CustomerView:
    def __init__(self, customer_controller: CustomerController):
        self._customer_controller = customer_controller

    def print_header(self, title: str):
        print("\n\033[1;36m" + "=" * 60)
        print(" " * 15 + title + " " * 15)
        print("=" * 60 + "\033[m")

    def get_valid_input(self, prompt: str, validator=None) -> str:
        while True:
            value = input(f"\033[1;37m{prompt}\033[m").strip()
            if not value:
                print("\033[1;31mEste campo é obrigatório!\033[m")
                continue
            if validator and not validator(value):
                print("\033[1;31mValor inválido! Tente novamente.\033[m")
                continue
            return value

    def create_customer(self):
        self.print_header("CADASTRO DE CLIENTE")
        
        name = self.get_valid_input("Nome do cliente: ")
        cpf = self.get_valid_input("CPF do cliente: ", cpf_validator)

        try:
            customer = self._customer_controller.create_customer(name, cpf)
            print(f"\n\033[1;32mCliente cadastrado com sucesso!\033[m")
            print(f"\n\033[1;37mDados do cliente:")
            print(f"ID: {customer.id}")
            print(f"Nome: {customer.name}")
            print(f"CPF: {customer.cpf}")
            print(f"Data de cadastro: {customer.created_at.strftime('%d/%m/%Y %H:%M:%S')}\033[m")
        except ValueError as e:
            print(f"\n\033[1;31mErro ao cadastrar cliente: {str(e)}\033[m")
        except Exception as e:
            print(f"\n\033[1;31mErro inesperado: {str(e)}\033[m")

    def list_customers(self):
        self.print_header("LISTA DE CLIENTES")
        
        try:
            customers = self._customer_controller.list_customers()
            if not customers:
                print("\n\033[1;33mNenhum cliente cadastrado.\033[m")
                return

            print("\n\033[1;37mClientes cadastrados:\033[m")
            for customer in customers:
                print(f"\n\033[1;37mID: {customer.id}")
                print(f"Nome: {customer.name}")
                print(f"CPF: {customer.cpf}")
                print(f"Data de cadastro: {customer.created_at.strftime('%d/%m/%Y %H:%M:%S')}\033[m")
        except Exception as e:
            print(f"\n\033[1;31mErro ao listar clientes: {str(e)}\033[m")
