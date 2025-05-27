from datetime import datetime
from dataclasses import dataclass


@dataclass
class Customer:
    id: int = None
    name: str = None
    cpf: str = None
    created_at: datetime = None

    def __post_init__(self):
        if self.name and not self.name.strip():
            raise ValueError("Name is required")
        if self.cpf and not self.cpf.strip():
            raise ValueError("CPF is required")

    @classmethod
    def create(cls) -> 'Customer':
        return cls()

    def with_id(self, id: int) -> 'Customer':
        self.id = id
        return self

    def with_name(self, name: str) -> 'Customer':
        self.name = name
        return self

    def with_cpf(self, cpf: str) -> 'Customer':
        self.cpf = cpf
        return self

    def with_created_at(self, created_at: datetime) -> 'Customer':
        self.created_at = created_at
        return self

    def build(self) -> 'Customer':
        if not self.name:
            raise ValueError("Name is required")
        if not self.cpf:
            raise ValueError("CPF is required")
        if not self.created_at:
            self.created_at = datetime.now()
        return self
