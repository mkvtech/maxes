from __future__ import annotations
import pandas as pd
import random
import typing

from src.xes.xes_file import XesFile

import src.xes.analyze_sequence

class GraphGenerator1:
    def __init__(
            self,
            n_max_events: int,
            df_filter: typing.Callable[[pd.DataFrame], pd.DataFrame] | None = None,
            sequence_keys: str | list[str] = ["concept:name", "lifecycle:transition"]
            ):
        self.n_max_events = n_max_events
        self.df_filter = (lambda df: df) if df_filter is None else df_filter
        self.sequence_keys = sequence_keys
        pass

    def fit(self, xes: XesFile) -> GraphGenerator1:
        self.sequences_ = []
        for trace in xes.traces:
            df = self.df_filter(trace.df)
            sequence = src.xes.analyze_sequence.analyze_sequence(df, sequence_keys=self.sequence_keys)
            self.sequences_.append(sequence)

        self.sequence_ = src.xes.analyze_sequence.merge_graphs(
            self.sequences_, resolve_edge_conflict="add", resolve_node_conflict="add")

        return self

    def generate(self) -> list[str]:
        possible_first_events = [node
                                 for node, data in self.sequence_.nodes.items()
                                 if data.get("first")]
        first_event = random.choice(possible_first_events)
        generated = [first_event]

        for i in range(self.n_max_events):
            event = generated[i]
            next_events_with_weights = {node: data["frequency"]
                                        for node, data in self.sequence_[event].items()}

            if len(next_events_with_weights) == 0: break

            next_event = src.utils.choice(next_events_with_weights)
            generated.append(next_event)

        return generated
