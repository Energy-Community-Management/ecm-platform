from enum import Enum


class ImportType(Enum):
    UNKNOWN = "UNKNOWN"

    ENERGY = "ENERGY"

    WEATHER = "WEATHER"

    PRICE = "PRICE"

    CONFIGURATION = "CONFIGURATION"