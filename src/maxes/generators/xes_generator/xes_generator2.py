from __future__ import annotations
import datetime
import itertools
import logging
import networkx as nx
import numpy as np
import pandas as pd
import random
import re
import sklearn.ensemble
import sklearn.neighbors
import typing

import maxes.analyze_sequence
import maxes.graphs
import maxes.utils
from maxes.xes_loader2 import XesLog, XesTrace, XesEvent
from maxes.models.simple_categorical_feature_picker import SimpleCategoricalFeaturePicker
from maxes.generators.xes_generator.event_feature import EventFeature, EventFeature2


XES_LOG_SPECIAL_ATTRIBUTES = ["concept:name", "lifecycle:transition", "time:timestamp"]
XES_LOG_ATTRIBUTES_EXCLUDED_FROM_RANDOM = ["concept:name", "lifecycle:transition", "time:timestamp"]


INDEPENDENT_FEATURE_GENERATION_MODEL = {
    "numerical": [
        sklearn.neighbors.KernelDensity
        # IncrementalGenerator
    ],
    "categorical": [
        SimpleCategoricalFeaturePicker
        # TransitionGraphGenerator
    ]
}
DEPENDENT_FEATURE_GENERATION_MODEL = {
    "numerical": [
        sklearn.ensemble.RandomForestRegressor
        # LinearRegression
    ],
    "categorical": [
        sklearn.ensemble.RandomForestClassifier
    ]
}

class KdeForTimeDeltas:
    def __init__(self):
        pass

    def fit(self, data):
        # TODO: Use appropriate conversion from timedelta to float based on delta = max(data) - min(data)
        data = [[time_delta.seconds] for time_delta in data]
        self.kde_ = sklearn.neighbors.KernelDensity().fit(data)
        return self

    def sample(self, n_samples=1):
        return [datetime.timedelta(seconds=item[0]) for item in self.kde_.sample(n_samples)]


class KdeForTimeStamps1:
    def __init__(self):
        pass

    def fit(self, data):
        data = [[date.timestamp()] for date in data]
        self.kde_ = sklearn.neighbors.KernelDensity().fit(data)
        return self

    def sample(self, n_samples=1):
        return [datetime.datetime.fromtimestamp(item[0]) for item in self.kde_.sample(n_samples)]


class KdeForTimeStamps2:
    def __init__(self):
        pass

    def fit(self, data):
        self.low_ = np.min(data)
        self.high_ = np.max(data)

        # TODO: Pick appropriate scale (seconds, days, etc.) when converting timedeltas to float, depending on delta:
        # delta = self.high_ - self.low_

        data = data - self.low_
        self.kde_ = sklearn.neighbors.KernelDensity().fit(data)

        return self

    def sample(self, n_samples=1):
        return self.kde_.sample(n_samples) + self.low_

class XesAttributeModel_Numerical_RandomRange: pass
class XesAttributeModel_Numerical_Kde: pass
class XesAttributeModel_Categorical_RandomByFrequency: pass
class XesAttributeModel_Categorical_RandomForest:
    """
    ```python
    model = XesAttributeModel_Categorical_RandomForest()

    X = [
        [0, 0],
        [1, 1],
        [2, 2],
        [3, 3],
    ]
    Y = ['a', 'b', 'c', 'd']
    model.fit(X, Y)

    X_test = [
        [0, 0],
        [2, 2]
    ]
    y_predict = model.predict(X_test)
    print(y_predict)
    # ['a', 'b']
    ```
    """
    pass

class XesAttributeModel_Categorical_FollowSequenceGraph:
    def __init__(self):
        pass

    def fit(self, data, attribute):
        pass

    def sample(self, value, n_samples=1):
        pass


# TODO: Attribute generation strats:
# pick_random_by_frequency (attribute: cat)
# pick_random_from_range (attribute: num)
# pick_random_from_kde (attribute: num)
# follow_sequence_graph (attribute: cat)
# predict_from_other (attribute: num, based_on: num), based_on can be other attribute or time diff from other event

