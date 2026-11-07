import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="carbon_compass"
    )