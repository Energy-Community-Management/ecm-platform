from pathlib import Path
from datetime import datetime
import csv

from app.domain.measurement import EnergyMeasurement
from app.shared.converters import parse_kwh

def parse_kwh(value: str) -> float:
    value = value.replace(" kWh", "")
    value = value.replace(" ", "")
    value = value.replace(",", ".")
    return float(value)


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%d.%m.%Y %H:%M")


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