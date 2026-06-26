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
    csv_file = base_dir / "data" / "input" / "pnd_export (15).csv"

    parser = OTEParser()
    records = parser.load_15min_profile(csv_file)

    total_kwh = sum(record.value_kwh for record in records)

    logger.info("Načteno 15min záznamů: %d", len(records))
    logger.info("První záznam: %s", records[0])
    logger.info("Celkem energie: %.4f kWh", total_kwh)


if __name__ == "__main__":
    main()