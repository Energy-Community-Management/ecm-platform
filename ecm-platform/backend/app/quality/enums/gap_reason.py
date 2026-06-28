from enum import Enum


class GapReason(Enum):
    UNKNOWN = "UNKNOWN"
    MISSING_DATA = "MISSING_DATA"
    DST_FORWARD = "DST_FORWARD"
    DST_BACKWARD = "DST_BACKWARD"