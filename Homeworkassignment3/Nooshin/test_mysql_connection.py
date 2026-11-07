from getpass import getpass
from mysql_database_manager import MySQLDatabaseManager

password = getpass("Enter MySQL root password: ")
database = MySQLDatabaseManager(password)

try:
    records = database.fetch_records()
    print("MySQL connection successful!")
    print("Records:", records)

except Exception as error:
    print("Connection failed:", error)