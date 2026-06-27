from pathlib import Path
from datetime import datetime
import shutil


class ArchiveService:
    """Archivuje originální importované soubory."""

    def __init__(self, storage_root: Path) -> None:
        self.storage_root = storage_root

    def store_original(
        self,
        source_file: Path,
        vendor: str,
        import_id: str,
    ) -> Path:
        imported_at = datetime.now()

        target_dir = (
            self.storage_root
            / "original"
            / vendor.lower()
            / imported_at.strftime("%Y")
            / imported_at.strftime("%m")
            / imported_at.strftime("%d")
            / import_id
        )

        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / source_file.name

        shutil.copy2(source_file, target_file)

        return target_file