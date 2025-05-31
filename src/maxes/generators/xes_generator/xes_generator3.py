from __future__ import annotations
import datetime
import itertools
import logging
import numpy as np
import pandas as pd
import sklearn.neighbors
from enum import Enum

from sklearn.base import BaseEstimator
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import CategoricalNB

import maxes.analyze_sequence
from maxes.graphs import RandomWeightedTraverser
import maxes.utils
from maxes.utils import dig
from maxes.logging import NestedLogger
from maxes.xes_log import (
    XesLog,
    XesTrace,
    XesEvent,
    XesTypeEnum,
    AttributeInfo as XesLog__AttributeInfo,
)
from maxes.models.fake_predictor import FakePredictor
from maxes.models.models import WeightedSampler
from maxes.generators.xes_generator.share import AttributeLevelEnum, NumeralicityEnum
from maxes.generators.xes_generator.algorithms import (
    expand_integer_range,
)
from maxes.generators.xes_generator.attribute_generators import (
    AttributeGenerator,
    AttributePredictor_MLPClassifier,
    AttributePredictor_ClassifierWrapper,
    AttributePredictorBase,
)

from maxes.constants import (
    SPECIAL_XES_ATTRIBUTES,
    CASE_CONCEPT_NAME,
    CONCEPT_NAME,
    TIME_TIMESTAMP,
    LIFECYCLE_TRANSITION,
)


from sklearn.naive_bayes import CategoricalNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

model_name_to_model_class = {
    "CategoricalNB": CategoricalNB,
    "KNeighborsClassifier": KNeighborsClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "RandomForestClassifier": RandomForestClassifier,
}


class KdeForTimeDeltas:
    def __init__(self, kde_kwargs={}):
        self.kde_kwargs = kde_kwargs

    def fit(self, data):
        # TODO: Use appropriate conversion from timedelta to float based on delta = max(data) - min(data)
        data = [[time_delta.seconds] for time_delta in data]
        self.kde_ = sklearn.neighbors.KernelDensity(**self.kde_kwargs)
        self.kde_.fit(data)
        return self

    def sample(self, n_samples=1):
        return [
            datetime.timedelta(seconds=item[0]) for item in self.kde_.sample(n_samples)
        ]


class KdeForTimeStamps1:
    def __init__(self):
        pass

    def fit(self, data):
        data = [[date.timestamp()] for date in data]
        self.kde_ = sklearn.neighbors.KernelDensity().fit(data)
        return self

    def sample(self, n_samples=1):
        return [
            datetime.datetime.fromtimestamp(item[0], tz=datetime.timezone.utc)
            for item in self.kde_.sample(n_samples)
        ]


class XesAttributeModelBase:
    def __init__(self, attribute: str, dependent_attributes: list[str] = []):
        self.attribute = attribute
        self.dependent_attributes = dependent_attributes

    def fit(self, df: pd.DataFrame):
        raise NotImplementedError()

    def predict(self, df: pd.DataFrame):
        raise NotImplementedError()


class XesAttributeModelPredictor(XesAttributeModelBase):
    def __init__(
        self,
        model,
        attribute: str,
        dependent_attributes: list[str],
        output_transformer: Pipeline = OneHotEncoder(),
    ):
        super().__init__(attribute, dependent_attributes)
        self.model = model
        self.output_transformer = output_transformer

    def fit(self, df: pd.DataFrame):
        y_train = self.output_transformer.fit_transform(df[[self.attribute]])
        self.model.fit(df, y_train)

    def predict(self, df: pd.DataFrame):
        y_predicted = self.model.predict(df)
        y_untransformed = self.output_transformer.inverse_transform(y_predicted)
        return y_untransformed


class XesAttributeModelRandom(XesAttributeModelBase):
    def __init__(self, attribute):
        self.attribute = attribute

    def fit(self, df: pd.DataFrame):
        pass

    def predict(self, df: pd.DataFrame):
        pass


class AttributeInfo:
    name: str = None
    level: AttributeLevelEnum = None
    xes_type: XesTypeEnum = None
    presence: float = None
    numeralicity: NumeralicityEnum = None
    is_trace_identifier: bool = None

    presence_model: BaseEstimator = None
    sampler = None
    predictor: BaseEstimator = None
    encoder: OneHotEncoder = None

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "xes_type": self.xes_type,
            "presence": self.presence,
            "numeralicity": self.numeralicity,
            "is_trace_identifier": self.is_trace_identifier,
        }


class Stats:
    nunique_per_log: pd.Series
    notnull: pd.DataFrame
    nunique_per_trace: pd.DataFrame
    is_trace_level: pd.Series[bool]
    presence: pd.DataFrame


# region Generator


