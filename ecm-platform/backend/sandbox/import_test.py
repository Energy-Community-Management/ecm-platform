from pathlib import Path
import logging

from app.services.import_manager import ImportManager
from app.services.quality_service import QualityService
from app.services.import_summary_service import ImportSummaryService
from app.repositories.database import Database
from app.repositories.schema import DatabaseSchema
from app.repositories.repository_manager import RepositoryManager


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def log_import_history(repository_manager: RepositoryManager) -> None:
    logger.info("")
    logger.info("=" * 60)
    logger.info("IMPORT HISTORY")
    logger.info("=" * 60)

    imports = repository_manager.list_imports()
    logger.info("Počet importů: %d", len(imports))

    for item in imports[:5]:
        logger.info(
            "%s | %s | %s | %s",
            item.imported_at,
            item.vendor.value,
            item.data_type.value,
            item.original_file_name,
        )


def log_import_summary(
    repository_manager: RepositoryManager,
    import_id: str,
) -> None:
    summary_service = ImportSummaryService(
        repository_manager=repository_manager,
        quality_service=QualityService(),
    )

    summary = summary_service.build(import_id)

    logger.info("")
    logger.info("=" * 60)
    logger.info("IMPORT SUMMARY")
    logger.info("=" * 60)
    logger.info("Import ID: %s", summary.import_id)
    logger.info("Soubor: %s", summary.original_file_name)
    logger.info("Zdroj: %s", summary.vendor.value)
    logger.info("Typ dat: %s", summary.data_type.value)
    logger.info("Importováno: %s", summary.imported_at)
    logger.info("Počet měření: %d", summary.measurements)
    logger.info("Celkem energie: %.4f kWh", summary.total_energy_kwh)
    logger.info("Období: %s -> %s", summary.start_time, summary.end_time)
    logger.info("Completeness: %.2f %%", summary.completeness)
    logger.info("Chybějící mezery: %d", summary.missing_intervals)
    logger.info("Warnings: %d", summary.warnings)
    logger.info("Errors: %d", summary.errors)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    source_file = base_dir / "storage" / "temp" / "pnd_export (17).csv"

    manager = ImportManager()
    result = manager.import_file(source_file)

    database_path = base_dir / "storage" / "ecm.sqlite"

    database = Database(database_path)
    schema = DatabaseSchema(database)
    schema.create()

    repository_manager = RepositoryManager(database)

    existing_import = repository_manager.find_import_by_checksum(
        result.import_record.checksum
    )

    if existing_import:
        logger.warning("Tento soubor už byl importován.")
        logger.warning("Import ID: %s", existing_import.import_id)
        logger.warning("Soubor: %s", existing_import.original_file_name)
        logger.warning("Zdroj: %s", existing_import.vendor.value)
        logger.warning("Typ dat: %s", existing_import.data_type.value)
        logger.warning("Importováno: %s", existing_import.imported_at)
        logger.warning("Archiv: %s", existing_import.stored_file_path)
        logger.warning("Vyber jiný soubor nebo otevři existující import.")

        loaded_series = repository_manager.load_series(existing_import.import_id)

        logger.info("")
        logger.info("=" * 60)
        logger.info("OPEN EXISTING SERIES")
        logger.info("=" * 60)
        logger.info("Načteno měření: %d", loaded_series.count())
        logger.info("Celkem energie: %.4f kWh", loaded_series.total_energy_kwh())
        logger.info("Začátek: %s", loaded_series.start())
        logger.info("Konec: %s", loaded_series.end())

        log_import_summary(repository_manager, existing_import.import_id)
        log_import_history(repository_manager)
        return

    saved_count = repository_manager.save_import_result(result)

    db_total = repository_manager.total_energy_by_import(
        result.import_record.import_id
    )

    loaded_series = repository_manager.load_series(result.import_record.import_id)

    logger.info("Uloženo měření do DB: %d", saved_count)
    logger.info("Součet z DB: %.4f kWh", db_total)
    logger.info("Načteno z DB: %d měření", loaded_series.count())
    logger.info("Součet načtený z DB: %.4f kWh", loaded_series.total_energy_kwh())

    series = result.series

    logger.info("")
    logger.info("=" * 60)
    logger.info("ENERGY SERIES")
    logger.info("=" * 60)

    logger.info("Počet měření: %d", series.count())
    logger.info("Začátek: %s", series.start())
    logger.info("Konec: %s", series.end())
    logger.info("Celkem energie: %.4f kWh", series.total_energy_kwh())
    logger.info("Průměr: %.4f kWh", series.average_energy_kwh())
    logger.info("Minimum: %.4f kWh", series.min_energy_kwh())
    logger.info("Maximum: %.4f kWh", series.max_energy_kwh())

    logger.info("")
    logger.info("=" * 60)
    logger.info("AGREGACE")
    logger.info("=" * 60)

    daily = series.daily_totals()
    monthly = series.monthly_totals()

    logger.info("Počet dnů: %d", len(daily))
    logger.info("Počet měsíců: %d", len(monthly))

    first_day = next(iter(daily.items()))
    logger.info("První den: %s = %.4f kWh", first_day[0], first_day[1])

    logger.info("")
    logger.info("=" * 60)
    logger.info("QUALITY")
    logger.info("=" * 60)

    quality = QualityService()
    report = quality.validate(series)

    logger.info("Completeness: %.2f %%", report.completeness)
    logger.info("Expected intervalů: %d", report.expected_intervals)
    logger.info("Missing intervalů: %d", report.missing_intervals_count)
    logger.info("Chybějící mezery: %d", len(report.missing_intervals))

    if report.missing_intervals:
        gap = report.missing_intervals[0]
        logger.info("První nalezená mezera:")
        logger.info("Od: %s", gap.start)
        logger.info("Do: %s", gap.end)
        logger.info("Délka: %s", gap.duration)
        logger.info("Důvod: %s", gap.reason.value)
        logger.info("Závažnost: %s", gap.severity.value)
    else:
        logger.info("Žádné chybějící intervaly.")

    log_import_summary(repository_manager, result.import_record.import_id)
    log_import_history(repository_manager)

    logger.info("")
    logger.info("=" * 60)
    logger.info("KONEC TESTU")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()