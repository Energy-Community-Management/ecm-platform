from app.domain.import_result import ImportResult
from app.domain.purge_result import PurgeResult
from app.repositories.database import Database
from app.repositories.import_repository import ImportRepository
from app.repositories.meter_repository import MeterRepository
from app.repositories.measurement_repository import MeasurementRepository

class RepositoryManager:
    """Orchestruje ukládání a načítání dat přes jednotlivé repository."""

    def __init__(self, database: Database) -> None:
        self.database = database
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

    def load_series(self, import_id: str):
        return self.measurement_repository.load_series_by_import(import_id)

    def update_import_status(
            self,
            import_id: str,
            status,
    ) -> None:
        self.import_repository.update_status(
            import_id,
            status,
        )

    def list_imports_by_status(self, status):
        return self.import_repository.list_by_status(status)

    def list_active_imports(self):
        from app.domain.enums.import_status import ImportStatus
        return self.list_imports_by_status(ImportStatus.ACTIVE)

    def list_archived_imports(self):
        from app.domain.enums.import_status import ImportStatus
        return self.list_imports_by_status(ImportStatus.ARCHIVED)

    def delete_measurements_by_import(self, import_id: str) -> int:
        return self.measurement_repository.delete_by_import(import_id)

    def delete_import(self, import_id: str) -> int:
        return self.import_repository.delete(import_id)

    def cleanup_unused_meters(self) -> int:
        return self.meter_repository.cleanup_unused()

    def purge_import(self, import_id: str) -> PurgeResult:
        with self.database.transaction() as connection:
            deleted_measurements = self.measurement_repository.delete_by_import(
                import_id,
                connection=connection,
            )

            deleted_imports = self.import_repository.delete(
                import_id,
                connection=connection,
            )

            deleted_meters = self.meter_repository.cleanup_unused(
                connection=connection,
            )

            if deleted_imports == 0:
                raise ValueError(
                    f"Import neexistuje nebo už byl smazán: {import_id}"
                )

            return PurgeResult(
                deleted_measurements=deleted_measurements,
                deleted_imports=deleted_imports,
                deleted_meters=deleted_meters,
            )