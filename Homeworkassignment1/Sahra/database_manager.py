import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.__db_path = db_path

    def get_db_path(self):
        return self.__db_path

    def set_db_path(self, new_path):
        self.__db_path = new_path

    def create_table(self):
        with sqlite3.connect(self.__db_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS consumption_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    building_id INTEGER,
                    timestamp TEXT,
                    electricity_kwh REAL
                )
            """)

    def save_record(self, building_id, timestamp, electricity_kwh):
        with sqlite3.connect(self.__db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO consumption_records
                (building_id, timestamp, electricity_kwh)
                VALUES (?, ?, ?)
                """,
                (building_id, timestamp, electricity_kwh)
            )
            return cursor.lastrowid

    def fetch_records(self):
        with sqlite3.connect(self.__db_path) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.execute(
                "SELECT record_id, building_id, timestamp, electricity_kwh FROM consumption_records"
            )

            return [dict(row) for row in cursor.fetchall()]

    def fetch_records_by_date(self, start_date, end_date):
        with sqlite3.connect(self.__db_path) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.execute(
                """
                SELECT record_id, building_id, timestamp, electricity_kwh
                FROM consumption_records
                WHERE timestamp BETWEEN ? AND ?
                """,
                (start_date, end_date)
            )

            return [dict(row) for row in cursor.fetchall()]