import copy
import pandas as pd
import xml.etree.ElementTree as ET
from maxes.xes_log import (
    XesLog,
    XesTrace,
    XesEvent,
    XesAttribute,
    XesAttributesCollectionBase,
    AttributeInfo,
    XesTypeEnum,
)


def serialize(log: XesLog) -> ET.ElementTree:
    return Serializer().serialize(log)


class Serializer:
    def __init__(self):
        pass

    def serialize(
        self, log: XesLog, xml_log_skeleton: ET.ElementTree | None = None
    ) -> ET.ElementTree:
        self.log = log
        self.xml_log_skeleton = xml_log_skeleton

        self.xml_log_tree = self._create_root()
        self.xml_log = self.xml_log_tree.getroot()

        for trace in log.traces:
            xtrace = ET.SubElement(self.xml_log, "trace")
            self._append_attributes(trace, xtrace, log.trace_attributes_info)

            for event in trace.events:
                xevent = ET.SubElement(xtrace, "event")
                self._append_attributes(event, xevent, log.event_attributes_info)

        return self.xml_log_tree

    def _create_root(self) -> ET.ElementTree:
        if self.xml_log_skeleton is not None:
            return copy.deepcopy(self.xml_log_skeleton)

        if self.log.loader is not None and self.log.loader.xml_log_skeleton is not None:
            return copy.deepcopy(self.log.loader.xml_log_skeleton)

        return ET.ElementTree(ET.Element("log"))

    def _append_attributes(
        self,
        attributable: XesAttributesCollectionBase,
        xml_element: ET.Element,
        attributes_info: dict[str, AttributeInfo],
    ) -> None:
        for key, attribute in attributable.attributes.items():
            attribute_info = attributes_info[key]
            xes_type = attribute_info.xes_type
            value = attribute.parsed_value

            serialized_value = None
            if xes_type == XesTypeEnum.DATE:
                serialized_value = value.isoformat()
            else:
                serialized_value = str(value)

            tag = xes_type.value

            ET.SubElement(xml_element, tag, {"key": key, "value": serialized_value})
