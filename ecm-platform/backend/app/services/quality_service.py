from datetime import timedelta

from app.domain.energy_series import EnergySeries
from app.quality.models.missing_interval import MissingInterval
from app.quality.models.validation_report import ValidationReport
from app.quality.enums.gap_reason import GapReason
from app.quality.enums.validation_severity import ValidationSeverity


class QualityService:
    EXPECTED_INTERVAL = timedelta(minutes=15)

    def validate(self, series: EnergySeries) -> ValidationReport:
        missing = self.find_missing_intervals(series)

        expected = series.count() + self.missing_intervals_count(series)
        missing_count = self.missing_intervals_count(series)

        completeness = 100.0
        if expected > 0:
            completeness = round(series.count() / expected * 100, 2)

        return ValidationReport(
            completeness=completeness,
            expected_intervals=expected,
            missing_intervals_count=missing_count,
            missing_intervals=missing,
        )

    def find_missing_intervals(self, series: EnergySeries) -> list[MissingInterval]:
        missing: list[MissingInterval] = []

        measurements = series.measurements

        if len(measurements) < 2:
            return missing

        for previous, current in zip(measurements, measurements[1:]):
            expected_start = previous.end

            if current.start > expected_start:
                duration = current.start - previous.end
                reason = self._classify_gap(previous.end, current.start, duration)

                missing.append(
                    MissingInterval(
                        start=previous.end,
                        end=current.start,
                        duration=duration,
                        reason=reason,
                        severity=self._severity_for_reason(reason),
                    )
                )

        return missing

    def missing_intervals_count(self, series: EnergySeries) -> int:
        count = 0

        for gap in self.find_missing_intervals(series):
            count += int(
                gap.duration.total_seconds()
                / self.EXPECTED_INTERVAL.total_seconds()
            )

        return count

    def _classify_gap(
        self,
        start,
        end,
        duration: timedelta,
    ) -> GapReason:
        if (
            start.month == 3
            and start.weekday() == 6
            and start.hour == 1
            and duration == timedelta(hours=1)
        ):
            return GapReason.DST_FORWARD

        return GapReason.MISSING_DATA

    def _severity_for_reason(
        self,
        reason: GapReason,
    ) -> ValidationSeverity:
        if reason is GapReason.DST_FORWARD:
            return ValidationSeverity.INFO

        return ValidationSeverity.WARNING