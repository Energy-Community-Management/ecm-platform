from __future__ import annotations

from datetime import datetime

from app.domain.measurement import EnergyMeasurement


class EnergySeries:
    """Časová řada energetických měření."""

    def __init__(self, measurements: list[EnergyMeasurement]) -> None:
        self._measurements = sorted(
            measurements,
            key=lambda measurement: measurement.start,
        )

    @property
    def measurements(self) -> list[EnergyMeasurement]:
        return self._measurements

    def count(self) -> int:
        return len(self._measurements)

    def total_energy(self) -> float:
        return sum(
            measurement.value_kwh
            for measurement in self._measurements
        )

    def start(self) -> datetime:
        return self._measurements[0].start

    def end(self) -> datetime:
        return self._measurements[-1].end

    def __len__(self) -> int:
        return len(self._measurements)

    def __getitem__(self, index: int) -> EnergyMeasurement:
        return self._measurements[index]

    def __iter__(self):
        return iter(self._measurements)