from datetime import datetime

from app.domain.import_record import ImportRecord
from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus
from app.domain.import_record import ImportRecord
from app.repositories.database import Database
from app.mappers.import_mapper import ImportMapper


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
                imported_at,    
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    import_record.status.value,
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

    def find_by_checksum(self, checksum: str) -> ImportRecord | None:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    vendor,
                    data_type,
                    file_format,
                    checksum,
                    original_file_name,
                    stored_file_path,
                    imported_at,
                    status
                FROM imports
                WHERE checksum = ?
                LIMIT 1
                """,
                (checksum,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return ImportMapper.from_row(row)

    def list(self) -> list[ImportRecord]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                 SELECT
                    id,
                    vendor,
                    data_type,
                    file_format,
                    checksum,
                    original_file_name,
                    stored_file_path,
                    imported_at,
                    status
                FROM imports
                ORDER BY imported_at DESC
                """
            )

            rows = cursor.fetchall()

        return [
            ImportMapper.from_row(row)
            for row in rows
        ]

    def get_by_id(self, import_id: str) -> ImportRecord | None:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    vendor,
                    data_type,
                    file_format,
                    checksum,
                    original_file_name,
                    stored_file_path,
                    imported_at,
                    status
                FROM imports
                WHERE id = ?
                LIMIT 1
                """,
                (import_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return ImportMapper.from_row(row)