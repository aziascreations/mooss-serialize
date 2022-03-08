# Imports
from enum import IntEnum, auto


# Enumerations
class EFieldType(IntEnum):
    """
    Enumeration of basic summaries used when deserializing fields to chose what to do with them without doing a
    second computationally expensive analysis.
    
    Should not be used outside this package !
    """
    FIELD_TYPE_UNKNOWN = auto()
    FIELD_TYPE_PRIMITIVE = auto()
    FIELD_TYPE_ITERABLE = auto()
    FIELD_TYPE_SERIALIZABLE = auto()
