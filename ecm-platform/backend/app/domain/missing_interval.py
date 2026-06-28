from dataclasses import dataclass
from datetime import datetime, timedelta

from app.domain.enums.gap_reason import GapReason
from app.domain.enums.validation_severity import ValidationSeverity


@dataclass(slots=True, frozen=True)
class MissingInterval:
    start: datetime
    end: datetime
    duration: timedelta
    reason: GapReason = GapReason.UNKNOWN
    severity: ValidationSeverity = ValidationSeverity.WARNING