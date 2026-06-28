from dataclasses import dataclass
from pathlib import Path

from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus


@dataclass(slots=True)
class ImportInfo:
    vendor: Vendor
    data_type: DataType
    file_format: FileFormat
    status: ImportStatus
    original_file: Path
    checksum: str = ""
    records: int = 0