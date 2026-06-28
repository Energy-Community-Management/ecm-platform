from dataclasses import dataclass

from app.domain.import_record import ImportRecord
from app.domain.energy_series import EnergySeries


@dataclass(slots=True)
class ImportResult:
    import_record: ImportRecord
    series: EnergySeries