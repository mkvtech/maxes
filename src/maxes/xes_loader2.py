from __future__ import annotations
import copy
import pandas as pd
import xml.dom.minidom
import xml.etree.ElementTree as ET
import dateutil.parser
import maxes.utils
from collections import defaultdict
from datetime import timezone
from maxes.utils import xml_tag_without_namespace
from enum import Enum

from maxes.logging import NestedLogger
from maxes.types import XesTypeEnum
from maxes.constants import CONCEPT_NAME

from maxes.xes_log import XesLog, XesTrace, XesEvent, XesAttribute, AttributeInfo

XES_STRING = "string"
XES_DATE = "date"
XES_INT = "int"
XES_FLOAT = "float"
XES_BOOLEAN = "boolean"
XES_ID = "id"
XES_LIST = "list"

XES_ATTRIBUTE_NAMES = ["string", "date", "int", "float", "boolean", "id", "list"]


class XesLoader:
    """
    loads XML into internal log structure with some further assumptions about the data.

    Loader makes the following assumptions (ignoring that the XES standard permits):
    - all attribute keys within a single attributable are unique
    - all attributes with same keys on the same level (trace, event) have the same type
    - other...

    """

    def __init__(
        self,
        nlogger: NestedLogger = NestedLogger.default(),
        option_extract_xml_skeleton: bool = True,
        option_drop_timezones: bool = True,
        option_load_traces: int | list[int] | None = None,
        option_event_attribute_key_allowlist: list[str] | None = None,
        option_generate_case_concept_name: bool = True,
        option_skip_list_attributes: bool = True,
    ):
        self.nlogger = nlogger
        self.option_extract_xml_skeleton = option_extract_xml_skeleton
        self.option_drop_timezones = option_drop_timezones
        self.option_load_traces = option_load_traces
        self.option_event_attribute_key_allowlist = option_event_attribute_key_allowlist
        self.option_generate_case_concept_name = option_generate_case_concept_name
        self.option_skip_list_attributes = option_skip_list_attributes

    def load(self, file_path: str) -> XesLog:
        # Process outline (Multiple passes):
        # 1. file_path -> Read xml -> Intermediate structure (XML)
        # 2. Intermediate structure (XML) -> Collect stats -> stats
        # 3. Intermediate structure (XML), stats -> Process intermediate structure -> compiled XES
        # 3b. Print warnings about assumptions (e.g. data type guesses)
        # 4. Return compiled XES

        # Initialize

        # 1. Read xml -> Intermediate structure (XML)
        with self.nlogger.action_logging("Loading XML"):
            self.tree = ET.parse(file_path)

        with self.nlogger.action_logging("Removing namespaces from XML file"):
            maxes.utils.xml_remove_namespaces(self.tree)

        with self.nlogger.action_logging("Collecting XML traces"):
            self.xml_log = self.tree.getroot()
            self.xml_traces = [
                node
                for node in self.xml_log
                if xml_tag_without_namespace(node.tag) == "trace"
            ]

        with self.nlogger.action_logging("Collecting XML events"):
            self.xml_events = [
                node
                for xml_trace in self.xml_traces
                for node in xml_trace
                if xml_tag_without_namespace(node.tag) == "event"
            ]

        # 2. Collect stats, validate
        self.errors = []

        self._trace_attribute_types_stats = self._collect_attribute_types(
            self.xml_traces
        )
        self._validate_trace_attribute_types()
        self._trace_attribute_type_map = self._guess_attribute_data_types(
            self._trace_attribute_types_stats
        )
        # self._trace_attributes_info = {
        #     attribute: {
        #         "data_type": self._trace_attribute_type_map[attribute],
        #         "statistical_data_type": self._trace_attribute_type_map[attribute] in ["int"]
        #     }
        #     for attribute in self._trace_attribute_type_map.values()
        # }

        self._event_attribute_types_stats = self._collect_attribute_types(
            self.xml_events
        )
        self._validate_event_attribute_types()
        self._event_attribute_type_map = self._guess_attribute_data_types(
            self._event_attribute_types_stats
        )

        # TODO:
        # Ensure all attributes are always present
        # Or add an option to fill with null/default values

        # Ensure all attributes appear not more than once per <attributable>

        # [-] Ensure only supported attributes in events

        # Calculate numerability for all attributes
        # for example if attribute is of type int, it might be that it is actually categorical data,
        # e.g. attribute of type int with data 1, 1, 1, 1, 5, 5, 5, 5, 5,
        # is actually categorical, and we should not generate integers 2, 3 and 4

        # 3. Process, compile
        xes_log = XesLog()

        xes_log.trace_attributes_info = self._collect_attribute_infos(
            self._trace_attribute_type_map
        )
        xes_log.event_attributes_info = self._collect_attribute_infos(
            self._event_attribute_type_map
        )

        for xml_trace in self.xml_traces:
            xes_trace = XesTrace()

            # Attributes
            xes_trace.attributes = self.parse_trace_attributes_dict(xml_trace)

            # Events
            xml_events = [
                node
                for node in xml_trace
                if xml_tag_without_namespace(node.tag) == "event"
            ]
            for xml_event in xml_events:
                event_attributes = self.parse_event_attributes_dict(xml_event)
                xes_event = XesEvent(event_attributes)
                xes_trace.events.append(xes_event)

            xes_trace.df = pd.DataFrame(
                [event.attributes for event in xes_trace.events]
            )

            xes_log.traces.append(xes_trace)

        if self.option_generate_case_concept_name:
            for i, trace in enumerate(xes_log.traces):
                trace[CONCEPT_NAME] = XesAttribute(
                    key="concept:name",
                    raw_value=str(i + 1),
                    parsed_value=i + 1,
                    xes_type=XesTypeEnum.INT,
                )

        xes_log.update_df()

        self._extract_xml_skeleton()

        xes_log.loader = self

        # TODO: Return LoadResult with: warnings, performance measurements, result

        return xes_log

    def _validate_trace_attribute_types(self):
        self._validate_attributable_attribute_types(
            self._trace_attribute_types_stats, "Trace"
        )

    def _validate_event_attribute_types(self):
        self._validate_attributable_attribute_types(
            self._event_attribute_types_stats, "Event"
        )

    def _validate_attributable_attribute_types(
        self,
        attributable_attribute_types_stats: dict[str, dict[str, int]],
        attributable_name: str,
    ):
        for (
            attribute_key,
            attribute_data_types,
        ) in attributable_attribute_types_stats.items():
            appeared_data_types = {
                data_type: count
                for data_type, count in attribute_data_types.items()
                if count >= 1
            }
            if len(appeared_data_types) >= 2:
                types_text = [
                    f"{data_type}: {count}"
                    for data_type, count in appeared_data_types.items()
                ]
                types_text = ", ".join(types_text)
                error_message = f"{attributable_name} attribute {attribute_key} has multiple types: {types_text}"
                self.errors.append(error_message)

    def _collect_attribute_types(
        self, attributables: list[ET.Element]
    ) -> defaultdict[str, defaultdict[str, int]]:
        attributes_type_stats = defaultdict(lambda: defaultdict(lambda: 0))

        for xml_attributable in attributables:
            xml_attributes = self._get_xes_attributes(xml_attributable)

            for xml_attribute in xml_attributes:
                data_type = xml_tag_without_namespace(xml_attribute.tag).lower()
                key = xml_attribute.attrib["key"]

                attributes_type_stats[key][data_type] += 1

        return attributes_type_stats

    def _get_xes_attributes(self, attributable: ET.Element) -> list[ET.Element]:
        return [
            attribute
            for attribute in attributable
            if xml_tag_without_namespace(attribute.tag) in XES_ATTRIBUTE_NAMES
        ]

    def is_load_trace(self, trace_index: int) -> bool:
        if self.option_load_traces is None:
            return True

        load_traces = self.option_load_traces

        return (
            isinstance(load_traces, list)
            and trace_index in load_traces
            or isinstance(load_traces, int)
            and trace_index < load_traces
        )

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

    def parse_trace_attributes_dict(self, xml_trace: ET.Element) -> dict[str, any]:
        return self.parse_attributes_dict(xml_trace, self._trace_attribute_type_map)

    def parse_event_attributes_dict(self, xml_event: ET.Element) -> dict[str, any]:
        return self.parse_attributes_dict(xml_event, self._event_attribute_type_map)

    def parse_attributes_dict(
        self,
        xml_xes_attributes_container: ET.Element,
        attribute_data_type_map: dict[str, str],
    ) -> dict[str, any]:
        xml_attributes = self._get_xes_attributes(xml_xes_attributes_container)
        attributes_dict = dict()

        for xml_attribute in xml_attributes:
            key = xml_attribute.attrib["key"]
            xes_type = XesTypeEnum(attribute_data_type_map[key])
            raw_value = (
                None if xes_type == XesTypeEnum.LIST else xml_attribute.attrib["value"]
            )
            parsed_value = self.parse_attribute_value(raw_value, xes_type)

            attribute = XesAttribute(
                key=key,
                raw_value=raw_value,
                xes_type=xes_type,
                parsed_value=parsed_value,
            )

            attributes_dict[key] = attribute

        return attributes_dict

    def parse_attribute(self, attribute_node: xml.dom.minidom.Element) -> XesAttribute:
        data_type = attribute_node.nodeName
        key = attribute_node.attributes["key"].value
        raw_value = attribute_node.attributes["value"].value
        parsed_value = self.parse_attribute_value(raw_value, data_type)

        return XesAttribute(data_type=data_type, key=key, value=parsed_value)

    def parse_attribute_value(self, value: str, value_type: XesTypeEnum):
        if value_type == XesTypeEnum.STRING or value_type == XesTypeEnum.ID:
            return str(value)
        if value_type == XesTypeEnum.INT:
            return int(value)
        if value_type == XesTypeEnum.FLOAT:
            return float(value)
        if value_type == XesTypeEnum.BOOLEAN:
            return value.lower() == "true"
        if value_type == XesTypeEnum.DATE:
            value = dateutil.parser.isoparse(value)
            if self.option_drop_timezones:
                value = value.astimezone(timezone.utc)
            return value
        if value_type == XesTypeEnum.LIST:
            if self.option_skip_list_attributes:
                return None
            else:
                raise NotImplementedError()

        raise ValueError("Unknown attribute type", value_type)

    def allow_event_attribute(self, event_attribute_key: str) -> bool:
        return (
            self.option_event_attribute_key_allowlist is None
            or isinstance(self.option_event_attribute_key_allowlist, list)
            and event_attribute_key in self.option_event_attribute_key_allowlist
        )

    def _extract_xml_skeleton(self):
        if not self.option_extract_xml_skeleton:
            return

        root_element = ET.Element(self.xml_log.tag, self.xml_log.attrib)

        for child in self.xml_log:
            if xml_tag_without_namespace(child.tag) == "trace":
                continue

            copied_element = copy.deepcopy(child)
            root_element.append(copied_element)

        self.xml_log_skeleton = ET.ElementTree(root_element)

    def _guess_attribute_data_types(
        self, attribute_types_stats: dict[str, dict[str, int]]
    ) -> dict[str, str]:
        attribute_to_type_map = {}

        for attribute, data_types_stats in attribute_types_stats.items():
            data_type = None

            # If attribute appears as "string" at least once, use "string" as its type
            # Example: "Activity Code" attribute in "Real-life event logs - Hospital log_1_all/Hospital_log.xes/Hospital_log.xes"
            if "string" in data_types_stats:
                data_type = "string"

            # Otherwise it is the most type it appears with
            else:
                data_type = max(data_types_stats, key=data_types_stats.get)

            # TODO: there might be more edge cases

            attribute_to_type_map[attribute] = data_type

        return attribute_to_type_map

    def _collect_attribute_infos(
        self, attribute_to_type: dict[str, str]
    ) -> dict[str, AttributeInfo]:
        attribute_infos = {}

        for attribute, xes_type_str in attribute_to_type.items():
            attribute_info = AttributeInfo()
            attribute_info.name = attribute
            attribute_info.xes_type = XesTypeEnum(xes_type_str)

            attribute_infos[attribute] = attribute_info

        return attribute_infos
