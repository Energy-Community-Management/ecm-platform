from pathlib import Path

from app.imports.ote.parser import OTEParser
from app.imports.ote.parser import parse_kwh


def main():

    parser = OTEParser()

    BASE_DIR = Path(__file__).resolve().parents[1]

    csv_file = BASE_DIR / "data" / "input" / "pnd_export.csv"

    rows = parser.load(csv_file)

    print(len(rows))

    print(rows[0])
    energy = parse_kwh(rows[0]["Celkem v intervalu"])
    print(energy)

if __name__ == "__main__":
    main()