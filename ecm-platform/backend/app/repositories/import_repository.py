from app.domain.import_record import ImportRecord
from app.repositories.database import Database


class ImportRepository:
    """Repository pro tabulku imports."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def save(self, import_record: ImportRecord) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO imports (
                    id,
                    vendor,
                    data_type,
                    file_format,
                    checksum,
                    original_file_name,
                    stored_file_path,
                    imported_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    import_record.import_id,
                    import_record.vendor.value,
                    import_record.data_type.value,
                    import_record.file_format.value,
                    import_record.checksum,
                    import_record.original_file_name,
                    str(import_record.stored_file_path),
                    import_record.imported_at.isoformat(),
                ),
            )

    def exists_by_checksum(self, checksum: str) -> bool:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                SELECT 1
                FROM imports
                WHERE checksum = ?
                LIMIT 1
                """,
                (checksum,),
            )

            return cursor.fetchone() is not None