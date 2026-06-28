from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(slots=True, frozen=True)
class MissingInterval:
    start: datetime
    end: datetime
    duration: timedelta