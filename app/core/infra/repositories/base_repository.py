from typing import TypeVar, Generic, List, Optional
from sqlite3 import Connection, Cursor
from core.infra.config.database import get_connection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, table_name: str):
        self._table_name = table_name
        self._connection = None

    def _get_connection(self):
        if not self._connection:
            self._connection = get_connection()
        return self._connection

    def _get_cursor(self):
        return self._get_connection().cursor()

    def _commit(self):
        try:
            self._get_connection().commit()
        except Exception as e:
            raise

    def _rollback(self):
        try:
            self._get_connection().rollback()
        except Exception as e:
            raise

    def find_by_id(self, id: int) -> Optional[T]:
        cursor = self._get_cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._map_row_to_entity(row) if row else None

    def find_all(self) -> List[T]:
        cursor = self._get_cursor()
        cursor.execute(f"SELECT * FROM {self._table_name}")
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def delete(self, id: int) -> bool:
        cursor = self._get_cursor()
        cursor.execute(f"DELETE FROM {self._table_name} WHERE id = ?", (id,))
        self._commit()
        return cursor.rowcount > 0

    def _map_row_to_entity(self, row) -> T:
        raise NotImplementedError("Subclasses must implement _map_row_to_entity method")
