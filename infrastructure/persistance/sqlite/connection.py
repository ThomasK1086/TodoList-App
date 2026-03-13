import sqlite3
from abc import abstractmethod, abstractclassmethod, abstractstaticmethod
from datetime import date, datetime


class DBConnection:
    """
    Singleton Database Connection instance.
    Pattern: One DB-one connection-many cursors-one cursor per repositor
    """
    _instance = None

    def __new__(cls, db_name=None):
        """Only allow one single (singleton) instance of this class to exist at the same time"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect(db_name)
        return cls._instance

    def connect(self, db_name):

        def convert_to_datetime(val):
            """Converts bytes from SQLite into a Python datetime object."""
            # SQLite often returns bytes; decode to string first
            dt_str = val.decode()
            try:
                # Handles '2026-03-12 15:45:12.032464' or '2026-03-12'
                return datetime.fromisoformat(dt_str)
            except ValueError:
                # Fallback for simple 'YYYY-MM-DD' strings if they exist
                return datetime.strptime(dt_str, "%Y-%m-%d")

        sqlite3.register_converter("DATETIME", convert_to_datetime)
        sqlite3.register_converter("TIMESTAMP", convert_to_datetime)
        sqlite3.register_converter("DATE", convert_to_datetime)

        self.conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        # add logic for database connection init here

    @property
    def cursor(self):
        """On request, returns a new cursor from the singleton"""
        return self.conn.cursor

    def commit(self):
        self.conn.commit()

    @classmethod
    def close(cls):
        if cls._instance is not None:
            cls._instance.conn.close()

    @classmethod
    def __getattr__(cls, name):
        if cls._instance is not None:
            cls._instance.conn.__getattr__(name)



class BaseDatabaseInterface:
    def __init__(self, db_name):
        self.conn = DBConnection(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    @abstractmethod
    def _create_tables(self):
        """Initializes the database schema."""

