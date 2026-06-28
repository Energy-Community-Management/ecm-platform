from datetime import datetime, timedelta
from collections import defaultdict

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

    def total_energy_kwh(self) -> float:
        return sum(item.value_kwh for item in self._measurements)

    def average_energy_kwh(self) -> float:
        if self.is_empty():
            return 0.0
        return self.total_energy_kwh() / self.count()

    def max_energy_kwh(self) -> float:
        if self.is_empty():
            return 0.0
        return max(item.value_kwh for item in self._measurements)

    def min_energy_kwh(self) -> float:
        if self.is_empty():
            return 0.0
        return min(item.value_kwh for item in self._measurements)

    def daily_totals(self) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)

        for measurement in self._measurements:
            day_key = measurement.start.strftime("%Y-%m-%d")
            totals[day_key] += measurement.value_kwh

        return dict(totals)

    def monthly_totals(self) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)

        for measurement in self._measurements:
            month_key = measurement.start.strftime("%Y-%m")
            totals[month_key] += measurement.value_kwh

        return dict(totals)

    def start(self) -> datetime:
        return self._measurements[0].start

    def end(self) -> datetime:
        return self._measurements[-1].end

    def period(self) -> timedelta:
        return self.end() - self.start()

    def first(self) -> EnergyMeasurement:
        return self._measurements[0]

    def last(self) -> EnergyMeasurement:
        return self._measurements[-1]

    def is_empty(self) -> bool:
        return len(self._measurements) == 0

    def __len__(self) -> int:
        return len(self._measurements)

    def __getitem__(self, index: int) -> EnergyMeasurement:
        return self._measurements[index]

    def __iter__(self):
        return iter(self._measurements)