from datetime import timedelta

from app.domain.energy_series import EnergySeries
from app.domain.missing_interval import MissingInterval


class EnergyValidationService:
    """Validace energetických časových řad."""

    EXPECTED_INTERVAL = timedelta(minutes=15)

    def find_missing_intervals(self, series: EnergySeries) -> list[MissingInterval]:
        missing: list[MissingInterval] = []

        measurements = series.measurements

        if len(measurements) < 2:
            return missing

        for previous, current in zip(measurements, measurements[1:]):
            expected_start = previous.end

            if current.start > expected_start:
                missing.append(
                    MissingInterval(
                        start=previous.end,
                        end=current.start,
                        duration=current.start - previous.end,
                    )
                )

        return missing

    def missing_intervals_count(self, series: EnergySeries) -> int:
        missing = self.find_missing_intervals(series)

        count = 0

        for gap in missing:
            count += int(
                gap.duration.total_seconds()
                / self.EXPECTED_INTERVAL.total_seconds()
            )

        return count

    def expected_intervals_count(self, series: EnergySeries) -> int:
        return series.count() + self.missing_intervals_count(series)

    def completeness(self, series: EnergySeries) -> float:
        expected = self.expected_intervals_count(series)

        if expected == 0:
            return 100.0

        return round(series.count() / expected * 100, 2)