from pathlib import Path
import logging

from app.repositories.database import Database
from app.repositories.schema import DatabaseSchema
from app.repositories.repository_manager import RepositoryManager
from app.services.import_statistics_service import ImportStatisticsService


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    database_path = base_dir / "storage" / "ecm.sqlite"

    database = Database(database_path)
    schema = DatabaseSchema(database)
    schema.create()

    repository_manager = RepositoryManager(database)

    statistics_service = ImportStatisticsService(
        repository_manager=repository_manager,
    )

    stats = statistics_service.build()

    logger.info("=" * 60)
    logger.info("IMPORT STATISTICS")
    logger.info("=" * 60)

    logger.info("Počet importů: %d", stats.total_imports)
    logger.info("Počet měření: %d", stats.total_measurements)
    logger.info("Celkem energie: %.4f kWh", stats.total_energy_kwh)

    logger.info("První import: %s", stats.first_import)
    logger.info("Poslední import: %s", stats.last_import)

    logger.info("OTE importy: %d", stats.ote_imports)
    logger.info("GoodWe importy: %d", stats.goodwe_imports)
    logger.info("Sofar importy: %d", stats.sofar_imports)


if __name__ == "__main__":
    main()