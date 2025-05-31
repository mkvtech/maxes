import itertools
import Levenshtein
import pandas as pd
import typing

from maxes.xes_loader2 import XesLog, XesTrace


class TraceSequence:
    index: int
    trace: XesTrace
    sequence: list[list[str]]

    def __init__(self, index, trace, sequence):
        self.index = index
        self.trace = trace
        self.sequence = sequence


class TracesPair(typing.NamedTuple):
    original_sequence: TraceSequence
    generated_sequence: TraceSequence
    score: float


def mean_levenstein_distance(original_log: XesLog, generated_log: XesLog, keys: list[str] = ['concept:name', 'lifecycle:transition']):
    original_sequences = _extract_sequences(original_log, keys=keys)
    generated_sequences = _extract_sequences(generated_log, keys=keys)

    pairs_scores: list[TracesPair] = []

    for original_sequence, generated_sequence in itertools.product(original_sequences, generated_sequences):
        score = Levenshtein.ratio(original_sequence.sequence, generated_sequence.sequence)

        item = TracesPair(
            original_sequence=original_sequence,
            generated_sequence=generated_sequence,
            score=score
        )

        pairs_scores.append(item)

    best_pairs_scores: list[TracesPair] = []

    while len(pairs_scores) > 0:
        # find best scored pair
        best_pair = max(pairs_scores, key=lambda item: item.score)
        best_pairs_scores.append(best_pair)

        # Remove all pairs containing first or second sequence

        pairs_scores = [
            pair_and_score
            for pair_and_score in pairs_scores
            if pair_and_score.original_sequence.index != best_pair.original_sequence.index and
            pair_and_score.generated_sequence.index != best_pair.generated_sequence.index
        ]

    return best_pairs_scores


def _extract_sequences(log: XesLog, keys: list[str] = ['concept:name', 'lifecycle:transition']) -> list[TraceSequence]:
    sequences = []

    for index, trace in enumerate(log.traces):
        sequence = df_to_sequence(trace.df, keys)
        trace_sequence = TraceSequence(index, trace, sequence)
        sequences.append(trace_sequence)

    return sequences


def df_to_sequence(df: pd.DataFrame, keys: list[str] = ['concept:name', 'lifecycle:transition']):
    # Returns list of tuples: [(), (), (), ...]
    return list(df[keys].itertuples(index=False, name=None))
