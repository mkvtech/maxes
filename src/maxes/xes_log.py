from functools import cached_property

import pandas as pd

from maxes.types import XesTypeEnum
from maxes.utils import reorder_xes_columns
from maxes.constants import CONCEPT_NAME, LIFECYCLE_TRANSITION, TIME_TIMESTAMP


class AttributeInfo:
    name: str
    xes_type: XesTypeEnum

    @staticmethod
    def concept_name():
        attribute_info = AttributeInfo()
        attribute_info.name = CONCEPT_NAME
        attribute_info.xes_type = XesTypeEnum.STRING
        return attribute_info

    @staticmethod
    def lifecycle_transition():
        attribute_info = AttributeInfo()
        attribute_info.name = LIFECYCLE_TRANSITION
        attribute_info.xes_type = XesTypeEnum.STRING
        return attribute_info

    @staticmethod
    def time_timestamp():
        attribute_info = AttributeInfo()
        attribute_info.name = TIME_TIMESTAMP
        attribute_info.xes_type = XesTypeEnum.DATE
        return attribute_info


class XesAttribute:
    @staticmethod
    def concept_name(value: str):
        return XesAttribute(
            xes_type=XesTypeEnum.STRING,
            key=CONCEPT_NAME,
            raw_value=value,
            parsed_value=value,
        )

    @staticmethod
    def lifecycle_transition(value: str):
        return XesAttribute(
            xes_type=XesTypeEnum.STRING,
            key=LIFECYCLE_TRANSITION,
            raw_value=value,
            parsed_value=value,
        )

    @staticmethod
    def time_timestamp(value: str):
        return XesAttribute(
            xes_type=XesTypeEnum.DATE,
            key=TIME_TIMESTAMP,
            raw_value=value,
            parsed_value=value,
        )

    def __init__(
        self, xes_type: XesTypeEnum, key: str, raw_value: str, parsed_value: str
    ):
        self.xes_type = xes_type
        self.key = key
        self.raw_value = raw_value
        self.parsed_value = parsed_value


class XesAttributesCollectionBase:
    def __init__(self, attributes: dict[str, any] | None = None):
        self.attributes = normalize_attributes(attributes)

    def clear_attributes(self):
        self.attributes = {}

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def _get_attribute(self, key):
        return self.attributes.get(key)

    def _get_attribute_parsed_value(self, key):
        attribute = self.attributes.get(key)
        return attribute.parsed_value if attribute is not None else None


class CommonXesAttributesMixin:
    @property
    def concept_name(self):
        return self._get_attribute_parsed_value(CONCEPT_NAME)

    @concept_name.setter
    def concept_name(self, value: str):
        self.attributes[CONCEPT_NAME] = XesAttribute.concept_name(value)

    @property
    def lifecycle_transition(self):
        return self._get_attribute_parsed_value(LIFECYCLE_TRANSITION)

    @lifecycle_transition.setter
    def lifecycle_transition(self, value: str):
        self.attributes[LIFECYCLE_TRANSITION] = XesAttribute.lifecycle_transition(value)

    @property
    def time_timestamp(self):
        return self._get_attribute_parsed_value(TIME_TIMESTAMP)

    @time_timestamp.setter
    def time_timestamp(self, value: str):
        self.attributes[TIME_TIMESTAMP] = XesAttribute.time_timestamp(value)


class XesEvent(XesAttributesCollectionBase, CommonXesAttributesMixin):
    def __init__(self, attributes: dict[str, any] | None = None):
        super().__init__(attributes)

    def __repr__(self):
        concept_name = self.concept_name
        concept_name_text = (
            f" concept:name={self.concept_name}" if concept_name is not None else ""
        )

        lifecycle_transition = self.lifecycle_transition
        lifecycle_transition_text = (
            f" concept:name={self.lifecycle_transition}"
            if lifecycle_transition is not None
            else ""
        )

        time_timestamp = self.time_timestamp
        time_timestamp_text = (
            f" concept:name={self.time_timestamp}" if time_timestamp is not None else ""
        )

        return f"<maxes.xes_log.XesEvent{concept_name_text}{lifecycle_transition_text}{time_timestamp_text}>"

    def to_series(self):
        return pd.Series(
            {key: attribute.parsed_value for key, attribute in self.attributes.items()}
        )


def normalize_attributes(
    attributes: list[XesAttribute] | dict[str, XesAttribute] | None,
) -> dict[str, XesAttribute]:
    if attributes is None:
        return {}
    if isinstance(attributes, list):
        return {attribute.key: attribute for attribute in attributes}

    return attributes


class XesTrace(XesAttributesCollectionBase, CommonXesAttributesMixin):
    def __init__(
        self,
        events: list[XesEvent] | None = None,
        attributes: list[XesAttribute] | None = None,
    ):
        super().__init__(attributes)
        self.events = events or []

    @cached_property
    def df(self):
        return pd.DataFrame([event.attributes for event in self.events])

    def update_df(self, with_trace_attributes=True) -> pd.DataFrame:
        self.df = pd.DataFrame([event.to_series() for event in self.events])

        if with_trace_attributes:
            for name, attribute in self.attributes.items():
                self.df[f"case:{name}"] = attribute.parsed_value

        return self.df

    def clear_cache(self):
        del self.df

    def update_events_from_df(self, attributes_info: list[AttributeInfo]):
        self.events = []

        for row_index, row in self.df.iterrows():
            event = XesEvent()
            self.events.append(event)

            for attribute_info in attributes_info:
                key = attribute_info.name

                event[key] = XesAttribute(
                    xes_type=attribute_info.xes_type,
                    key=key,
                    raw_value=row[key],
                    parsed_value=row[key],
                )


class XesLog:
    log_attributes_info: dict[str, AttributeInfo]
    trace_attributes_info: dict[str, AttributeInfo]
    event_attributes_info: dict[str, AttributeInfo]

    def __init__(
        self,
        traces: list[XesTrace] = None,
        attributes: list[XesAttribute] = None,
        # extensions: list[XesExtension]= None,
        # global
        # classifier
        # version
    ):
        self.traces = traces or []
        self.attributes = normalize_attributes(attributes)

        self.log_attributes_info = {}
        self.trace_attributes_info = {}
        self.event_attributes_info = {}

        self.loader = None

    @property
    def event_attributes(self) -> list[str]:
        return self.event_attributes_info.keys()

    def update_df(self, with_trace_attributes=True):
        for trace in self.traces:
            trace.update_df(with_trace_attributes=with_trace_attributes)

        self.df = pd.concat([trace.df for trace in self.traces])

        self.df = reorder_xes_columns(self.df)

        return self.df

    def _update_events_from_df(self):
        attributes_info = self.event_attributes_info.values()
        for trace in self.traces:
            trace.update_events_from_df(attributes_info=attributes_info)

    def update_traces_from_df(self):
        self.traces = []

        for name, group in self.df.groupby("case:concept:name"):
            trace = XesTrace()

            trace.df = group
            trace.attributes[CONCEPT_NAME] = XesAttribute.concept_name(name)

            self.traces.append(trace)

        self._update_events_from_df()
