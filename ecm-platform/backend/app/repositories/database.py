import sqlite3
from pathlib import Path


class Database:
    """Správa připojení k SQLite databázi."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        return sqlite3.connect(self.database_path)