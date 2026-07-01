from enum import Enum


class ImportStatus(Enum):
    IMPORTING = "IMPORTING"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    FAILED = "FAILED"