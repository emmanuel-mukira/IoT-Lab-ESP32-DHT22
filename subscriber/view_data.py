import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sensor_data.db"


def view_data():
    """
    Displays all sensor records from newest to oldest.
    """

    if not DB_PATH.exists():
        print("Database not found:", DB_PATH)
        print("Run create_db.py or subscriber.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, device, message_no, temperature, humidity, uptime_seconds, mqtt_topic, received_at
        FROM sensor_data
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No data found.")
        return

    print("Saved sensor data:")
    print("-" * 100)

    for row in rows:
        print(row)


if __name__ == "__main__":
    view_data()