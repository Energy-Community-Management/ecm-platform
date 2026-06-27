from pathlib import Path
import logging

from app.services.hash_service import HashService
from app.services.import_id_service import ImportIdService
from app.services.archive_service import ArchiveService


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
        / "pnd_export (15).csv"
    )

    storage_root = base_dir / "storage"

    import_id_service = ImportIdService()
    hash_service = HashService()
    archive_service = ArchiveService(storage_root)

    import_id = import_id_service.generate()
    checksum = hash_service.calculate_sha256(source_file)

    stored_file = archive_service.store_original(
        source_file=source_file,
        vendor="OTE",
        import_id=import_id,
    )

    logger.info("Import ID: %s", import_id)
    logger.info("SHA256: %s", checksum)
    logger.info("Originál uložen: %s", stored_file)


if __name__ == "__main__":
    main()