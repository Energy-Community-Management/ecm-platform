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

    selected_import = imports[0]

    logger.info("Vybraný import: %s", selected_import.import_id)
    logger.info("Původní status: %s", selected_import.status.value)

    lifecycle.archive(selected_import.import_id)

    archived_import = repository_manager.get_import(selected_import.import_id)
    logger.info("Po archivaci: %s", archived_import.status.value)

    lifecycle.restore(selected_import.import_id)

    restored_import = repository_manager.get_import(selected_import.import_id)
    logger.info("Po obnovení: %s", restored_import.status.value)


if __name__ == "__main__":
    main()