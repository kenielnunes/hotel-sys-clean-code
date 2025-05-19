from typing import TypeVar, Generic, List, Optional
from sqlite3 import Connection
from core.infra.config.database import get_connection

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn: Connection = get_connection()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def _get_cursor(self):
        return self.conn.cursor()

    def _commit(self):
        self.conn.commit()

    def find_by_id(self, id: int) -> Optional[T]:
        cursor = self._get_cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._map_row_to_entity(row) if row else None

    def find_all(self) -> List[T]:
        cursor = self._get_cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        return [self._map_row_to_entity(row) for row in rows]

    def delete(self, id: int) -> bool:
        cursor = self._get_cursor()
        cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
        self._commit()
        return cursor.rowcount > 0

    def _map_row_to_entity(self, row) -> T:
        raise NotImplementedError("Subclasses must implement _map_row_to_entity method") 