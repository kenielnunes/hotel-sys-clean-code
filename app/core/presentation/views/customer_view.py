from typing import Optional
from core.presentation.controllers.customer_controller import CustomerController
from utils.cpf_validator import cpf_validator

class CustomerView:
    def __init__(self, controller: CustomerController):
        self._controller = controller

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
        print("\n=== Cadastro de Cliente ===")
        
        name = input("\nNome do cliente: ")
        if not name:
            print("\n\033[0;31mNome é obrigatório!\033[m")
            return

        cpf = input("CPF do cliente: ")
        if not cpf:
            print("\n\033[0;31mCPF é obrigatório!\033[m")
            return

        try:
            customer = self._controller.create_customer(name=name, cpf=cpf)
            print(f"\n\033[0;32mCliente cadastrado com sucesso! ID: {customer.id}\033[m")
        except ValueError as e:
            print(f"\n\033[0;31mErro: {str(e)}\033[m") 