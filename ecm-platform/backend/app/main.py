from pathlib import Path
import logging

from app.imports.ote.parser import OTEParser

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main():

    base_dir = Path(__file__).resolve().parent.parent

    csv_file = (
            base_dir
            / "data"
            / "input"
            / "pnd_export (15).csv"
    )

    parser = OTEParser()

    series = parser.load_15min_profile(csv_file)

    logger.info("Počet měření: %d", series.count())
    logger.info("Období: %s -> %s", series.start(), series.end())
    logger.info("Celkem energie: %.4f kWh", series.total_energy())
    logger.info("První měření: %s", series[0])


if __name__ == "__main__":
    main()