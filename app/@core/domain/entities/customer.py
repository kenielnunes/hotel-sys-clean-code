from dataclasses import dataclass

@dataclass
class Customer:
    id: int = None
    name: str = None
    cpf: str = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name is required")
        if not self.cpf:
            raise ValueError("CPF is required") 