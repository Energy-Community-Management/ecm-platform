from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PurgeResult:
    deleted_measurements: int
    deleted_imports: int
    deleted_meters: int