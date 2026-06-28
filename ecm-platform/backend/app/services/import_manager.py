from datetime import datetime
from pathlib import Path

from app.domain.import_record import ImportRecord
from app.domain.import_result import ImportResult
from app.domain.enums.import_status import ImportStatus
from app.domain.enums.data_type import DataType

from app.services.import_id_service import ImportIdService
from app.services.hash_service import HashService
from app.services.archive_service import ArchiveService

from app.imports.detector import ImportDetector
from app.imports.parser_factory import ParserFactory
from app.repositories.metadata_repository import MetadataRepository


class ImportManager:
    """Řídí celý proces importu."""

    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parents[2]
        storage_root = base_dir / "storage"

        self.import_id_service = ImportIdService()
        self.hash_service = HashService()
        self.detector = ImportDetector()
        self.parser_factory = ParserFactory()
        self.archive_service = ArchiveService(storage_root)
        self.metadata_repository = MetadataRepository(storage_root)

    def import_file(self, file_path: Path) -> ImportResult:
        import_id = self.import_id_service.generate()
        checksum = self.hash_service.calculate_sha256(file_path)
        import_info = self.detector.detect(file_path)

        stored_file = self.archive_service.store_original(
            source_file=file_path,
            vendor=import_info.vendor.value,
            import_id=import_id,
        )

        import_record = ImportRecord(
            import_id=import_id,
            vendor=import_info.vendor,
            data_type=import_info.data_type,
            file_format=import_info.file_format,
            status=ImportStatus.PROCESSED,
            original_file_name=file_path.name,
            original_file_path=file_path,
            stored_file_path=stored_file,
            checksum=checksum,
            imported_at=datetime.now(),
            records_count=import_info.records,
        )

        parser = self.parser_factory.get_parser(import_info)

        if import_info.data_type is DataType.PROFILE_15MIN:
            series = parser.load_15min_profile(file_path)
        elif import_info.data_type is DataType.MONTHLY_SUMMARY:
            series = parser.load_monthly_summary(file_path)
        else:
            raise ValueError(
                f"Nepodporovaný typ dat: {import_info.data_type.value}"
            )

        import_record.records_count = series.count()
        import_record.status = ImportStatus.READY

        self.metadata_repository.save(import_record)

        return ImportResult(
            import_record=import_record,
            measurements=series.measurements,
        )