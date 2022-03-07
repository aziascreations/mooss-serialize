# Imports
from enum import IntEnum, auto


# Enumerations
class EFieldType(IntEnum):
    FIELD_TYPE_UNKNOWN = auto()
    FIELD_TYPE_PRIMITIVE = auto()
    FIELD_TYPE_ITERABLE = auto()
    FIELD_TYPE_SERIALIZABLE = auto()
