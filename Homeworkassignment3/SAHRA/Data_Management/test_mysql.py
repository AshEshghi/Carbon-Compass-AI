
import mysql.connector
from getpass import getpass

password = getpass("MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="carbon_compass"
)

cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM consumption_records")

count = cursor.fetchone()[0]

print("MySQL connection successful!")
print("Total records:", count)

cursor.close()
connection.close()
