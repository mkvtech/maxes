import typing
import pandas as pd
import xml.dom.minidom
import xml.dom.pulldom
import dateutil.parser
import numpy as np
import functools
import maxes.utils
from datetime import timezone
from maxes.types import XesEventRaw, XesTraceRaw, XesFileRaw

XES_ATTRIBUTE_NAMES = ["string", "date", "int", "float", "boolean", "id", "list"]


class XesAttribute:
    def __init__(self, data_type: str, key: str, raw_value: str, parsed_value: str):
        self.data_type = data_type
        self.key = key
        self.raw_value = raw_value
        self.parsed_value = parsed_value


class XesEvent:
    def __init__(self, attributes: list[XesAttribute]):
        self.attributes = normalize_attributes(attributes)


def xes_attributes_dict(attributes: list[XesAttribute]) -> dict[str, XesAttribute]:
    return {attribute.key: attribute for attribute in attributes}


def xes_attribute_df(attributes: list[XesAttribute]) -> pd.DataFrame:
    return pd.DataFrame({attribute.key: attribute.value for attribute in attributes})


def normalize_attributes(
        attributes: list[XesAttribute] | dict[str, XesAttribute] | None
) -> dict[str, XesAttribute]:
    if attributes is None:
        return {}
    if isinstance(attributes, list):
        # TODO: Check duplicate keys
        return {attribute.key: attribute for attribute in attributes}

    return attributes


class XesTrace:
    def __init__(
            self,
            events: list[XesEvent] = None,
            attributes: list[XesAttribute] = None,
    ):
        self.events = events or []
        self.attributes = normalize_attributes(attributes)

    def update_df(self):
        self.df = xes_attribute_df(self.attributes)


class XesLog:
    def __init__(
            self,
            traces: list[XesTrace] = None,
            attributes: list[XesAttribute] = None,
            # extensions: list[XesExtension]= None,
            # global
            # classifier
            # version
    ):
        self.traces = traces
        self.attributes = normalize_attributes(attributes)


class XesLoader:
    def __init__(self, options: dict[str, any] = {}):
        self.options = options

    def load(self, file_path: str) -> XesLog:
        current_log = XesLog()

        with open(file_path) as xml_file:
            event_stream = xml.dom.pulldom.parse(xml_file)

            # trace_index = -1
            current_trace = None

            for event_stream__event, node in event_stream:
                if event_stream__event == xml.dom.pulldom.START_ELEMENT:

                    if node.tagName == "trace":
                        # trace_index += 1
                        # if not self.is_load_trace(trace_index):
                        #     continue

                        current_trace = XesTrace()

                    elif node.tagName == "event":
                        assert current_trace is not None

                        # if not self.is_load_trace(trace_index):
                        #     continue

                        event_stream.expandNode(node)
                        event = self.parse_event(node)
                        current_trace.events.append(event)

                    elif node.tagName in XES_ATTRIBUTE_NAMES:
                        assert current_log is not None or current_trace is not None

                        event_stream.expandNode(node)
                        attribute = self.parse_attribute(node)

                        if current_trace is not None:
                            current_trace.attributes.append(attribute)
                        elif current_log is not None:
                            current_log.attributes.append(attribute)

                    # TODO: "extension", "global", "classifier"

                elif event_stream__event == xml.dom.pulldom.END_ELEMENT:
                    if node.tagName == "trace":
                        current_log.traces.append(current_trace)
                        current_trace = None
        return current_log

    def is_load_trace(self, trace_index: int) -> bool:
        if "load_traces" not in self.options:
            return True

        load_traces = self.options["load_traces"]

        return \
            isinstance(load_traces, list) and trace_index in load_traces or \
            isinstance(load_traces, int) and trace_index < load_traces

    def parse_event(self, event_node: xml.dom.minidom.Element) -> XesEvent:
        attributes = {}

        for node in event_node.childNodes:
            if node.nodeType != xml.dom.minidom.Node.ELEMENT_NODE:
                continue

            key = node.attributes["key"].value
            if not self.allow_event_attribute(key):
                continue

            attributes[key] = self.parse_attribute(node)

        return XesEvent(attributes)

    def parse_attribute(self, attribute_node: xml.dom.minidom.Element) -> XesAttribute:
        data_type = attribute_node.nodeName
        key = attribute_node.attributes["key"].value
        raw_value = attribute_node.attributes["value"].value
        parsed_value = self.parse_attribute_value(raw_value, data_type)

        return XesAttribute(data_type=data_type, key=key, raw_value=raw_value, parsed_value=parsed_value)

    def parse_attribute_value(self, value: str, value_type: str):
        if value_type == "string" or value_type == "id":
            return str(value)
        if value_type == "int":
            return int(value)
        if value_type == "float":
            return float(value)
        if value_type == "boolean":
            return value.lower() == "true"
        if value_type == "date":
            value = dateutil.parser.isoparse(value)
            if self.options.get("drop_timezones"):
                value = value.astimezone(timezone.utc)
            return value
        if value_type == "list":
            raise NotImplementedError()

        raise AttributeError("Unknown attribute type", value_type)

    def allow_event_attribute(self, event_attribute_key: str) -> bool:
        if "event_attribute_key_allowlist" in self.options and \
                event_attribute_key in self.options["event_attribute_key_allowlist"]:
            return True

        if "event_attribute_key_denylist" in self.options and \
                event_attribute_key in self.options["event_attribute_key_denylist"]:
            return False

        return True

    def _register_event_attribute_type(self, key: str, data_type: str):
        if key not in self.event_attribute_type_mapping:
            self.event_attribute_type_mapping[key] = {}
        self.event_attribute_type_mapping[key].setdefault(data_type, 0)
        self.event_attribute_type_mapping[key][data_type] += 1


