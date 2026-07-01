from app.repositories.database import Database


class DatabaseSchema:
    """Vytvoření databázového schématu."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self) -> None:
        with self.database.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS imports (
                    id TEXT PRIMARY KEY,
                    vendor TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    file_format TEXT NOT NULL,
                    checksum TEXT NOT NULL,
                    original_file_name TEXT NOT NULL,
                    stored_file_path TEXT NOT NULL,
                    imported_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ACTIVE'
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS meters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL UNIQUE,
                    name TEXT,
                    unit TEXT
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    import_id TEXT NOT NULL,
                    meter_id INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    value_kwh REAL NOT NULL,
                    status TEXT,
                    FOREIGN KEY(import_id) REFERENCES imports(id),
                    FOREIGN KEY(meter_id) REFERENCES meters(id)
                )
            """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_measurements_import_id
                ON measurements(import_id)
            """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_measurements_meter_time
                ON measurements(meter_id, start_time)
            """)

            self._ensure_import_status_column(connection)

    def _ensure_import_status_column(self, connection) -> None:
        cursor = connection.execute("PRAGMA table_info(imports)")
        columns = [row[1] for row in cursor.fetchall()]

        if "status" not in columns:
            connection.execute(
                "ALTER TABLE imports ADD COLUMN status TEXT NOT NULL DEFAULT 'ACTIVE'"
            )