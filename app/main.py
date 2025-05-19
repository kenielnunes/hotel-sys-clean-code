from utils.cpf_validator import cpf_validator
from core.presentation.controllers.customer_controller import CustomerController
from core.infra.config.database import create_tables

def get_valid_input(prompt: str, validator=None) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("\033[91mEste campo é obrigatório!\033[0m")
            continue
        if validator and not validator(value):
            print("\033[91mValor inválido! Tente novamente.\033[0m")
            continue
        return value

def register_customer():
    print("\n=== Cadastro de Cliente ===")
    
    # Get customer name
    name = get_valid_input("Nome do cliente: ")
    
    # Get and validate CPF
    cpf = get_valid_input(
        "CPF do cliente (apenas números ou com formatação): ",
        validator=cpf_validator
    )
    
    # Create customer using controller
    controller = CustomerController()
    response = controller.create({
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

def main():
    # Create database tables
    create_tables()
    
    while True:
        print("\n=== Sistema de Hotel ===")
        print("1. Cadastrar Cliente")
        print("2. Sair")
        
        option = input("\nEscolha uma opção: ")
        
        if option == "1":
            register_customer()
        elif option == "2":
            print("\nSaindo do sistema...")
            break
        else:
            print("\n\033[91mOpção inválida! Tente novamente.\033[0m")

if __name__ == "__main__":
    main() 