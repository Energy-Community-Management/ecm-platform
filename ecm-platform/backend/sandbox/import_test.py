from pathlib import Path
import logging

from app.services.import_manager import ImportManager
from app.services.energy_validation_service import EnergyValidationService


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:

    base_dir = Path(__file__).resolve().parents[1]

    source_file = (
        base_dir
        / "storage"
        / "temp"
        / "pnd_export (16).csv"
    )

    manager = ImportManager()

    result = manager.import_file(source_file)

    series = result.series

    logger.info("=" * 60)
    logger.info("IMPORT")
    logger.info("=" * 60)

    logger.info("Import ID: %s", result.import_record.import_id)
    logger.info("Vendor: %s", result.import_record.vendor.value)
    logger.info("Typ dat: %s", result.import_record.data_type.value)
    logger.info("Soubor: %s", result.import_record.original_file_name)
    logger.info("SHA256: %s", result.import_record.checksum)
    logger.info("Archiv: %s", result.import_record.stored_file_path)

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
    logger.info(
        "První den: %s = %.4f kWh",
        first_day[0],
        first_day[1],
    )

    logger.info("")
    logger.info("=" * 60)
    logger.info("VALIDACE")
    logger.info("=" * 60)

    validator = EnergyValidationService()

    missing = validator.find_missing_intervals(series)

    logger.info("Completeness: %.2f %%", validator.completeness(series))
    logger.info("Expected intervalů: %d", validator.expected_intervals_count(series))
    logger.info("Missing intervalů: %d", validator.missing_intervals_count(series))
    logger.info("Chybějící intervaly: %d", len(missing))

    if missing:

        gap = missing[0]

        logger.info("První nalezená mezera:")
        logger.info("Od: %s", gap.start)
        logger.info("Do: %s", gap.end)
        logger.info("Délka: %s", gap.duration)

    else:

        logger.info("Žádné chybějící intervaly.")

    logger.info("")
    logger.info("=" * 60)
    logger.info("KONEC TESTU")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()