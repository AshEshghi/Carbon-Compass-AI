
import sqlite3
import mysql.connector
from getpass import getpass
from pathlib import Path

# Read records from SQLite
db_path = Path(__file__).parent / "carbon_compass.db"
sqlite_db = sqlite3.connect(db_path)
records = sqlite_db.execute(
    "SELECT building_id, timestamp, electricity_kwh FROM consumption_records"
).fetchall()

# Connect to MySQL
password = getpass("MySQL password: ")
mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="carbon_compass"
)

cursor = mysql_db.cursor()
added = 0

for building_id, timestamp, kwh in records:
    # Check for existing records
    cursor.execute(
        """SELECT COUNT(*) FROM consumption_records
           WHERE building_id = %s
           AND timestamp = %s
           AND electricity_kwh = %s""",
        (building_id, timestamp, kwh)
    )

    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """INSERT INTO consumption_records
               (building_id, timestamp, electricity_kwh)
               VALUES (%s, %s, %s)""",
            (building_id, timestamp, kwh)
        )
        added += 1

mysql_db.commit()

print("SQLite records:", len(records))
print("New MySQL records:", added)
print("Migration completed!")

cursor.close()
mysql_db.close()
sqlite_db.close()

