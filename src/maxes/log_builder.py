import pandas as pd
from maxes.xes_log import XesLog, XesTrace, XesEvent, XesAttribute, AttributeInfo
from maxes.types import XesTypeEnum


def is_trace_level_attribute(name: str):
    return name[:5] == "case:"


class LogBuilder:
    def __init__(
        self,
        event_attributes_types: dict[str, XesTypeEnum] = dict(),
        trace_attributes_types: dict[str, XesTypeEnum] = dict(),
    ):
        self.event_attributes_types = event_attributes_types
        self.trace_attributes_types = trace_attributes_types

    def build_log(self, df: pd.DataFrame) -> XesLog:
        self._trace_attributes_names = [
            column[5:] for column in df.columns if is_trace_level_attribute(column)
        ]
        self._event_attributes_names = [
            column for column in df.columns if not is_trace_level_attribute(column)
        ]

        self._event_attributes_types = self._fill_attributes_types(
            self._event_attributes_names, self.event_attributes_types
        )
        self._trace_attributes_types = self._fill_attributes_types(
            self._trace_attributes_names, self.trace_attributes_types
        )

        self._trace_column_names = [
            f"case:{name}" for name in self._trace_attributes_names
        ]

        log = XesLog()

        for case_concept_name, group in df.groupby("case:concept:name"):
            trace_attributes = self._get_trace_attributes(case_concept_name, group)
            trace = XesTrace(attributes=trace_attributes)
            log.traces.append(trace)

            for index, event in group.iterrows():
                event_attributes = self._collect_attributes(
                    event, type_map=self._event_attributes_types
                )
                event = XesEvent(event_attributes)
                trace.events.append(event)

        log.event_attributes_info = self._collect_attributes_info(
            self._event_attributes_types
        )
        log.trace_attributes_info = self._collect_attributes_info(
            self._trace_attributes_types
        )

        return log

    def _get_trace_attributes(
        self, case_concept_name: str, df: pd.DataFrame
    ) -> dict[str, XesAttribute]:
        nunique = df[self._trace_column_names].nunique()

        columns_with_multiple_values = [
            key for key, value in nunique.items() if value > 1
        ]

        if len(columns_with_multiple_values) > 0:
            raise ValueError(
                f"Case {case_concept_name} contains multiple values for columns {columns_with_multiple_values}"
            )

        series: pd.Series = df.iloc[0][self._trace_column_names]
        return self._collect_attributes(
            series, type_map=self._trace_attributes_types, df_prefix="case:"
        )

    def _fill_attributes_types(self, attributes: list[str], type_map: dict[str, str]):
        new_type_map = dict()

        for attribute in attributes:
            configured_type = type_map.get(attribute)

            if configured_type is None:
                configured_type = XesTypeEnum.STRING
            if configured_type is str:
                configured_type = XesTypeEnum(configured_type)

            new_type_map[attribute] = configured_type

        return new_type_map

    def _collect_attributes(
        self, series: pd.Series, type_map: dict[str, XesTypeEnum], df_prefix: str = ""
    ) -> dict[str, XesAttribute]:
        attributes = dict()

        for name, xes_type in type_map.items():
            column = df_prefix + name
            value = series[column]

            attribute = XesAttribute(
                key=name,
                raw_value=value,
                parsed_value=value,
                xes_type=xes_type,
            )
            attributes[name] = attribute

        return attributes

    def _collect_attributes_info(self, type_map: dict[str, XesTypeEnum]):
        attributes_info = {}

        for name, xes_type in type_map.items():
            attribute_info = AttributeInfo()
            attribute_info.name = name
            attribute_info.xes_type = xes_type

            attributes_info[name] = attribute_info

        return attributes_info
