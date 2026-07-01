from pathlib import Path
import logging

from app.repositories.database import Database
from app.repositories.schema import DatabaseSchema
from app.repositories.repository_manager import RepositoryManager
from app.services.import_lifecycle_service import ImportLifecycleService


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
    lifecycle = ImportLifecycleService(repository_manager)

    imports = repository_manager.list_imports()

    if not imports:
        logger.warning("Žádné importy v databázi.")
        return

    # POZOR: pro test mažeme nejstarší import, ne poslední
    selected_import = imports[-1]

    logger.info("Vybraný import ke smazání: %s", selected_import.import_id)
    logger.info("Soubor: %s", selected_import.original_file_name)

    series_before = repository_manager.load_series(selected_import.import_id)
    logger.info("Měření před smazáním: %d", series_before.count())

    result = lifecycle.purge(selected_import.import_id)

    logger.info("Smazaná měření: %d", result.deleted_measurements)
    logger.info("Smazané importy: %d", result.deleted_imports)
    logger.info("Smazaná nepoužitá měřidla: %d", result.deleted_meters)

    deleted_import = repository_manager.get_import(selected_import.import_id)

    if deleted_import is None:
        logger.info("Import byl smazán z databáze.")
    else:
        logger.error("Import stále existuje!")

    logger.info("Hotovo.")


if __name__ == "__main__":
    main()