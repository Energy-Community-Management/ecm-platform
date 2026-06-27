from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus


@dataclass(slots=True)
class ImportRecord:
    import_id: str
    vendor: Vendor
    data_type: DataType
    file_format: FileFormat
    status: ImportStatus

    original_file_name: str
    original_file_path: Path
    stored_file_path: Path

    checksum: str
    imported_at: datetime

    records_count: int = 0
    error_message: str = ""