from datetime import timedelta

from app.domain.energy_series import EnergySeries


class EnergyValidationService:
    """Validace energetických časových řad."""

    EXPECTED_INTERVAL = timedelta(minutes=15)

    def find_missing_intervals(self, series: EnergySeries) -> list[tuple]:

        missing: list[tuple] = []

        measurements = series.measurements

        if len(measurements) < 2:
            return missing

        for previous, current in zip(measurements, measurements[1:]):

            expected_start = previous.end

            if current.start != expected_start:
                missing.append(
                    (
                        previous.end,
                        current.start,
                        current.start - previous.end,
                    )
                )
        return missing

    def completeness(self, series: EnergySeries) -> float:

        if len(series) < 2:
            return 100.0

        expected = int(
            series.period() / self.EXPECTED_INTERVAL
        )

        if expected == 0:
            return 100.0

        return round(
            series.count() / expected * 100,
            2,
        )