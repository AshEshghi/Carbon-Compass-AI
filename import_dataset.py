
import csv
import mysql.connector
from getpass import getpass

# Read the main CSV dataset
with open(
    "carbon_compass_real_daily_building1.csv",
    newline="",
    encoding="utf-8"
) as file:
    rows = list(csv.DictReader(file))

# Connect to MySQL
password = getpass("MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="carbon_compass"
)

cursor = connection.cursor()

# Insert the 2016 records
sql = """
    INSERT INTO consumption_records
    (building_id, timestamp, electricity_kwh)
    VALUES (%s, %s, %s)
"""

values = [
    (1, row["timestamp"], float(row["electricity_kwh"]))
    for row in rows
]

cursor.executemany(sql, values)
connection.commit()

print("Inserted records:", cursor.rowcount)

cursor.close()
connection.close()
