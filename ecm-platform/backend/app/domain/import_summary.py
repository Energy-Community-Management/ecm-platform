from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.domain.enums.data_type import DataType
from app.domain.enums.vendor import Vendor


@dataclass(slots=True, frozen=True)
class ImportSummary:
    """Souhrn importu pro GUI, API a reporty."""

    import_id: str

    vendor: Vendor
    data_type: DataType

    imported_at: datetime

    original_file_name: str
    archive_path: Path

    measurements: int

    total_energy_kwh: float

    start_time: datetime
    end_time: datetime

    completeness: float

    missing_intervals: int

    warnings: int

    errors: int