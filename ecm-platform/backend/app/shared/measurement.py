from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Measurement:
    timestamp: datetime
    consumption: float
    production: float
    export: float
    import_energy: float