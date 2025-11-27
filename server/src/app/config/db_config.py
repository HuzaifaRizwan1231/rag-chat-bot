import mysql.connector
from mysql.connector import Error, pooling
from config.config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_PORT

class DatabaseConnection:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize_pool()
        return cls._instance

    @classmethod
    def _initialize_pool(cls):
        try:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=10,  # Adjust pool size as needed
                pool_reset_session=True,
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=MYSQL_PORT,
                connection_timeout=10
            )
            print("Connection pool created successfully")
        except Error as e:
            print(f"The error '{e}' occurred while creating the connection pool")

    def create_connection(self):
        try:
            if self._pool:
                connection = self._pool.get_connection()
                if connection.is_connected():
                    print("Connection to MySQL DB successful")
                return connection
            else:
                print("Connection pool is not initialized")
        except Error as e:
            print(f"The error '{e}' occurred while getting a connection from the pool")
            return None
