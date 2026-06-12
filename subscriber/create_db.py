import sqlite3
from pathlib import Path


# Database will be created inside the subscriber folder.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sensor_data.db"


def create_database():
    """
    Creates the SQLite database and sensor_data table if it does not exist.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT,
            message_no INTEGER,
            temperature REAL,
            humidity REAL,
            uptime_seconds INTEGER,
            mqtt_topic TEXT,
            received_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print(f"Database ready at: {DB_PATH}")


if __name__ == "__main__":
    create_database()