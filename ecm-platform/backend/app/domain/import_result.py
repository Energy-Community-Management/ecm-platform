from dataclasses import dataclass

from app.domain.import_record import ImportRecord
from app.domain.measurement import EnergyMeasurement


@dataclass(slots=True)
class ImportResult:
    import_record: ImportRecord
    measurements: list[EnergyMeasurement]