from pathlib import Path

from app.domain.import_result import ImportResult


class ImportManager:
    """Řídí celý proces importu."""

    def __init__(self) -> None:
        pass

    def import_file(self, file_path: Path) -> ImportResult:
        raise NotImplementedError("ImportManager zatím není dokončen.")