import sqlite3
from sqlite3 import Connection
from datetime import datetime
from pathlib import Path
from core.domain.entities.room import RoomType


def get_connection() -> Connection:
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.parent.parent.parent
    db_path = root_dir / "hotel.db"
    return sqlite3.connect(str(db_path))


def create_tables() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # Create customers table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
    """
    )

    # Create rooms table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            daily_rate REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """
    )

    # Create reservations table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            room_type TEXT NOT NULL,
            number_of_guests INTEGER NOT NULL,
            number_of_days INTEGER NOT NULL,
            total_value REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    """
    )

    # Insert default room types if they don't exist
    print("Inserting default room types...")
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO rooms (type, daily_rate, created_at) VALUES (?, ?, ?)",
            [
                (RoomType.STANDARD.value, 100.0, datetime.now().isoformat()),
                (RoomType.DELUXE.value, 200.0, datetime.now().isoformat()),
                (RoomType.PREMIUM.value, 300.0, datetime.now().isoformat()),
            ],
        )

    conn.commit()
    conn.close()
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
