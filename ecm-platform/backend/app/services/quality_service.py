from app.domain.energy_series import EnergySeries
from app.quality.models.validation_report import ValidationReport
from app.quality.rules.missing_interval_rule import MissingIntervalRule


class QualityService:

    def __init__(self) -> None:

        self.rules = [
            MissingIntervalRule(),
        ]

    def validate(
        self,
        series: EnergySeries,
    ) -> ValidationReport:

        report = ValidationReport(
            completeness=100.0,
            expected_intervals=0,
            missing_intervals_count=0,
        )

        for rule in self.rules:
            rule.validate(series, report)

        self._calculate_statistics(series, report)

        return report

    def _calculate_statistics(
        self,
        series: EnergySeries,
        report: ValidationReport,
    ) -> None:

        missing_intervals = 0

        for gap in report.missing_intervals:
            missing_intervals += int(
                gap.duration.total_seconds() / (15 * 60)
            )

        report.missing_intervals_count = missing_intervals

        report.expected_intervals = (
            series.count()
            + missing_intervals
        )

        if report.expected_intervals == 0:
            report.completeness = 100.0
        else:
            report.completeness = round(
                series.count()
                / report.expected_intervals
                * 100,
                2,
            )