def parse_xes_event(
    event_node,
    keys: None | str | list[str] = None,
    unify_timestamps=True
) -> XesEventRaw:
    data = {}

    for node in event_node.childNodes:
        if node.nodeType == xml.dom.minidom.Node.TEXT_NODE:
            continue

        key = node.getAttribute("key")

        if keys != None and key not in keys:
            continue

        raw_value = node.getAttribute("value")
        value = None

        data_type = node.tagName

        if data_type == "date":
            value = dateutil.parser.isoparse(raw_value)
            if unify_timestamps:
                value = value.astimezone(timezone.utc)
        else:
            value = raw_value

        data[key] = value

    return data


def parse_xes(
    filepath,
    on_trace: typing.Callable[[], None] = maxes.utils.noop,
    on_trace_end: typing.Callable[[dict[str, any]], None] = maxes.utils.noop,
    on_event: typing.Callable[[XesEventRaw], None] = maxes.utils.noop,
    keys: None | str | list[str] = None,
    load_traces: typing.Literal["all"] | int | list[int] = "all"
):
    with open(filepath) as xml_file:
        event_stream = xml.dom.pulldom.parse(xml_file)

        trace_index = -1
        trace_data = {}

        def is_load_trace():
            return load_traces == "all" or \
                isinstance(load_traces, list) and trace_index in load_traces or \
                isinstance(load_traces, int) and trace_index < load_traces

        for event, node in event_stream:
            if event == xml.dom.pulldom.START_ELEMENT:
                if node.tagName == "trace":
                    trace_index += 1
                    if not is_load_trace():
                        continue

                    trace_data = {}
                    on_trace()
                if node.tagName == "event":
                    if not is_load_trace():
                        continue

                    event_stream.expandNode(node)
                    on_event(parse_xes_event(node, keys=keys))

                if node.tagName == "string":
                    event_stream.expandNode(node)
                    key = node.getAttribute("key")
                    value = node.getAttribute("value")
                    trace_data[key] = value

            if event == xml.dom.pulldom.END_ELEMENT:
                if node.tagName == "trace":
                    if not is_load_trace():
                        continue
                    on_trace_end(trace_data)


def load_raw_xes(
    filepath: str,
    keys: None | str | list[str] = None,
    load_traces: typing.Literal["all"] | int | list[int] = "all"
) -> XesFileRaw:
    traces = []
    current_trace = {}
    current_trace_events = []

    def on_trace():
        nonlocal current_trace, current_trace_events
        current_trace_events = []
        current_trace = {"events": current_trace_events}
        traces.append(current_trace)

    def on_trace_end(trace_attributes: dict[str, any]):
        current_trace["attributes"] = trace_attributes

    def on_event(event):
        current_trace_events.append(event)

    parse_xes(filepath, on_trace=on_trace, on_trace_end=on_trace_end,
              on_event=on_event, keys=keys, load_traces=load_traces)

    # TODO: Add related data, extensions, etc
    return {
        "filepath": filepath,
        "traces": traces
    }
