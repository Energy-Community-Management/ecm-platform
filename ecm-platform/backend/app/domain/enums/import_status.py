from enum import Enum


class ImportStatus(Enum):
    RECEIVED = "RECEIVED"

    VALIDATED = "VALIDATED"

    PROCESSED = "PROCESSED"

    READY = "READY"

    FAILED = "FAILED"