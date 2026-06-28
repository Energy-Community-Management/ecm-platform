from pathlib import Path
import csv

from app.domain.import_info import ImportInfo
from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus


class ImportDetector:
    """Rozpoznání typu importovaného souboru."""

    def detect(self, file_path: Path) -> ImportInfo:
        if file_path.suffix.lower() == ".csv":
            return self._detect_csv(file_path)

        return ImportInfo(
            vendor=Vendor.UNKNOWN,
            data_type=DataType.UNKNOWN,
            file_format=FileFormat.UNKNOWN,
            status=ImportStatus.FAILED,
            original_file=file_path,
        )

    def _detect_csv(self, file_path: Path) -> ImportInfo:
        with open(file_path, mode="r", encoding="cp1250", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            rows = list(reader)
            columns = reader.fieldnames or []

        row_count = len(rows)

        if row_count <= 20 and "Celkem v intervalu" in columns:
            return ImportInfo(
                vendor=Vendor.OTE,
                data_type=DataType.MONTHLY_SUMMARY,
                file_format=FileFormat.CSV,
                status=ImportStatus.RECEIVED,
                original_file=file_path,
                records=row_count,
            )

        if row_count > 30000 and "Datum" in columns:
            if any("[kW]" in column for column in columns):
                return ImportInfo(
                    vendor=Vendor.OTE,
                    data_type=DataType.PROFILE_15MIN,
                    file_format=FileFormat.CSV,
                    status=ImportStatus.RECEIVED,
                    original_file=file_path,
                    records=row_count,
                )

        return ImportInfo(
            vendor=Vendor.UNKNOWN,
            data_type=DataType.UNKNOWN,
            file_format=FileFormat.CSV,
            status=ImportStatus.FAILED,
            original_file=file_path,
            records=row_count,
        )