# Heuristics:
# Email, address, phone number, color (name), color (html)
# etc...
class XesGenerator2:
    def __init__(self, random_seed=None, debug=False) -> None:
        self.rng = np.random.default_rng(random_seed)
        self.debug = debug

    # region Fitting

    def fit(self, log: XesLog, configuration = None) -> XesGenerator2:
        if self.debug: logging.info("Validating")

        # TODO: Validate that log events have required attributes:
        # "concept:name", "lifecycle:transition", "time:timestamp"

        if self.debug: logging.info("Analyzing sequence graph")

        self.sequence_graph_ = maxes.analyze_sequence.analyze_xes_log_sequence(log)

        if self.debug: logging.info("Gathering meta data")

        self.traces_count_ = len(log.traces)

        traces_lengths = [len(trace.events) for trace in log.traces]
        self.trace_length_range_ = (min(traces_lengths), max(traces_lengths))

        def combine_dfs():
            return pd.concat(trace.df for trace in log.traces)
        # self.log_df = pd.concat(trace.df for trace in log.traces)
        log_df = combine_dfs()

        trace_beginning_timestamps_ = [trace.events[0].time_timestamp for trace in log.traces]
        self.trace_beginning_timestamp_generator_ = KdeForTimeStamps1().fit(trace_beginning_timestamps_)

        if self.debug: logging.info("Analysing attributes types")

        # self._trace_attributes_info = {
        #     attribute: {
        #         "data_type": self._trace_attribute_type_map[attribute],
        #         "statistical_data_type": self._trace_attribute_type_map[attribute] in ["int"]
        #     }
        #     for attribute in self._trace_attribute_type_map.values()
        # }

        # "time:timestamp"
        if self.debug: logging.info("Fitting models for \"time:timestamp\" attribute")

        for transition, transition_attributes in self.sequence_graph_.edges.items():
            durations = transition_attributes["transition_durations"]
            generator = KdeForTimeDeltas().fit(durations)
            generator.fit(durations)
            transition_attributes["duration_generator"] = generator

        if self.debug: logging.info("Fitting models for other attributes")

        # Numerical attributes
        self.numerical_attributes = [attribute
                                for attribute, attr_type in log.event_attribute_type_map.items()
                                if attr_type in ["date", "int", "float"] and
                                attribute not in XES_LOG_ATTRIBUTES_EXCLUDED_FROM_RANDOM]
        self.numerical_event_attribute_ranges_: dict[str, (int, int)] = {}
        for attribute in self.numerical_attributes:
            min_value = log_df.loc[:, attribute].min()
            max_value = log_df.loc[:, attribute].max()
            self.numerical_event_attribute_ranges_[attribute] = (min_value, max_value)

        # Categorical attributes
        self.categorical_attributes = [attribute
                                  for attribute, attr_type in log.event_attribute_type_map.items()
                                  if attr_type in ["string", "id", "bool"] and
                                  attribute not in XES_LOG_ATTRIBUTES_EXCLUDED_FROM_RANDOM]
        self.categorical_event_attribute_frequencies_: dict[str, dict[str, int]] = {}
        for attribute in self.categorical_attributes:
            counts = log_df.loc[:, attribute].value_counts().to_dict()
            self.categorical_event_attribute_frequencies_[attribute] = counts

        # Other
        self.log_attribute_type_map = log.log_attribute_type_map
        self.trace_attribute_type_map = log.trace_attribute_type_map
        self.event_attribute_type_map = log.event_attribute_type_map

        # self.create_primary_model_data_frame(log)
        # self.create_initial_attribute_generation_dependency_graph(log)

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

        for i in range(self.traces_count_):
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
                    XesGenerator2._get_sequence_graph_node_key(current_event),
                    XesGenerator2._get_sequence_graph_node_key(next_event),
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

    def _generate_data(self, trace):
        pass

    def _analyze_sequence(self, trace: XesTrace) -> nx.DiGraph:
        graph = nx.DiGraph()

        if len(trace.events) == 0:
            return graph

        if len(trace.events) == 1:
            key = self._get_sequence_graph_node_key(trace.events[0])
            graph.add_node(key)
            return graph

        for i in range(len(trace.events) - 1):
            current_event = trace.events[i]
            current_event_key = self._get_sequence_graph_node_key(current_event)
            next_event = trace.events[i + 1]
            next_event_key = self._get_sequence_graph_node_key(next_event)

            edge = (current_event_key, next_event_key)
            transition_duration = abs(next_event["time:timestamp"] - current_event["time:timestamp"])

            if edge not in graph.edges:
                graph.add_edge(*edge, frequency=0, transition_durations=[])

            graph.edges[edge]["frequency"] += 1
            graph.edges[edge]["transition_durations"].append(transition_duration)

        first_event_key = self._get_sequence_graph_node_key(trace.events[0])
        graph.nodes[first_event_key]["first"] = 1

        last_event_key = self._get_sequence_graph_node_key(trace.events[-1])
        graph.nodes[last_event_key]["last"] = 1

        return graph

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

    def is_categorical(self, attribute: str):
        return attribute in self.categorical_attributes

    def is_numerical(self, attribute: str):
        return attribute in self.numerical_attributes

    def get_statistical_type(self, attribute: str):
        return "numerical" if self.is_numerical(attribute) else "categorical"

    # region attribute dependency graph

    def create_primary_model_data_frame(self, log: XesLog):
        self._create_primary_model_attributes_data_frame(log)
        self._add_one_hot_encoded_attributes_to_data_frame(log)
        self._add_event_transition_duration_to_data_frame(log)

    def _create_primary_model_attributes_data_frame(self, log: XesLog):
        self.trace_dfs = []

        for trace in log.traces:
            columns_rename_map = {column: f"attribute__{column}" for column in trace.df.columns}
            new_df = trace.df.rename(columns=columns_rename_map, inplace=False)
            self.trace_dfs.append(new_df)

        self.df = pd.concat(self.trace_dfs)

    # def _add_one_hot_encoded_attributes_to_data_frame(self, log: XesLog):

    def _add_event_transition_duration_to_data_frame(self, log: XesLog):
        self._add_new_df_column(
            name = "meta__event_transition_duration",
            calculation = lambda df: df["attribute__time:timestamp"] - df.shift(1)["attribute__time:timestamp"]
        )

    def _add_new_df_column(
            self,
            name: str,
            calculation: typing.Callable[[pd.DataFrame], typing.Any],
            overwrite=False
        ):
        if not overwrite and name in self.df:
            return

        for trace_df in self.trace_dfs:
            trace_df[name] = calculation(trace_df)

        self.df[name] = pd.concat([trace_df[name] for trace_df in self.trace_dfs])

    def create_initial_attribute_generation_dependency_graph(self, log: XesLog):
        graph = nx.DiGraph()

        features = []
        attribute_features = []
        for attribute, attr_type in log.event_attribute_type_map.items():
            if attr_type == 'int':
                feature = EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute],
                    compute_action_single=lambda f, values: values[attribute]
                )
                attribute_features.append(EventFeature2())
            elif attr_type == 'date':
                features.append(EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute].year,
                    compute_action_single=lambda f, values: values[attribute].year
                ))
                features.append(EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute].month,
                    compute_action_single=lambda f, values: values[attribute].month
                ))
                features.append(EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute].day,
                    compute_action_single=lambda f, values: values[attribute].day
                ))
                features.append(EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute].hour,
                    compute_action_single=lambda f, values: values[attribute].hour
                ))
                features.append(EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute].minute,
                    compute_action_single=lambda f, values: values[attribute].minute
                ))
                features.append(EventFeature2(
                    attributes=[attribute],
                    compute_action_df=lambda f, df: df[attribute].second,
                    compute_action_single=lambda f, values: values[attribute].second
                ))
            statistical_type = "numerical" if attribute in self.numerical_attributes else "categorical"
            feature = EventFeature("attribute", attribute, statistical_type)
            attribute_features.append(feature)

        features = [
            # time:timestamp difference from last event
            EventFeature("meta", "event_transition_duration", "numerical"),

            # Other event attributes
            *attribute_features

            # Previous event attributes
            # TODO: Naming convention:
            # "meta__event_i-1_attribute__attribute_name"
            # "meta__event_i-2_attribute__lifecycle_transition"
            # "meta__event_i-1_meta__event_transition_duration"

            # Other

            # "delta__time_timestamp"
            # "le__time_timestamp" # Label Encoding
        ]

        # TODO: Instead of what is happening below, evaluate feature dependency between each element

        self.rng.shuffle(features)

        # randomly split list to 2 lists by following rules:
        # 1 list size: [1, n] (must have at least one element)
        # 2 list size: [0, n - 1]

        split_point = self.rng.integers(1, len(features))
        independent, dependent = features[:split_point], features[split_point:]

        for feature in independent:
            if self.debug:
                logging.info(f"Fitting independent feature: {feature.id}")

            model = self._pick_model_for_independent_feature(feature)

            if self.debug:
                logging.info(f"Model: {model}")

            model.fit(self.df[[feature.id]].to_numpy())

            graph.add_node(feature.id, feature=feature, model=model)

        assert(len(graph.nodes) >= 1)

        for feature in dependent:
            if self.debug:
                logging.info(f"Fitting dependent feature: {feature.id}")

            existing_features = [feature for node, feature in graph.nodes.data("feature")]

            depending_on_features = None
            if len(existing_features) == 1:
                depending_on_features = [next(iter(existing_features))]
            else:
                depending_on_features_count = self.rng.integers(1, len(existing_features))
                depending_on_features = self.rng.choice(existing_features, size=depending_on_features_count, replace=False)

            # TODO: label encode depending categorical attributes

            if self.debug:
                depending_on_features_text = ", ".join([feature.id for feature in depending_on_features])
                logging.info(f"Depending on {len(depending_on_features)} feature(s): {depending_on_features_text}")

            for depending_on_feature in depending_on_features:
                # graph.add_edge(depending_on_feature, feature)
                graph.add_edge(feature.id, depending_on_feature.id)

            # TODO: Pick previous (and before-previous, up-to configurable N) iteration features (any)

            model = self._pick_model_for_dependent_feature(feature)

            if self.debug:
                logging.info(f"Model: {model}")

            fit_data = self.df[[feature.id for feature in depending_on_features]].to_numpy()
            fit_target = self.df[feature.id].to_numpy()
            model.fit(fit_data, fit_target)

            graph.add_node(feature.id, feature=feature, model=model)

        self._event_feature_dependency_graph = graph

    def _pick_model_for_independent_feature(self, feature: EventFeature):
        return self.rng.choice(INDEPENDENT_FEATURE_GENERATION_MODEL[feature.statistical_type])

    def _pick_model_for_dependent_feature(self, feature: EventFeature):
        return self.rng.choice(DEPENDENT_FEATURE_GENERATION_MODEL[feature.statistical_type])

    # region Attribute generation

    def _prepare_traverse_sequence(self):
        # create post-order traverse sequence for given graph
        # graph can be splitted into non-connected components

        # for each component:
        #   find its root
        #   traverse post-order

        # https://en.wikipedia.org/wiki/Tree_traversal#Post-order

        # visit_sequence = []
        # visited = set()
        # queue = []

        # graph = self._event_feature_dependency_graph

        # independent_features = [node for node in graph.out_degree(0)]
        # queue = independent_features

        # while len(queue) > 0:
        #     node = queue.pop()

        # # For each "root" in each disconnected component of the graph:
        # for node in graph.in_degree(0):
        #     if node in visited:
        #         continue

        # 🤦 apparently, it is called topological sort: https://en.wikipedia.org/wiki/Topological_sorting
        # and apparently it is already implemented in NetworkX

        self._event_feature_dependency_graph_traverse_sequence = \
            nx.topological_sort(self._event_feature_dependency_graph)

    def generate_attributes_for_event(self, event):
        graph = self._event_feature_dependency_graph

        for feature_id in self._event_feature_dependency_graph_traverse_sequence:
            dependent_on_features_ids = graph[feature_id]

            model = graph.nodes[feature_id]["model"]

            result = None
            if len(dependent_on_features_ids) == 0:
                result = model.sample()
            else:
                dependent_on_features_values = [event[feature] for feature in dependent_on_features_ids]
                result = model.predict(dependent_on_features_values)

            event[feature_id] = result
