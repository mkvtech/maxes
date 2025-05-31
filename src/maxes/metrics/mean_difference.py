from functools import reduce
import typing
import pandas as pd

from maxes.constants import CONCEPT_NAME, LIFECYCLE_TRANSITION
from maxes.utils import noop


def find_matching_events(
    events: pd.DataFrame, event: pd.Series, identification_columns: list[str]
):
    id_mask = [events[column] == event[column] for column in identification_columns]
    id_mask = reduce(lambda a, b: a & b, id_mask)
    return events[id_mask]


def find_best_score_categorical(
    original_df: pd.DataFrame,
    event: pd.Series,
    identification_columns: list[str],
    weights: pd.Series,
):
    matching_events = find_matching_events(original_df, event, identification_columns)

    if len(matching_events) == 0:
        return None, None, None

    matching_events_data = matching_events[weights.keys()]
    event_data = event[weights.keys()]

    similarities = (matching_events_data == event_data) | (
        (matching_events_data != matching_events_data) & (event_data != event_data)
    )

    diffs = ~similarities
    diffs = diffs.astype(int)
    diffs = diffs * weights

    scores = diffs.sum(axis=1) / weights.sum()

    best_score_index = scores.idxmin()

    score = scores.loc[best_score_index]

    return score, diffs, best_score_index


def compute_best_match_categorical(
    original_df: pd.DataFrame,
    generated_df: pd.DataFrame,
    identification_columns: list[str] = [CONCEPT_NAME, LIFECYCLE_TRANSITION],
    difference_columns: list[str] | None = None,
    weights: pd.Series | dict[str, float] | None = None,
    unidentified_event_penalty: int | None = None,
):
    """
    Parameters
    ----------
    unidentified_event_penalty : int, None
        Score to assign to a generated event, if there is no matching event in original_df. If None, will be computed from sum of weights.
    """
    if weights is None and difference_columns is None:
        raise ValueError("Either difference_columns or weights must be present")

    if weights is None:
        weights = {column: 1 for column in difference_columns}
    else:
        difference_columns = list(weights.keys())

    if unidentified_event_penalty is None:
        unidentified_event_penalty = sum(weights.values())

    weights = pd.Series(weights)

    identification_columns = set(identification_columns)
    difference_columns = set(difference_columns)

    if identification_columns & difference_columns:
        raise ValueError(
            "identification_columns and difference_columns must not intersect"
        )

    all_columns = list(identification_columns | difference_columns)

    original_df = original_df[all_columns].reset_index(drop=True)
    generated_df = generated_df[all_columns].reset_index(drop=True)

    scores = []

    for generated_event_index, generated_event in generated_df.iterrows():
        score, diffs, best_score_index = find_best_score_categorical(
            original_df, generated_event, identification_columns, weights
        )

        if score is None:
            score = unidentified_event_penalty

        # print()
        # print()
        # print()
        # print("event")
        # print(generated_event)

        # print()
        # print("best score index")
        # print(best_score_index)

        # print()
        # print("matched event")
        # print(original_df.iloc[best_score_index])

        scores.append(score)

    mean_score = pd.Series(scores).mean()

    return mean_score


def find_best_score_numerical(
    original_df: pd.DataFrame,
    event: pd.Series,
    identification_columns: list[str],
    difference_weights: pd.Series,
):
    matching_events = find_matching_events(original_df, event, identification_columns)

    if len(matching_events) == 0:
        return None, None, None

    column_diffs = (
        matching_events[difference_weights.keys()] - event[difference_weights.keys()]
    )
    column_diffs = column_diffs.abs()

    # Normalize within each column's range
    column_diffs = column_diffs / column_diffs.max()

    column_diffs = column_diffs * difference_weights

    scores = column_diffs.sum(axis=1) / difference_weights.sum()
    best_score_index = scores.idxmin()

    # Note: best_score_index may be greater than len(scores)
    # because best_score_index is index of original_df, not matching_events
    # It is important to use .loc and not .iloc
    score = scores.loc[best_score_index]

    return score, column_diffs, best_score_index


def compute_best_match_numerical(
    original_log: pd.DataFrame,
    generated_log: pd.DataFrame,
    difference_columns: list[str],
    weights: dict[str, float] | None = None,
    identification_columns: list[str] = [CONCEPT_NAME, LIFECYCLE_TRANSITION],
    unidentified_event_penalty: int | None = None,
):
    if weights is None and difference_columns is None:
        raise ValueError("Either difference_columns or weights must be present")

    if weights is None:
        weights = {column: 1 for column in difference_columns}
    else:
        difference_columns = list(weights.keys())

    if unidentified_event_penalty is None:
        unidentified_event_penalty = sum(weights.values())

    weights = pd.Series(weights)

    identification_columns = set(identification_columns)
    difference_columns = set(difference_columns)

    if identification_columns & difference_columns:
        raise ValueError(
            "identification_columns and difference_columns must not intersect"
        )

    all_columns = list(set(identification_columns) | set(difference_columns))

    original_df = original_log[all_columns].reset_index(drop=True)
    generated_df = generated_log[all_columns].reset_index(drop=True)

    # Validate same columns and column types
    if (original_df.dtypes != generated_df.dtypes).any():
        raise ValueError("Mismatching dtypes")

    generated_df_of_difference_columns = generated_df[list(difference_columns)]
    dtypes = generated_df_of_difference_columns.dtypes
    invalid_dtypes = list(generated_df_of_difference_columns.columns[dtypes != "float"])
    if len(invalid_dtypes):
        raise ValueError(
            f"All of identification columns must be converted to float. These identification columns have invalid dtype: {invalid_dtypes}"
        )

    scores = []
    for generated_event_index, generated_event in generated_df.iterrows():
        score, column_scores, best_score_index = find_best_score_numerical(
            original_df, generated_event, identification_columns, weights
        )

        if score is None:
            score = unidentified_event_penalty

        # print()
        # print()
        # print()
        # print("event")
        # print(generated_event)

        # print()
        # print("best score index")
        # print(best_score_index)

        # print()
        # print("matched event")
        # print(original_df.iloc[best_score_index])

        scores.append(score)

    mean_score = pd.Series(scores).mean()

    return mean_score
