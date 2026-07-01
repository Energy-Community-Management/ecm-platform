from app.repositories.database import Database


class MeterRepository:
    """Repository pro tabulku meters."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def get_or_create(
        self,
        source: str,
        name: str | None = None,
        unit: str | None = None,
    ) -> int:
        with self.database.connect() as connection:
            cursor = connection.execute(
                "SELECT id FROM meters WHERE source = ?",
                (source,),
            )

            row = cursor.fetchone()

            if row:
                return row[0]

            cursor = connection.execute(
                """
                INSERT INTO meters (source, name, unit)
                VALUES (?, ?, ?)
                """,
                (source, name, unit),
            )

            return cursor.lastrowid

    def cleanup_unused(
            self,
            connection=None,
    ) -> int:
        active_connection = connection or self.database.connect()

        try:
            cursor = active_connection.execute(
                """
                DELETE FROM meters
                WHERE id NOT IN (
                    SELECT DISTINCT meter_id
                    FROM measurements
                )
                """
            )

            return cursor.rowcount

        finally:
            if connection is None:
                active_connection.close()