from dataclasses import dataclass, field

from app.domain.missing_interval import MissingInterval


@dataclass(slots=True)
class ValidationReport:
    completeness: float
    expected_intervals: int
    missing_intervals_count: int
    missing_intervals: list[MissingInterval] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return self.missing_intervals_count > 0