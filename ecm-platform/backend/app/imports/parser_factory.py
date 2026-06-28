from app.domain.import_info import ImportInfo
from app.domain.enums.vendor import Vendor
from app.domain.enums.data_type import DataType

from app.imports.parsers.ote.parser import OTEParser


class ParserFactory:
    """Vrací správný parser podle typu importu."""

    def get_parser(self, info: ImportInfo):
        if info.vendor is Vendor.OTE:
            if info.data_type in (
                DataType.PROFILE_15MIN,
                DataType.MONTHLY_SUMMARY,
            ):
                return OTEParser()

        raise ValueError(
            f"Pro import neexistuje parser: "
            f"{info.vendor.value} / {info.data_type.value}"
        )