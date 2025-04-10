"""
This module contains the configuration class for the database connection.
"""
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the database connection.
    """
    def __init__(self):
        self.server = os.getenv('SQL_SERVER')
        self.username = os.getenv('SQL_USERNAME')
        self.password = os.getenv('SQL_PASSWORD')
        self.database = os.getenv('SQL_DATABASE')
        self.validate_config()

        self.connection_string = (
            f'DRIVER=ODBC Driver 17 for SQL Server;'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            f'Encrypt=yes;TrustServerCertificate=yes;'
        )

        self.sqlalchemy_database_uri = ('mssql+pyodbc:///?odbc_connect=' +
                                        urllib.parse.quote_plus(self.connection_string))

    def validate_config(self):
        """
        Validate the configuration.
        :raises ValueError: If any of the required configuration variables are not set.
        """
        if not self.server:
            raise ValueError("Configuration variable SQL_SERVER is not set")
        if not self.username:
            raise ValueError("Configuration variable SQL_USERNAME is not set")
        if not self.password:
            raise ValueError("Configuration variable SQL_PASSWORD is not set")
        if not self.database:
            raise ValueError("Configuration variable SQL_DATABASE is not set")

    def __str__(self):
        return f"{self.server}, {self.username}, {self.database}"
