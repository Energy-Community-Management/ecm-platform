from app.domain.import_summary import ImportSummary
from app.repositories.repository_manager import RepositoryManager
from app.services.quality_service import QualityService


class ImportSummaryService:
    """Skládá souhrn importu pro GUI, API a reporty."""

    def __init__(
        self,
        repository_manager: RepositoryManager,
        quality_service: QualityService,
    ) -> None:
        self.repository_manager = repository_manager
        self.quality_service = quality_service

    def build(self, import_id: str) -> ImportSummary:
        import_record = self.repository_manager.get_import(import_id)

        if import_record is None:
            raise ValueError(f"Import neexistuje: {import_id}")

        series = self.repository_manager.load_series(import_id)
        report = self.quality_service.validate(series)

        warnings = sum(
            1
            for gap in report.missing_intervals
            if gap.severity.value == "WARNING"
        )

        errors = sum(
            1
            for gap in report.missing_intervals
            if gap.severity.value == "ERROR"
        )

        return ImportSummary(
            import_id=import_record.import_id,
            vendor=import_record.vendor,
            data_type=import_record.data_type,
            imported_at=import_record.imported_at,
            original_file_name=import_record.original_file_name,
            archive_path=import_record.stored_file_path,
            measurements=series.count(),
            total_energy_kwh=series.total_energy_kwh(),
            start_time=series.start(),
            end_time=series.end(),
            completeness=report.completeness,
            missing_intervals=len(report.missing_intervals),
            warnings=warnings,
            errors=errors,
        )