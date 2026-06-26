from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EnergyMeasurement:
    start: datetime
    end: datetime
    source: str
    value_kwh: float