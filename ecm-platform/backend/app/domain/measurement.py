from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EnergyMeasurement:
    """Jedno energetické měření."""

    start: datetime
    end: datetime
    source: str
    value_kwh: float
    status: str = ""