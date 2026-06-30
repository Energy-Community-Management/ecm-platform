from app.domain.import_result import ImportResult
from app.repositories.database import Database
from app.repositories.import_repository import ImportRepository
from app.repositories.meter_repository import MeterRepository
from app.repositories.measurement_repository import MeasurementRepository
from datetime import datetime

from app.domain.import_record import ImportRecord
from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType
from app.domain.enums.file_format import FileFormat
from app.domain.enums.import_status import ImportStatus


class RepositoryManager:
    """Orchestruje ukládání a načítání dat přes jednotlivé repository."""

    def __init__(self, database: Database) -> None:
        self.import_repository = ImportRepository(database)
        self.meter_repository = MeterRepository(database)
        self.measurement_repository = MeasurementRepository(database)

    def save_import_result(self, result: ImportResult) -> int:
        self.import_repository.save(result.import_record)

        meter_id = self.meter_repository.get_or_create(
            source=result.series.first().source,
            unit="kWh",
        )

        return self.measurement_repository.save_series(
            import_id=result.import_record.import_id,
            meter_id=meter_id,
            series=result.series,
        )

    def total_energy_by_import(self, import_id: str) -> float:
        return self.measurement_repository.total_energy_by_import(import_id)

    def import_exists_by_checksum(self, checksum: str) -> bool:
        return self.import_repository.exists_by_checksum(checksum)

    def load_series_by_import(self, import_id: str):
        return self.measurement_repository.load_series_by_import(import_id)

    def find_import_by_checksum(self, checksum: str):
        return self.import_repository.find_by_checksum(checksum)

    def list_imports(self):
        return self.import_repository.list()

    def get_import(self, import_id: str):
        return self.import_repository.get_by_id(import_id)