from abc import ABC, abstractmethod

from app.domain.energy_series import EnergySeries
from app.quality.models.validation_report import ValidationReport


class BaseRule(ABC):
    @abstractmethod
    def validate(
        self,
        series: EnergySeries,
        report: ValidationReport,
    ) -> None:
        pass