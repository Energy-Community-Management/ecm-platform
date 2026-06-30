from datetime import datetime

from app.domain.import_record import ImportRecord
from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus


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
                    imported_at
                FROM imports
                WHERE checksum = ?
                LIMIT 1
                """,
                (checksum,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return ImportRecord(
            import_id=row[0],
            vendor=Vendor(row[1]),
            data_type=DataType(row[2]),
            file_format=FileFormat(row[3]),
            status=ImportStatus.READY,
            original_file_name=row[5],
            original_file_path=row[5],
            stored_file_path=row[6],
            checksum=row[4],
            imported_at=datetime.fromisoformat(row[7]),
        )