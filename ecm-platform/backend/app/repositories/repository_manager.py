from app.domain.import_result import ImportResult
from app.repositories.database import Database
from app.repositories.import_repository import ImportRepository
from app.repositories.meter_repository import MeterRepository
from app.repositories.measurement_repository import MeasurementRepository


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