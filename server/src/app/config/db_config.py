import mysql.connector
from mysql.connector import pooling
from config.config import *


class DatabaseConnection:
    _pool = None  # shared across all instances

    def __init__(self):
        if DatabaseConnection._pool is None:
            DatabaseConnection._pool = self._initialize_pool()

    @staticmethod
    def _initialize_pool():
        print("Initializing MySQL pool...")
        return pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=10,
            pool_reset_session=True,
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            connection_timeout=10,
        )

    def get_connection(self):
        return DatabaseConnection._pool.get_connection()