class XesGenerator3:
    trace_attributes_info: dict[str, AttributeInfo] = {}
    event_attributes_info: dict[str, AttributeInfo] = {}

    _traces_count: int
    _stats: Stats = Stats()

    def __init__(
        self,
        attributes_models: dict[str, dict[str, any]] = {},
        generate_traces_count: int | None = None,
        generate_attributes=True,
        rng: np.random.Generator = np.random,
        nlogger: NestedLogger = NestedLogger.default(),
        transition_models_kwargs: dict[tuple, any] = {},
    ) -> None:
        self.attributes_models = attributes_models
        self.generate_traces_count = generate_traces_count
        self.generate_attributes = generate_attributes
        self.rng = rng
        self.nlogger = nlogger
        self.transition_models_kwargs = transition_models_kwargs

    # region Fitting

    def fit(self, log: XesLog) -> XesGenerator3:

        self._log = log

        # TODO: Fill case:concept:name if not present

        with self.nlogger.action_logging("Validating"):
            self._validate_required_attributes()
            self._validate_multiple_level_attributes()

        with self.nlogger.action_logging("Gathering meta data"):
            self._has_attribute_lifecycle_transition = (
                LIFECYCLE_TRANSITION in log.df.columns
            )

            if self.generate_traces_count is None:
                self.generate_traces_count = len(log.traces)

            self._traces_count = len(log.traces)

            traces_lengths = [len(trace.events) for trace in log.traces]
            self.trace_length_range_ = (min(traces_lengths), max(traces_lengths))

            self.log_df_ = pd.concat(trace.df for trace in log.traces)

        with self.nlogger.action_logging(
            "Fitting models for traces beginning timestamps"
        ):
            trace_beginning_timestamps_ = [
                trace.events[0].time_timestamp for trace in log.traces
            ]
            self.trace_beginning_timestamp_generator_ = KdeForTimeStamps1().fit(
                trace_beginning_timestamps_
            )

        with self.nlogger.action_logging("Analysing sequence graph"):
            self.sequence_graph_ = maxes.analyze_sequence.analyze_xes_log_sequence(log)

        with self.nlogger.action_logging("Fitting graph traverser"):
            self.graph_traverser_ = RandomWeightedTraverser(
                rng=self.rng,
                min_steps=self.trace_length_range_[0],
                max_steps=self.trace_length_range_[1],
                weight_feature_name="frequency",
            )
            self.graph_traverser_.fit(self.sequence_graph_)

        with self.nlogger.action_logging("Fittig models for time:timestamp attribute"):
            for transition in self.sequence_graph_.edges.keys():
                self.fit_transition_model(transition)

        if self.generate_attributes:
            with self.nlogger.action_logging("Collecting stats"):
                self._collect_stats()

            with self.nlogger.action_logging("Collecting attributes info"):
                self._construct_event_attributes_info()

            with self.nlogger.action_logging("Fitting presence models"):
                self._fit_presence_models()

            with self.nlogger.action_logging("Fitting trace-level attributes models"):
                self._fit_trace_level_attributes_models()

            with self.nlogger.action_logging("Fitting event-level attributes models"):
                self._fit_event_level_attributes_models()

        del self._log

        return self

    # region Fitting / Separate

    def fit_transition_model(self, edge: tuple[tuple, tuple]):
        edge_data = self.sequence_graph_.edges[edge]

        durations = edge_data["transition_durations"]
        kwargs = self.transition_models_kwargs.get(edge, {})

        generator = KdeForTimeDeltas(kde_kwargs=kwargs).fit(durations)
        generator.fit(durations)
        edge_data["duration_generator"] = generator

    # region Fitting / private

    def _collect_stats(self):
        df = self.log_df_

        stats = Stats()

        stats.nunique_per_log = df.nunique()
        stats.notnull = df.notnull()
        stats.nunique_per_trace = df.groupby(CASE_CONCEPT_NAME).nunique()
        stats.is_trace_level = (stats.nunique_per_trace == 1).all()
        stats.presence = stats.notnull.sum() / len(df)

        self._stats = stats

    def _construct_event_attributes_info(self):
        df = self.log_df_
        stats = self._stats

        self.event_attributes_info = {}
        for log_attribute_info in self._log.event_attributes_info.values():
            attribute_info = AttributeInfo()
            attribute_info.name = log_attribute_info.name
            attribute_info.xes_type = log_attribute_info.xes_type

            self.event_attributes_info[attribute_info.name] = attribute_info

        custom_attributes = [
            attribute
            for attribute in self.event_attributes_info.keys()
            if attribute not in SPECIAL_XES_ATTRIBUTES
        ]

        for attribute in custom_attributes:
            attribute_info = self.event_attributes_info[attribute]

            # level
            level = (
                AttributeLevelEnum.TRACE
                if stats.is_trace_level[attribute]
                else AttributeLevelEnum.EVENT
            )
            attribute_info.level = level

            # is_trace_identifier
            is_unique_per_trace = stats.nunique_per_log[attribute] == self._traces_count
            attribute_info.is_trace_identifier = (
                is_unique_per_trace and stats.is_trace_level[attribute]
            )

            # presence
            attribute_info.presence = stats.presence[attribute]

            # presence_model
            presence_model = None
            if attribute_info.presence == 1.0:
                presence_model = FakePredictor(value=True)
            elif attribute_info.presence == 0.0:
                presence_model = FakePredictor(value=False)
            else:
                presence_model = CategoricalNB()
            attribute_info.presence_model = presence_model

        # DONE: Compute level
        # DONE: Fit presence model
        # TODO: Fill categorical / numerical
        # DONE: Guess if is unique per trace
        # TODO: Find attributes that are of float type, but never have float part

    def _fit_presence_models(self):
        X = self.log_df_[["concept:name"]]
        self._concept_name_encoder = OneHotEncoder()
        X = self._concept_name_encoder.fit_transform(X)
        X = np.asarray(X.todense())

        for attribute_info in self.event_attributes_info.values():
            attribute = attribute_info.name

            y = self._stats.notnull[attribute]

            model = attribute_info.presence_model

            if model is None:
                continue

            model.fit(X, y)

    def _fit_trace_level_attributes_models(self):
        for attribute_info in self.event_attributes_info.values():
            if attribute_info.level != AttributeLevelEnum.TRACE:
                continue
            if attribute_info.is_trace_identifier:
                continue

            attribute = attribute_info.name

            X = self.log_df_[attribute]

            sampler = WeightedSampler(rng=self.rng)
            sampler.fit(X)

            attribute_info.sampler = sampler

    def _fit_event_level_attributes_models(self):
        X = self.log_df_[[CONCEPT_NAME]]

        for attribute_info in self.event_attributes_info.values():
            if attribute_info.level != AttributeLevelEnum.EVENT:
                continue

            attribute = attribute_info.name

            with self.nlogger.action_logging(f"  Fitting model for {attribute}"):
                self.fit_event_level_attribute_model(attribute)

    def fit_event_level_attribute_model(self, attribute: str):
        attribute_info = self.event_attributes_info[attribute]

        inner_model_name = (
            dig(self.attributes_models, attribute, "model_name") or "CategoricalNB"
        )
        inner_model_class = model_name_to_model_class[inner_model_name]
        inner_model_kwargs = (
            dig(self.attributes_models, attribute, "model_kwargs") or {}
        )

        predictor = AttributePredictor_ClassifierWrapper(
            inner_model_class=inner_model_class, inner_model_kwargs=inner_model_kwargs
        )

        generator = AttributeGenerator(
            input_columns=[CONCEPT_NAME],
            output_column=attribute,
            model=predictor,
        )

        with self.nlogger.action_logging(f"  Fitting transformers for {attribute}"):
            generator.fit_transformers(self.log_df_)

        with self.nlogger.action_logging(f"  Fitting prediction model for {attribute}"):
            generator.fit(self.log_df_)

        attribute_info.predictor = generator

    # region Generation

    def sample(self, n_samples=1) -> list[XesLog]:
        return [self.generate() for i in range(n_samples)]

    def generate(self) -> XesLog:
        log = XesLog()
        self._log = log

        # Default attributes_info
        log.event_attributes_info[CONCEPT_NAME] = XesLog__AttributeInfo.concept_name()
        log.event_attributes_info[TIME_TIMESTAMP] = (
            XesLog__AttributeInfo.time_timestamp()
        )

        if self._has_attribute_lifecycle_transition:
            log.event_attributes_info[LIFECYCLE_TRANSITION] = (
                XesLog__AttributeInfo.lifecycle_transition()
            )

        log.trace_attributes_info[CONCEPT_NAME] = XesLog__AttributeInfo.concept_name()

        for attribute_info in self.event_attributes_info.values():
            log_attrubte_info = XesLog__AttributeInfo()
            log_attrubte_info.name = attribute_info.name
            log_attrubte_info.xes_type = attribute_info.xes_type
            log.event_attributes_info[attribute_info.name] = log_attrubte_info

        trace_length_range = self.trace_length_range_

        for i in range(self.generate_traces_count):
            trace = XesTrace()
            trace.concept_name = i
            log.traces.append(trace)

            for j in range(10):
                try:
                    self.graph_traverser_.min_steps = trace_length_range[0]
                    self.graph_traverser_.max_steps = trace_length_range[1]

                    generated_events_sequence = self.graph_traverser_.sample()[0]

                    if len(generated_events_sequence) == 0:
                        # sequence generator picked unsuccessful first and last nodes
                        continue

                    break
                except maxes.utils.CustomStackOverflowException as e:
                    new_trace_length_range = expand_integer_range(
                        trace_length_range, 0.1
                    )
                    logging.info(
                        f"Failed to generate events sequence with trace length in {
                                 trace_length_range}, will extend range to {new_trace_length_range} and try again."
                    )
                    trace_length_range = new_trace_length_range
            else:
                logging.info(trace_length_range)
                raise RuntimeError(
                    "Gave up after extending trace length range multiple times"
                )

            # Assign concept:name and lifecycle:transition
            for event_sequence_item in generated_events_sequence:
                event = XesEvent()
                trace.events.append(event)

                event.concept_name = event_sequence_item[0]

                if self._has_attribute_lifecycle_transition:
                    event.lifecycle_transition = event_sequence_item[1]

            # Assign time:timestamp
            trace_time_timestamp = self.trace_beginning_timestamp_generator_.sample()[0]
            trace.events[0].time_timestamp = trace_time_timestamp
            for current_event, next_event in itertools.pairwise(trace.events):
                edge = (
                    self._get_sequence_graph_node_key(current_event),
                    self._get_sequence_graph_node_key(next_event),
                )
                duration_generator = self.sequence_graph_.edges[edge][
                    "duration_generator"
                ]
                sample_duration = duration_generator.sample()[0]
                event_time_timestamp = current_event.time_timestamp + sample_duration
                next_event.time_timestamp = event_time_timestamp

        log.update_df()

        self._log_df = log.df

        if self.generate_attributes:
            self._predict_attributes_presence(log.df)

            self._sample_trace_level_attributes()

            self._sample_event_level_attributes()

            log.update_traces_from_df()

        return log

    # region Generation / private

    def _predict_attributes_presence(self, df: pd.DataFrame):
        result = pd.DataFrame()

        X = df[[CONCEPT_NAME]]
        X = self._concept_name_encoder.transform(X)
        X = np.asarray(X.todense())

        for attribute_info in self.event_attributes_info.values():
            model = attribute_info.presence_model

            if model is None:
                continue

            attribute = attribute_info.name
            result[attribute] = model.predict(X)

        self._presence_df = result

    def _sample_trace_level_attributes(self):
        values = pd.DataFrame()

        attributes_info = [
            attribute_info
            for attribute_info in self.event_attributes_info.values()
            if attribute_info.level == AttributeLevelEnum.TRACE
            and not attribute_info.is_trace_identifier
        ]

        # Generate
        for attribute_info in attributes_info:
            attribute = attribute_info.name
            sampler = attribute_info.sampler
            data = sampler.sample(n_samples=self.generate_traces_count)
            values[attribute] = data

        # Assign
        values[CASE_CONCEPT_NAME] = (
            self._log_df.groupby(CASE_CONCEPT_NAME)
            .first()
            .reset_index()[CASE_CONCEPT_NAME]
        )
        result = pd.merge(self._log_df, values, on=CASE_CONCEPT_NAME)
        for attribute_info in attributes_info:
            attribute = attribute_info.name
            result[attribute] = result[attribute][self._presence_df[attribute]]

        self._log.df = result

    def _sample_event_level_attributes(self):
        for attribute_info in self.event_attributes_info.values():
            if attribute_info.level != AttributeLevelEnum.EVENT:
                continue

            attribute = attribute_info.name

            model = attribute_info.predictor
            series = model.predict(self._log_df)

            self._log.df[attribute] = series

    # region Other

    def event_attributes_info_df(self):
        return pd.DataFrame(
            (ai.to_dict() for ai in self.event_attributes_info.values())
        )

    # region Validation

    def _validate_required_attributes(self):
        self._validate_required_attribute("concept:name")
        self._validate_required_attribute("time:timestamp")
        # self._validate_required_attribute("lifecycle:transition")

    def _validate_required_attribute(self, attribute: str):
        if self._log.event_attributes_info.get(attribute):
            return

        raise ValueError(f"Missing required event-level attribute: {attribute}")

    def _validate_multiple_level_attributes(self):
        event_attributes = self._log.event_attributes_info.keys() - {CONCEPT_NAME}
        trace_attributes = self._log.trace_attributes_info.keys() - {CONCEPT_NAME}
        multiple_level_attributes = event_attributes & trace_attributes

        if len(multiple_level_attributes) == 0:
            return

        raise ValueError(
            f"Multi-level attributes are not supported: {', '.join(multiple_level_attributes)}"
        )

    # region Private

    def _get_sequence_graph_node_key(self, event: XesEvent):
        if self._has_attribute_lifecycle_transition:
            return (event.concept_name, event.lifecycle_transition)
        else:
            return (event.concept_name,)
