from pathlib import Path
from datetime import datetime, timedelta
import csv

from app.domain.measurement import EnergyMeasurement
from app.shared.converters import parse_kwh, parse_kw



def parse_profile_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%d.%m.%Y %H:%M:%S")


def parse_profile_datetime(value: str) -> datetime:
    if " 24:" in value:
        fixed_value = value.replace(" 24:", " 00:")
        return datetime.strptime(fixed_value, "%d.%m.%Y %H:%M:%S") + timedelta(days=1)

    return datetime.strptime(value, "%d.%m.%Y %H:%M:%S")


class OTEParser:
    """Parser CSV exportů z OTE."""

    def load_rows(self, file_path: Path) -> list[dict]:
        with open(file_path, mode="r", encoding="cp1250", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            return list(reader)

    def load_records(self, file_path: Path) -> list[EnergyMeasurement]:
        rows = self.load_rows(file_path)

        records: list[EnergyMeasurement] = []

        for row in rows:
            record = EnergyMeasurement(
                start=parse_datetime(row["Datum od"]),
                end=parse_datetime(row["Datum do"]),
                source=row["Datová řada"],
                value_kwh=parse_kwh(row["Celkem v intervalu"]),
            )
            records.append(record)

        return records

    def load_15min_profile(self, file_path: Path) -> list[EnergyMeasurement]:
        rows = self.load_rows(file_path)

        columns = rows[0].keys()
        value_column = next(column for column in columns if "[kW]" in column)

        records: list[EnergyMeasurement] = []

        for row in rows:
            end = parse_profile_datetime(row["Datum"])
            start = end - timedelta(minutes=15)

            kw = parse_kw(row[value_column])
            kwh = kw * 0.25

            records.append(
                EnergyMeasurement(
                    start=start,
                    end=end,
                    source=value_column,
                    value_kwh=kwh,
                    status=row.get("Status", ""),
                )
            )

        return records