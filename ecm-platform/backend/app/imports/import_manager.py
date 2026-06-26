from pathlib import Path

from app.core.energy_series import EnergySeries
from app.imports.detector import ImportDetector
from app.imports.ote.parser import OTEParser


class ImportManager:

    def __init__(self):

        self.detector = ImportDetector()

    def import_file(
        self,
        file_path: Path,
    ) -> EnergySeries:

        file_type = self.detector.detect(file_path)

        if file_type == "OTE_15MIN_PROFILE":

            parser = OTEParser()

            return parser.load_15min_profile(file_path)

        if file_type == "OTE_MONTHLY_SUMMARY":

            parser = OTEParser()

            return parser.load_monthly_summary(file_path)

        raise ValueError(
            f"Nepodporovaný typ souboru: {file_type}"
        )