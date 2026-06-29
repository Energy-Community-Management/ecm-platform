from datetime import timedelta

from app.domain.energy_series import EnergySeries
from app.quality.enums.gap_reason import GapReason
from app.quality.enums.validation_severity import ValidationSeverity
from app.quality.models.missing_interval import MissingInterval
from app.quality.models.validation_report import ValidationReport
from app.quality.rules.base_rule import BaseRule


class MissingIntervalRule(BaseRule):
    EXPECTED_INTERVAL = timedelta(minutes=15)

    def validate(
        self,
        series: EnergySeries,
        report: ValidationReport,
    ) -> None:
        measurements = series.measurements

        if len(measurements) < 2:
            return

        for previous, current in zip(measurements, measurements[1:]):
            if current.start > previous.end:
                duration = current.start - previous.end
                reason = self._classify_gap(previous.end, duration)

                report.missing_intervals.append(
                    MissingInterval(
                        start=previous.end,
                        end=current.start,
                        duration=duration,
                        reason=reason,
                        severity=self._severity_for_reason(reason),
                    )
                )

    def _classify_gap(self, start, duration: timedelta) -> GapReason:
        if (
            start.month == 3
            and start.weekday() == 6
            and start.hour == 1
            and duration == timedelta(hours=1)
        ):
            return GapReason.DST_FORWARD

        return GapReason.MISSING_DATA

    def _severity_for_reason(self, reason: GapReason) -> ValidationSeverity:
        if reason is GapReason.DST_FORWARD:
            return ValidationSeverity.INFO

        return ValidationSeverity.WARNING