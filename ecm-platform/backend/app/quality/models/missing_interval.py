from dataclasses import dataclass
from datetime import datetime, timedelta

from app.quality.enums.gap_reason import GapReason
from app.quality.enums.validation_severity import ValidationSeverity


@dataclass(slots=True, frozen=True)
class MissingInterval:
    start: datetime
    end: datetime
    duration: timedelta
    reason: GapReason = GapReason.UNKNOWN
    severity: ValidationSeverity = ValidationSeverity.WARNING