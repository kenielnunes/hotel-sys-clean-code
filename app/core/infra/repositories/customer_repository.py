from typing import Optional, List
from datetime import datetime
from core.domain.entities.customer import Customer
from .base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self):
        super().__init__("customers")

    def create(self, customer: Customer) -> Customer:
        cursor = self._get_cursor()
        try:
            cursor.execute(
                "INSERT INTO customers (name, cpf, created_at) VALUES (?, ?, ?)",
                (customer.name, customer.cpf, customer.created_at.isoformat())
            )
            self._commit()
            customer.id = cursor.lastrowid
            return customer
        except Exception as e:
            raise

    def update(self, customer: Customer) -> Customer:
        cursor = self._get_cursor()
        cursor.execute(
            "UPDATE customers SET name = ?, cpf = ? WHERE id = ?",
            (customer.name, customer.cpf, customer.id)
        )
        self._commit()
        return customer

    def find_by_cpf(self, cpf: str) -> Optional[Customer]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM customers WHERE cpf = ?", (cpf,))
        row = cursor.fetchone()
        return self._map_row_to_entity(row) if row else None

    def find_all(self) -> List[Customer]:
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM customers ORDER BY name")
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def _map_row_to_entity(self, row) -> Customer:
        if not row:
            return None
        try:
            return Customer(
                id=row[0],
                name=row[1],
                cpf=row[2],
                created_at=datetime.fromisoformat(row[3])
            )
        except Exception as e:
            raise 