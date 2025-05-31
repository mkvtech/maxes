from __future__ import annotations
import datetime
import itertools
import logging
import networkx as nx
import numpy as np
import pandas as pd
import sklearn.ensemble
import sklearn.neighbors

import maxes.analyze_sequence
import maxes.graphs
import maxes.utils
from maxes.utils import action_logging
from maxes.xes_loader2 import XesLog, XesTrace, XesEvent

XES_LOG_ATTRIBUTES_EXCLUDED_FROM_RANDOM = ["concept:name", "lifecycle:transition", "time:timestamp"]

class KdeForTimeDeltas:
    def __init__(self, only_non_negative=True):
        self.only_non_negative = only_non_negative

    def fit(self, data):
        # TODO: Use appropriate conversion from timedelta to float based on delta = max(data) - min(data)
        data_1d = [time_delta.seconds for time_delta in data]

        min_value, max_value = min(data_1d), max(data_1d)
        bandwidth = (max_value - min_value) * 0.05

        if bandwidth <= 0.0:
            bandwidth = 1.0 # default

        data_2d = [[seconds] for seconds in data_1d]
        self.kde_ = sklearn.neighbors.KernelDensity(bandwidth=bandwidth).fit(data_2d)

        return self

    def sample(self, n_samples=1):
        seconds = [item[0] for item in self.kde_.sample(n_samples)]

        if self.only_non_negative:
            seconds = [max(0, item) for item in seconds]

        time_deltas = [datetime.timedelta(seconds=item) for item in seconds]
        return time_deltas


class KdeForTimeStamps1:
    def __init__(self):
        pass

    def fit(self, data):
        data_1d = [date.timestamp() for date in data]
        self.min_max_range_ = [min(data_1d), max(data_1d)]

        data_2d = [[date] for date in data_1d]
        self.kde_ = sklearn.neighbors.KernelDensity().fit(data_2d)

        return self

    def sample(self, n_samples=1):
        return [datetime.datetime.fromtimestamp(item[0], tz=datetime.timezone.utc) for item in self.kde_.sample(n_samples)]


