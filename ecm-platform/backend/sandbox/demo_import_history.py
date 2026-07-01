from pathlib import Path
import logging

from app.repositories.database import Database
from app.repositories.schema import DatabaseSchema
from app.repositories.repository_manager import RepositoryManager


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

    imports = repository_manager.list_imports()

    logger.info("=" * 60)
    logger.info("IMPORT HISTORY")
    logger.info("=" * 60)
    logger.info("Počet importů: %d", len(imports))

    for item in imports:
        logger.info(
            "%s | %s | %s | %s | %s | %s",
            item.imported_at,
            item.import_id,
            item.status.value,
            item.vendor.value,
            item.data_type.value,
            item.original_file_name,
        )


if __name__ == "__main__":
    main()