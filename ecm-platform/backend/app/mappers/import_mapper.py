from datetime import datetime
from pathlib import Path

from app.domain.import_record import ImportRecord
from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus


class ImportMapper:
    """Převody mezi databázovým řádkem a ImportRecord."""

    @staticmethod
    def from_row(row) -> ImportRecord:
        return ImportRecord(
            import_id=row[0],
            vendor=Vendor(row[1]),
            data_type=DataType(row[2]),
            file_format=FileFormat(row[3]),
            checksum=row[4],
            original_file_name=row[5],
            original_file_path=Path(row[5]),
            stored_file_path=Path(row[6]),
            imported_at=datetime.fromisoformat(row[7]),
            status=ImportStatus(row[8]),
        )