import mysql.connector

class MySQLConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Establishes a new MySQL connection."""
        self.connection = mysql.connector.connect(
            host="host",
            user="root",
            password="pass"
        )

    def select_database(self, database_name):
        """Selects the specified database for the existing connection."""
        if self.connection.is_connected():
            self.connection.database = database_name

    def get_connection(self):
        """Returns the existing connection or establishes a new one if not connected."""
        if not self.connection.is_connected():
            self._connect()
        return self.connection
