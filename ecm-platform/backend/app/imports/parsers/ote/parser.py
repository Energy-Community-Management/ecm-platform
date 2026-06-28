from pathlib import Path
from datetime import datetime, timedelta
import csv

from app.domain.energy_series import EnergySeries
from app.domain.measurement import EnergyMeasurement
from app.utils.converters import parse_kwh, parse_kw


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%d.%m.%Y %H:%M")


def parse_profile_datetime(value: str) -> datetime:
    if " 24:" in value:
        fixed = value.replace(" 24:", " 00:")
        return (
            datetime.strptime(
                fixed,
                "%d.%m.%Y %H:%M:%S",
            )
            + timedelta(days=1)
        )

    return datetime.strptime(
        value,
        "%d.%m.%Y %H:%M:%S",
    )


class OTEParser:
    """Parser exportů OTE."""

    def load_rows(self, file_path: Path) -> list[dict]:
        with open(
            file_path,
            mode="r",
            encoding="cp1250",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(
                csv_file,
                delimiter=";",
            )

            return list(reader)

    def load_monthly_summary(
        self,
        file_path: Path,
    ) -> EnergySeries:

        rows = self.load_rows(file_path)

        measurements: list[EnergyMeasurement] = []

        for row in rows:

            measurements.append(
                EnergyMeasurement(
                    start=parse_datetime(row["Datum od"]),
                    end=parse_datetime(row["Datum do"]),
                    source=row["Datová řada"],
                    value_kwh=parse_kwh(
                        row["Celkem v intervalu"]
                    ),
                )
            )

        return EnergySeries(measurements)

    def load_15min_profile(
        self,
        file_path: Path,
    ) -> EnergySeries:

        rows = self.load_rows(file_path)

        value_column = next(
            column
            for column in rows[0].keys()
            if "[kW]" in column
        )

        measurements: list[EnergyMeasurement] = []

        for row in rows:

            end = parse_profile_datetime(row["Datum"])
            start = end - timedelta(minutes=15)

            kw = parse_kw(row[value_column])

            measurements.append(
                EnergyMeasurement(
                    start=start,
                    end=end,
                    source=value_column,
                    value_kwh=kw * 0.25,
                    status=row.get("Status", ""),
                )
            )

        return EnergySeries(measurements)