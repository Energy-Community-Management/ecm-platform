from app.domain.enums.import_status import ImportStatus
from app.repositories.repository_manager import RepositoryManager


class ImportLifecycleService:
    """Řídí životní cyklus importu."""

    def __init__(
        self,
        repository_manager: RepositoryManager,
    ) -> None:
        self.repository_manager = repository_manager

    def activate(self, import_id: str) -> None:
        """Označí import jako ACTIVE."""
        self.repository_manager.update_import_status(
            import_id,
            ImportStatus.ACTIVE,
        )

    def archive(self, import_id: str) -> None:
        """Označí import jako ARCHIVED."""
        self.repository_manager.update_import_status(
            import_id,
            ImportStatus.ARCHIVED,
        )

    def fail(self, import_id: str) -> None:
        """Označí import jako FAILED."""
        self.repository_manager.update_import_status(
            import_id,
            ImportStatus.FAILED,
        )

    def restore(self, import_id: str) -> None:
        """Obnoví archivovaný import."""
        self.activate(import_id)

    def purge(self, import_id: str):
        """Trvale smaže import z databáze včetně jeho měření."""
        return self.repository_manager.purge_import(import_id)