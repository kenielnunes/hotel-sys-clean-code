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
        
        # Get customer name
        name = self.get_valid_input("Nome do cliente: ")
        
        # Get and validate CPF
        cpf = self.get_valid_input(
            "CPF do cliente (apenas números ou com formatação): ",
            validator=cpf_validator
        )
        
        # Create customer using controller
        response = self._controller.create({
            'name': name,
            'cpf': cpf
        })
        
        if response['status_code'] == 201:
            print("\n\033[92mCliente cadastrado com sucesso!\033[0m")
            print(f"ID: {response['body']['id']}")
            print(f"Nome: {response['body']['name']}")
            print(f"CPF: {response['body']['cpf']}")
        else:
            print(f"\n\033[91mErro ao cadastrar cliente: {response['body']['error']}\033[0m") 