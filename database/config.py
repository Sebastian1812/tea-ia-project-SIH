import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='tesis_tea',
                user='tea_user',
                password='TeaPassword123!',  # La que creaste
                charset='utf8mb4'
            )
            return connection
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return None
