import sqlite3
from sqlite3 import Connection
from datetime import datetime


def get_connection() -> Connection:
    conn = sqlite3.connect("hotel.db")
    return conn


def create_tables() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            daily_rate REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create reservations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            number_of_guests INTEGER NOT NULL,
            room_type TEXT NOT NULL,
            number_of_days INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    """)

    # Insert default room types if they don't exist
    cursor.execute("""
        INSERT OR IGNORE INTO rooms (type, daily_rate) VALUES
        ('S', 100.0),
        ('D', 200.0),
        ('P', 300.0)
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
