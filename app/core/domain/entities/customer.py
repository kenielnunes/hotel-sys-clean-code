from datetime import datetime
from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    name: str
    cpf: str
    created_at: datetime

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name is required")
        if not self.cpf:
            raise ValueError("CPF is required")
