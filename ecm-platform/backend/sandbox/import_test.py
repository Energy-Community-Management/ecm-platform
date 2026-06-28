from pathlib import Path
import logging

from app.services.import_manager import ImportManager


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    source_file = base_dir / "storage" / "temp" / "pnd_export (16).csv"

    manager = ImportManager()
    result = manager.import_file(source_file)

    logger.info("Import ID: %s", result.import_record.import_id)
    logger.info("Vendor: %s", result.import_record.vendor.value)
    logger.info("Typ dat: %s", result.import_record.data_type.value)
    logger.info("Soubor: %s", result.import_record.original_file_name)
    logger.info("SHA256: %s", result.import_record.checksum)
    logger.info("Archiv: %s", result.import_record.stored_file_path)

    logger.info("Počet měření: %d", result.series.count())
    logger.info("Celkem kWh: %.4f", result.series.total_energy_kwh())
    logger.info("Min kWh / interval: %.4f", result.series.min_energy_kwh())
    logger.info("Max kWh / interval: %.4f", result.series.max_energy_kwh())


if __name__ == "__main__":
    main()