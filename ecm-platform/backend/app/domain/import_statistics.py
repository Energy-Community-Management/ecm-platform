from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class ImportStatistics:
    """Souhrnné statistiky importů."""

    total_imports: int
    total_measurements: int
    total_energy_kwh: float

    first_import: datetime | None
    last_import: datetime | None

    ote_imports: int
    goodwe_imports: int
    sofar_imports: int