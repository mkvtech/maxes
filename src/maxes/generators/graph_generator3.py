from __future__ import annotations
import pandas as pd
import typing

from maxes.xes_file import XesFile

import maxes.analyze_sequence


class GraphGenerator3:
    def __init__(
            self,
            n_max_events: int,
            n_min_events: int = 0,
            df_filter: typing.Callable[[pd.DataFrame], pd.DataFrame] | None = None,
            sequence_keys: str | list[str] = ["concept:name", "lifecycle:transition"]
    ):
        self.n_min_events = n_min_events
        self.n_max_events = n_max_events
        self.df_filter = (lambda df: df) if df_filter is None else df_filter
        self.sequence_keys = sequence_keys
        pass

    def fit(self, xes: XesFile) -> GraphGenerator3:
        self.sequences_ = []
        for trace in xes.traces:
            df = self.df_filter(trace.df)
            sequence = maxes.analyze_sequence.analyze_sequence(df, sequence_keys=self.sequence_keys)
            self.sequences_.append(sequence)

        self.sequence_ = maxes.analyze_sequence.merge_graphs(
            self.sequences_, resolve_edge_conflict="add", resolve_node_conflict="add")

        self.tree_ = maxes.analyze_sequence.traverse_all_pathes(
            sequence=self.sequence_,
            # For N events there are N-1 steps between events
            min_steps=self.n_min_events - 1,
            max_steps=self.n_max_events - 1)

        return self

    def generate(self) -> list[str]:
        return maxes.analyze_sequence.random_weighted_tree_path(
            self.tree_, weight_feature="frequency")
