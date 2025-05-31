import pandas as pd

from maxes.constants import (
    CASE_CONCEPT_NAME,
    CONCEPT_NAME,
    LIFECYCLE_TRANSITION,
    TIME_TIMESTAMP,
    SPECIAL_XES_ATTRIBUTES,
)

from maxes.generators.xes_generator.share import (
    AttributeLevelEnum,
    NumeralicityEnum,
)


def guess_xes_attributes_levels(df: pd.DataFrame) -> dict[str, AttributeLevelEnum]:
    custom_attributes = [a for a in df.columns if a not in SPECIAL_XES_ATTRIBUTES]

    nunique_per_trace = df.groupby(CASE_CONCEPT_NAME)[custom_attributes].nunique()

    computed_levels = {}
    for attribute in custom_attributes:
        is_trace_level = (nunique_per_trace[attribute] == 1).all()
        level = AttributeLevelEnum.TRACE if is_trace_level else AttributeLevelEnum.EVENT
        computed_levels[attribute] = level

    static_levels = {
        CASE_CONCEPT_NAME: AttributeLevelEnum.EVENT,
        CONCEPT_NAME: AttributeLevelEnum.EVENT,
        LIFECYCLE_TRANSITION: AttributeLevelEnum.EVENT,
        TIME_TIMESTAMP: AttributeLevelEnum.EVENT,
    }

    return computed_levels | static_levels


def guess_numeralicity(
    df: pd.DataFrame, event_level_attributes: list[str], threshold: float = 0.9
) -> dict[str, NumeralicityEnum]:
    # All column values match regex of an integer / float
    # {threshold}% of values are unique
    raise NotImplementedError()

    # custom_attributes = [a for a in df.columns if a not in SPECIAL_XES_ATTRIBUTES]
    # other_attributes = list(set(df.columns) - set(SPECIAL_XES_ATTRIBUTES))

    # event_level_custom_attributes = [
    #     a for a in custom_attributes if a in event_level_attributes
    # ]
    # trace_level_custom_attributes = [
    #     a for a in custom_attributes if a not in event_level_attributes
    # ]

    # nunique_per_log = df[custom_attributes].nunique()
    # nunique_per_trace = df.groupby(CASE_CONCEPT_NAME)[custom_attributes].nunique()

    # result = {}

    # for attribute in event_level_custom_attributes:


def expand_integer_range(range: tuple[int, int], amount: float) -> tuple[int, int]:
    r_min, r_max = range

    new_min = round(r_min * (1 - amount))
    new_min = new_min - 1 if new_min == r_min else new_min
    new_min = max(new_min, 1)

    new_max = round(r_max * (1 + amount))
    new_max = new_max + 1 if new_max == r_max else new_max

    return (new_min, new_max)


# trace unique identifier
def guess_unique_per_trace_attributes(df: pd.DataFrame) -> list[str]:
    """
    Returns list of attributes that are maintain the same value within a trace, but have different values in each trace
    """
    other_attributes = list(set(df.columns) - set(SPECIAL_XES_ATTRIBUTES))
    nunique_per_trace = df.groupby(CASE_CONCEPT_NAME)[other_attributes].nunique()
    traces_count = df.groupby(CASE_CONCEPT_NAME).count()
    nunique_per_log = df[other_attributes].nunique()

    result = []
    for attribute in other_attributes:
        is_trace_level = len(nunique_per_trace[attribute].value_counts()) == 1
        is_unique_per_log = nunique_per_log[attribute] == traces_count
        print(attribute)
        if is_trace_level and is_unique_per_log:
            result.append(attribute)

    return result
