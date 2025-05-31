import numpy as np
import pandas as pd

from maxes.types import TEventsSequenceFlat

def all(xes1, xes2):
    # TODO:
    # dot of all events counts -> if 0 -> event streams have all the same events (good), if high, generated event streams has generated new unknown events (bad)
    # dot of all transitions count -> if 0, event streams have all the same transitions (good), if high, generated event stream has generated new unknown transitions (not gud, but maybe ok)
    # unknown transitions ratio -> if 0, event streams have all the same transitions (good), if high, generated event stream has generated new unknown transitions (not gud, but maybe ok)
    # ratio of incorrect start events
    # ratio of incorrect end events

    # sequence distances:
    # - levenstein distance
    # - earth mover's distance
    # - other

    pass

def xes_dot_product(first: pd.DataFrame, second: pd.DataFrame, keys=["concept:name"]):
    first_keys_frequences = first[keys].value_counts()
    second_keys_frequences = second[keys].value_count()

    return dot_product(first_keys_frequences, second_keys_frequences)

def dot_product(original: dict[any, float], generated: dict[any, float]) -> float:
    """Calculates normalized dot product of 2 dictionaries (aka cosine of an angle between them)

    Args:
        original (dict[any, float]): _description_
        generated (dict[any, float]): _description_

    Returns:
        float: _description_
    """
    s1, s2 = pd.Series(original), pd.Series(generated)
    s1, s2 = s1.align(s2, fill_value=0)
    a1, a2 = s1.to_numpy(), s2.to_numpy()
    return a1.dot(a2) / np.linalg.norm(a1) / np.linalg.norm(a2)

def incorrect_transitions_ratio(
        original: TEventsSequenceFlat,
        generated: TEventsSequenceFlat,
        use_counts = True
    ) -> float:
    """
    calculates ratio of unknown transitions to all transitions in 2 given graphs

    Parameters
    ----------
    original : dict[(str, str), int]
        Original dictionary of event transitions where key is tuple of (source, destination) and value is number of transitions
    generated : dict[(str, str), int]
        Generated dictionary of event transitions, structure is the same as `original`
    use_counts : bool
        Whether to use or ignore transition counts

    Returns
    -------
    out : float
        incorrect to all tranisitions ratio in range [0, 1]. if ratio is closer to 0 - means there are no unknown transitions.

    """

    if not use_counts:
        unknown_edges = set(generated.keys()) - set(original.keys())
        ratio = len(unknown_edges) / len(generated)
        return ratio

    unknown_transitions_count = 0

    for edge in generated.keys():
        if edge not in original:
            unknown_transitions_count += generated[edge]

    all_transitions_counts = sum(count for count in generated.values())

    return unknown_transitions_count / all_transitions_counts
