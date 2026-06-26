from pathlib import Path
import csv


def parse_kwh(value: str) -> float:
    value = value.replace(" kWh", "")
    value = value.replace(",", ".")
    return float(value)


class OTEParser:
    """Parser CSV exportů z OTE."""

    def load(self, file_path: Path) -> list[dict]:
        with open(file_path, encoding="cp1250") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            return list(reader)