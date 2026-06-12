import sqlite3
import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sensor_data.db"

CSV_PATH = BASE_DIR / "sensor_data_output.csv"
MD_PATH = BASE_DIR / "sensor_data_table.md"


def export_data():
    """
    Exports sensor_data table to:
    1. CSV file for Excel/GitHub
    2. Markdown table for README.md
    """

    if not DB_PATH.exists():
        print("Database not found:", DB_PATH)
        print("Run subscriber.py first to collect data.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, device, message_no, temperature, humidity, uptime_seconds, mqtt_topic, received_at
        FROM sensor_data
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    conn.close()

    if not rows:
        print("No data found to export.")
        return

    # Export to CSV.
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(column_names)
        writer.writerows(rows)

    print(f"Successfully saved CSV file to: {CSV_PATH}")

    # Export to Markdown table.
    with open(MD_PATH, "w", encoding="utf-8") as md_file:
        md_file.write("| " + " | ".join(column_names) + " |\n")
        md_file.write("| " + " | ".join(["---"] * len(column_names)) + " |\n")

        for row in rows:
            clean_row = [str(item) if item is not None else "" for item in row]
            md_file.write("| " + " | ".join(clean_row) + " |\n")

    print(f"Successfully saved Markdown table to: {MD_PATH}")


if __name__ == "__main__":
    export_data()
    