class XesGenerator1:
    def __init__(
            self,
            traces_count: int | None = None,
            random_seed=None,
            debug=False) -> None:
        self.traces_count = traces_count
        self.rng = np.random.default_rng(random_seed)
        self.debug = debug

    # region Fitting

    def fit(self, log: XesLog) -> XesGenerator1:

        # TODO: Validate that log events have required attributes:
        # "concept:name", "lifecycle:transition", "time:timestamp"

        with action_logging("Analysing sequence graph", self.debug):
            self.sequence_graph_ = maxes.analyze_sequence.analyze_xes_log_sequence(log)

        with action_logging("Gathering meta data"):
            if self.traces_count is None:
                self.traces_count = len(log.traces)

            traces_lengths = [len(trace.events) for trace in log.traces]
            self.trace_length_range_ = (min(traces_lengths), max(traces_lengths))

            self.log_df_ = pd.concat(trace.df for trace in log.traces)

            trace_beginning_timestamps_ = [trace.events[0].time_timestamp for trace in log.traces]
            self.trace_beginning_timestamp_generator_ = KdeForTimeStamps1().fit(trace_beginning_timestamps_)

        with action_logging("Fittig models for time:timestamp attribute"):
            for transition, transition_attributes in self.sequence_graph_.edges.items():
                durations = transition_attributes["transition_durations"]
                generator = KdeForTimeDeltas().fit(durations)
                generator.fit(durations)
                transition_attributes["duration_generator"] = generator

        if self.debug: logging.info("Fitting models for other attributes")

        with action_logging("Fitting models for other attributes"):
            # Numerical attributes
            self.numerical_attributes = [attribute
                                    for attribute, attr_type in log.event_attribute_type_map.items()
                                    if attr_type in ["date", "int", "float"] and
                                    attribute not in XES_LOG_ATTRIBUTES_EXCLUDED_FROM_RANDOM]
            self.numerical_event_attribute_ranges_: dict[str, (int, int)] = {}
            for attribute in self.numerical_attributes:
                min_value = self.log_df_.loc[:, attribute].min()
                max_value = self.log_df_.loc[:, attribute].max()
                self.numerical_event_attribute_ranges_[attribute] = (min_value, max_value)

            # Categorical attributes
            self.categorical_attributes = [attribute
                                    for attribute, attr_type in log.event_attribute_type_map.items()
                                    if attr_type in ["string", "id", "bool"] and
                                    attribute not in XES_LOG_ATTRIBUTES_EXCLUDED_FROM_RANDOM]
            self.categorical_event_attribute_frequencies_: dict[str, dict[str, int]] = {}
            for attribute in self.categorical_attributes:
                counts = self.log_df_.loc[:, attribute].value_counts().to_dict()
                self.categorical_event_attribute_frequencies_[attribute] = counts

        # Other
        self.log_attribute_type_map = log.log_attribute_type_map
        self.trace_attribute_type_map = log.trace_attribute_type_map
        self.event_attribute_type_map = log.event_attribute_type_map

        return self

    # region Generation

    def sample(self, n_samples=1) -> list[XesLog]:
        return [self.generate() for i in range(n_samples)]

    def generate(self) -> XesLog:
        log = XesLog()

        log.log_attribute_type_map = self.log_attribute_type_map
        log.trace_attribute_type_map = self.trace_attribute_type_map
        log.event_attribute_type_map = self.event_attribute_type_map

        trace_length_range = self.trace_length_range_

        for i in range(self.traces_count):
            trace = XesTrace()
            log.traces.append(trace)

            for j in range(3):
                try:
                    generated_events_sequence: list[list[str]] = maxes.graphs.random_weighted_traverse(
                        graph=self.sequence_graph_,
                        min_steps=trace_length_range[0],
                        max_steps=trace_length_range[1],
                        weight_feature_name="frequency",
                    )
                    break
                except maxes.utils.CustomStackOverflowException as e:
                    new_trace_length_range = self._extend_trace_length_range(trace_length_range)
                    logging.info(f"Failed to generate events sequence with trace length in {trace_length_range}, will extend range to {new_trace_length_range} and try again.")
                    trace_length_range = new_trace_length_range
            else:
                logging.info(trace_length_range)
                raise RuntimeError("Gave up after extending trace length range multiple times")

            # Assign concept:name and lifecycle:transition
            for event_sequence_item in generated_events_sequence:
                event = XesEvent()
                trace.events.append(event)

                # concept:name and lifecycle:transition
                concept_name, lifecycle_transition = event_sequence_item
                event.attributes["concept:name"] = concept_name
                event.attributes["lifecycle:transition"] = lifecycle_transition

            # Assign time:timestamp
            trace.events[0].attributes["time:timestamp"] = self.trace_beginning_timestamp_generator_.sample()[0]
            for current_event, next_event in itertools.pairwise(trace.events):
                edge = (
                    XesGenerator1._get_sequence_graph_node_key(current_event),
                    XesGenerator1._get_sequence_graph_node_key(next_event),
                )
                duration_generator = self.sequence_graph_.edges[edge]["duration_generator"]
                sample_duration = duration_generator.sample()[0]
                next_event.attributes["time:timestamp"] = current_event.time_timestamp + sample_duration

            # Other attributes
            for event in trace.events:
                # Numerical attributes
                for attribute, value_range in self.numerical_event_attribute_ranges_.items():
                    value = self.rng.integers(low=value_range[0], high=value_range[1], endpoint=True)
                    event.attributes[attribute] = value

                # Categorical attributes
                for attribute, categories_frequencies in self.categorical_event_attribute_frequencies_.items():
                    event.attributes[attribute] = maxes.utils.choice(categories_frequencies)

        return log

    def _get_sequence_graph_node_key(event: XesEvent):
        return (event["concept:name"], event["lifecycle:transition"])

    def _extend_trace_length_range(self, range):
        r_min, r_max = range

        new_min = None
        if r_min < 1:
            new_min = 1
        else:
            new_min = round(r_min * 0.9)
            new_min = new_min - 1 if new_min == r_min else new_min

        new_max = round(r_max * 1.1)
        new_max = new_max + 1 if new_max == r_max else new_max

        return (new_min, new_max)
