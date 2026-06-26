import logging
from pathlib import Path

from app.imports.ote.parser import OTEParser


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    csv_file = base_dir / "data" / "input" / "pnd_export.csv"

    parser = OTEParser()
    records = parser.load_records(csv_file)

    total_kwh = sum(record.value_kwh for record in records)

    logger.info("Načteno záznamů: %d", len(records))
    logger.info("Celkem energie: %.4f kWh", total_kwh)


if __name__ == "__main__":
    main()