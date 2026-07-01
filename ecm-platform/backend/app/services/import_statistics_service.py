from app.domain.import_statistics import ImportStatistics
from app.domain.enums.vendor import Vendor
from app.repositories.repository_manager import RepositoryManager


class ImportStatisticsService:
    """Vytváří souhrnné statistiky importů."""

    def __init__(self, repository_manager: RepositoryManager) -> None:
        self.repository_manager = repository_manager

    def build(self) -> ImportStatistics:
        imports = self.repository_manager.list_imports()

        total_imports = len(imports)
        total_measurements = 0
        total_energy = 0.0

        ote_imports = 0
        goodwe_imports = 0
        sofar_imports = 0

        imported_dates = [
            item.imported_at
            for item in imports
        ]

        first_import = min(imported_dates) if imported_dates else None
        last_import = max(imported_dates) if imported_dates else None

        for import_record in imports:
            series = self.repository_manager.load_series(
                import_record.import_id
            )

            total_measurements += series.count()
            total_energy += series.total_energy_kwh()

            if import_record.vendor == Vendor.OTE:
                ote_imports += 1
            elif import_record.vendor == Vendor.GOODWE:
                goodwe_imports += 1
            elif import_record.vendor == Vendor.SOFAR:
                sofar_imports += 1

        return ImportStatistics(
            total_imports=total_imports,
            total_measurements=total_measurements,
            total_energy_kwh=total_energy,
            first_import=first_import,
            last_import=last_import,
            ote_imports=ote_imports,
            goodwe_imports=goodwe_imports,
            sofar_imports=sofar_imports,
        )