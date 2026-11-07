
import mysql.connector


class MySQLDatabaseManager:

    def __init__(self, password):
        self.connection_config = {
            "host": "localhost",
            "user": "root",
            "password": password,
            "database": "carbon_compass"
        }

    def fetch_records(self):
        with mysql.connector.connect(**self.connection_config) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT timestamp, electricity_kwh
                FROM consumption_records
                ORDER BY timestamp
            """)

            records = cursor.fetchall()
            cursor.close()

            return records

    def save_record(self, building_id, timestamp, electricity_kwh):
        with mysql.connector.connect(**self.connection_config) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO consumption_records
                (building_id, timestamp, electricity_kwh)
                VALUES (%s, %s, %s)
            """, (building_id, timestamp, electricity_kwh))

            connection.commit()
            cursor.close()

            return True
