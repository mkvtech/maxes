from enum import Enum


class AttributeLevelEnum(Enum):
    EVENT = "event"
    TRACE = "trace"
    LOG = "log"


class NumeralicityEnum(Enum):
    CATEGORICAL = "categorical"
    NUMERICAL = "numerical"
