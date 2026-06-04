import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sensor.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC")

rows = cursor.fetchall()

if not rows:
    print("No data found.")
else:
    for row in rows:
        print(row)

conn.close()