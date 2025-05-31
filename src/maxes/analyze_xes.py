from collections import Counter, defaultdict
import dateutil
import logging
import os
import time
import typing
import math

import pandas as pd
import numpy as np
import xmlschema

import maxes.constants
import maxes.utils
from maxes.utils import action_logging
from maxes.xes_loader2 import XesLoader

series_type = (
    typing.Literal["categorical"]
    | typing.Literal["numerical"]
    | typing.Literal["unknown"]
)

AUTO_SERIES_TYPES = {
    "time:timestamp": "numerical",
    "concept:name": "categorical",
    "lifecycle:transition": "categorical",
}


class AnalyzeXes:
    """
    Collects useful info about an XES file
    """

    def s_analyze(xes_file_path: str):
        analyzer = AnalyzeXes()
        return analyzer.analyze(xes_file_path)

    def __init__(
        self,
        check_xml_schema_xes_2014=True,
        check_xml_schema_xes_2023=True,
        check_xml_schema_xes_2023_extended=True,
    ):
        self.check_xml_schema_xes_2014 = check_xml_schema_xes_2014
        self.check_xml_schema_xes_2023 = check_xml_schema_xes_2023
        self.check_xml_schema_xes_2023_extended = check_xml_schema_xes_2023_extended

    def analyze(
        self,
        xes_file_path: str,
    ):

        with action_logging("Analyze"):
            start_time = time.time()

            self.xes_file_path = xes_file_path

            logging.info(f'Started analysing "{self.xes_file_path}"')

            self.info = {}

            self.info["File"] = self._collect_info__file()
            self.info["XML"] = self._collect_info__xml__schema_pass()

            with action_logging("Load XML"):
                self.xes_loader = XesLoader()
                self.xes = self.xes_loader.load(self.xes_file_path)
                self.xml_tree = self.xes_loader.tree

            # TODO: XML info, tags counts (int, meta, list, etc)

            with action_logging("Collect XML info"):
                self.info["XML"]["Tags"] = self._collect_info__count_xml_tags(".//*")
                self.info["XML"]["Tags"]["Per level"] = {}
                self.info["XML"]["Tags"]["Per level"]["Log"] = (
                    self._collect_info__count_xml_tags("./*")
                )
                self.info["XML"]["Tags"]["Per level"]["Trace"] = (
                    self._collect_info__count_xml_tags("./trace/*")
                )
                self.info["XML"]["Tags"]["Per level"]["Event"] = (
                    self._collect_info__count_xml_tags("./trace/event/*")
                )

            traces_count = len(self.xes.traces)

            with action_logging("Collect Log info"):
                self.info["Log"] = {}
                self.info["Log"]["Extensions"] = self._collect_info__log__extensions()

            with action_logging("Collect Traces info"):
                self.info["Traces"] = {}
                self.info["Traces"]["Count"] = traces_count

                # TODO: trace level attributes
                # self.info["Traces"]["Attributes"] = {}
                # self.info["Traces"]["Attributes"]["Attributes per trace"] = "TODO"
                # self.info["Traces"]["Attributes"]["Each"] = "TODO"

            with action_logging("Collect Events info"):
                # events_counts_per_trace = np.Array([len(trace.events) for trace in self.xes.traces])
                events_counts_per_trace = pd.Series(
                    [len(trace.events) for trace in self.xes.traces]
                )
                self.events_count = sum(events_counts_per_trace)

                self.info["Events"] = {}
                self.info["Events"]["Count in log"] = self.events_count
                self.info["Events"]["Count per trace"] = self._describe(
                    events_counts_per_trace
                )

                with action_logging("Calculate events attributes counts"):
                    self._event_attributes_counts = (
                        self._calculate_event_attributes_counts()
                    )

                with action_logging("Collect Event/Attributes info"):
                    self.info["Events"]["Attributes"] = {}
                    self.info["Events"]["Attributes"]["Unique count"] = len(
                        self._event_attributes_counts
                    )

                    self.info["Events"]["Attributes"]["Each"] = {}

                    for attribute in self.xes.event_attributes:
                        with action_logging(
                            f"Collect Event/Attributes/Each/{attribute} info"
                        ):
                            self._collect_info__event_attribute(attribute)

                end_time = time.time()
                self.info["Analysis time"] = end_time - start_time

        return self.info

    def _collect_info__file(self):
        info = None

        with action_logging("Collect file info"):
            size_in_bytes = os.path.getsize(self.xes_file_path)

            info = {
                "Path": self.xes_file_path,
                "Size in bytes": size_in_bytes,
                "Size human-readable": maxes.utils.sizeof_fmt(size_in_bytes),
            }

        return info

    def _collect_info__xml__schema_pass(self):
        info = {}

        with action_logging("Collect XML schema results"):
            if self.check_xml_schema_xes_2014:
                with action_logging("Validate with XES 2014 XML schema"):
                    info["XES 2014"] = self._pass_xml_schema(
                        maxes.constants.xml_schema_xes_2014
                    )
            if self.check_xml_schema_xes_2023:
                with action_logging("Validate with XES 2023 XML schema"):
                    info["XES 2023"] = self._pass_xml_schema(
                        maxes.constants.xml_schema_xes_2023
                    )
            if self.check_xml_schema_xes_2023_extended:
                with action_logging("Validate with XES 2023 (Extended) XML schema"):
                    info["XES 2023 (Extended)"] = self._pass_xml_schema(
                        maxes.constants.xml_schema_xes_2023_extended
                    )

        return info

    def _pass_xml_schema(self, schema: xmlschema.XMLSchema):
        start_time = time.time()

        info = {}

        try:
            schema.validate(self.xes_file_path)
            info["Passed"] = True
        except xmlschema.XMLSchemaValidationError as error:
            info["Passed"] = False
            info["Error"] = {
                "Message": error.message,
                "Reason": error.reason,
            }
        except xmlschema.XMLSchemaParseError as error:
            info["Passed"] = False
            info["Error"] = {
                "Message": error.message,
            }

        info["Time"] = time.time() - start_time

        return info

    def _collect_info__count_xml_tags(self, path: str) -> dict[str, int]:
        d = dict(
            Counter(
                maxes.utils.xml_tag_without_namespace(element.tag)
                for element in self.xml_tree.findall(path)
            )
        )

        return {
            "Count": sum(d.values()),
            "Distribution": d,
        }

    def _collect_info__log__extensions(self):
        xml_extensions = [
            child
            for child in self.xml_tree.getroot()
            if maxes.utils.xml_tag_without_namespace(child.tag).lower() == "extension"
        ]

        info = {
            "Count": len(xml_extensions),
            "Each": [
                {
                    "Name": xml_extension.attrib["name"],
                    "Prefix": xml_extension.attrib["prefix"],
                    "uri": xml_extension.attrib["uri"],
                }
                for xml_extension in xml_extensions
            ],
        }
        return info

    def _collect_info__event_attribute(self, attribute: str):
        calculated_attribute_info = self._event_attributes_counts[attribute]
        attribute_info = {}

        attribute_info["Count"] = calculated_attribute_info["Count"]
        attribute_info["Count per type"] = calculated_attribute_info["Count per type"]
        attribute_info["Event count"] = calculated_attribute_info["Event count"]
        attribute_info["Presence %"] = calculated_attribute_info["Presence %"]

        xes_type = self.xes.event_attributes_info[attribute].xes_type.value
        attribute_info["XES type"] = xes_type

        statistical_type = "unknown"
        if xes_type in ["int", "date", "float"]:
            statistical_type = "numerical"
        elif xes_type in ["string", "bool", "id"]:
            statistical_type = "categorical"

        attribute_info["Statistical type"] = statistical_type

        attribute_info_by_statistical_type = {}
        if statistical_type == "numerical":
            attribute_info_by_statistical_type = (
                self._collect_info__numerical_attribute(attribute)
            )
        elif statistical_type == "categorical":
            attribute_info_by_statistical_type = (
                self._collect_info__categorical_attribute(attribute)
            )
        attribute_info = attribute_info | attribute_info_by_statistical_type

        if xes_type == "date":
            xpath = f"./trace/event/date[@key='{attribute}']"
            attribute_info["Timezones"] = self._collect_info__date_time_zones(xpath)

        self.info["Events"]["Attributes"]["Each"][attribute] = attribute_info

    def _collect_info__categorical_attribute(self, attribute: str, top_count: int = 5):
        value_counts = self.xes.df[attribute].value_counts()

        return {
            "Unique values count": len(value_counts),
            "Top values": dict(value_counts.nlargest(top_count)),
        }

    def _collect_info__numerical_attribute(self, attribute: str):
        filtered_traces = [trace for trace in self.xes.traces if attribute in trace.df]
        min_per_trace = np.array(
            [trace.df[attribute].min() for trace in filtered_traces]
        )
        max_per_trace = np.array(
            [trace.df[attribute].max() for trace in filtered_traces]
        )

        avg_span_per_trace = pd.Series(max_per_trace - min_per_trace).mean()

        return {
            "Statistics": self._describe(self.xes.df[attribute]),
            "Mean span": avg_span_per_trace,
        }

    def _collect_info__date_time_zones(self, xpath: str) -> dict[str, int]:
        xml_dates = self.xml_tree.findall(xpath)

        def generator():
            for xml_date in xml_dates:
                date = dateutil.parser.isoparse(xml_date.attrib["value"])
                time_zone = date.tzinfo
                time_zone_offset = time_zone.utcoffset(date)
                yield str(time_zone_offset)

        d = dict(Counter(generator()))
        return {
            "Count": sum(d.values()),
            "Distribution": d,
        }

    def _event_attribute_counts_per_trace(self, event_attribute: str):
        counts_per_trace = [
            sum(event_attribute in event for event in trace.events_raw)
            for trace in self.xes.traces
        ]
        return sum(counts_per_trace), counts_per_trace

    def _str_presence(self, event_attribute: int):
        row = self.event_attributes_counts.loc[
            self.event_attributes_counts["Attribute"] == event_attribute
        ]
        return row["Presence"].to_string(index=False)

    def _calculate_event_attributes_counts(self):
        events_count = 0
        attributes_info = {}

        for xml_event in self.xml_tree.findall("./trace/event"):
            this_event_attributes = set()

            for xml_xes_attribute in xml_event:
                key = xml_xes_attribute.attrib["key"]
                data_type = maxes.utils.xml_tag_without_namespace(xml_xes_attribute.tag)

                attribute_info = None
                if key in attributes_info:
                    attribute_info = attributes_info[key]
                else:
                    attribute_info = {
                        "Count": 0,
                        "Count per type": defaultdict(lambda: 0),
                        "Event count": 0,
                    }
                    attributes_info[key] = attribute_info

                attribute_info["Count"] += 1
                attribute_info["Count per type"][data_type] += 1

                this_event_attributes.add(key)

            for attribute in this_event_attributes:
                attributes_info[attribute]["Event count"] += 1

            events_count += 1

        for attribute_info in attributes_info.values():
            attribute_info["Count per type"] = dict(attribute_info["Count per type"])
            presence = attribute_info["Event count"] / events_count * 100
            attribute_info["Presence %"] = f"{presence:.1f}%"

        return attributes_info

    def _describe(self, series: pd.Series):
        d = dict(series.describe())

        if "std" in d and math.isnan(d["std"]):
            d["std"] = None

        return d
