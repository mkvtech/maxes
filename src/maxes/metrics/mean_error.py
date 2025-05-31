import typing

import maxes.utils
from maxes.xes_loader2 import XesLog, XesTrace, XesEvent, XES_STRING, XES_INT, XES_DATE

def calculate_mean_log_error(
        original_log: XesLog,
        generated_log: XesLog,
        trace_mapping: list[tuple[int, int]] | typing.Literal["sequential"] | typing.Literal["best"] | None,
        attribute_weights: dict[str, float] | None = None
        ) -> float:
    if attribute_weights is None:
        attribute_weights = _create_attributes_weights(original_log)

    if trace_mapping == "sequential":
        original_log_traces_count = len(original_log.traces)
        generated_log_traces_count = len(generated_log.traces)
        if original_log_traces_count != generated_log_traces_count:
            raise ValueError(f"Original log has {original_log_traces_count} traces, but generated log has {generated_log_traces_count} traces")

        trace_mapping = []
        for i in range(len(original_log.traces)):
            trace_mapping.append((i, i))

    if trace_mapping == "best":
        raise NotImplementedError()

    accumulated_error = 0

    for original_trace_index, generated_trace_index in trace_mapping:
        original_trace = original_log.traces[original_trace_index]
        generated_trace = generated_log.traces[generated_trace_index]

        trace_error, _event_mapping = calculate_mean_trace_error(
            original_trace,
            generated_trace,
            original_log=original_log,
            event_attribute_type_map=original_log.event_attribute_type_map,
            attributes_weights=attribute_weights
        )

        accumulated_error += trace_error

    mean_log_error = accumulated_error / float(len(trace_mapping))

    return mean_log_error

class EventMappingItem(typing.NamedTuple):
    original_event: XesEvent
    original_event_index: int
    generated_event: XesEvent
    generated_event_index: int
    error: float

def calculate_attributes_range_lengths(original_log: XesLog, original_trace: XesTrace) -> dict[str, float]:
    attributes_range_lengths: dict[str, float] = {}

    for attribute_name, attribute_type in original_log.event_attribute_type_map.items():
        range_length = None

        if attribute_type == XES_INT:
            series = original_trace.df[attribute_name]
            range_length = series.max() - series.min()

        if attribute_type == XES_DATE:
            series = original_trace.df[attribute_name]
            range_length = (series.max() - series.min()).seconds

        if range_length != None:
            attributes_range_lengths[attribute_name] = range_length

    return attributes_range_lengths

def calculate_mean_trace_error(
        original_trace: XesTrace,
        generated_trace: XesTrace,

        original_log: XesLog,
        event_attribute_type_map: dict[str, str],
        attributes_weights: dict[str, float]
        ) -> tuple[float, any]:
    accumulated_error = 0.0
    event_mapping: list[EventMappingItem] = []

    attributes_range_lengths = calculate_attributes_range_lengths(original_log, original_trace)

    for original_event_index, original_event in enumerate(original_trace.events):

        generated_events_candidates: list[EventMappingItem] = []
        for generated_event_index, generated_event in enumerate(generated_trace.events):
            error = calculate_mean_event_error(
                original_event,
                generated_event,
                event_attribute_type_map=event_attribute_type_map,
                attributes_range_lengths=attributes_range_lengths,
                attributes_weights=attributes_weights
            )

            pair = EventMappingItem(
                original_event=original_event,
                original_event_index=original_event_index,
                generated_event=generated_event,
                generated_event_index=generated_event_index,
                error=error
            )
            generated_events_candidates.append(pair)

        if len(generated_events_candidates) == 0:
            continue

        suitable_event_with_error = min(generated_events_candidates, key=lambda pair: pair.error)
        event_mapping.append(suitable_event_with_error)
        accumulated_error += suitable_event_with_error.error

    mean_error = accumulated_error / float(len(original_trace.events))
    return mean_error, event_mapping

def calculate_mean_event_error(
        original_event: XesEvent,
        generated_event: XesEvent,

        event_attribute_type_map: dict[str, str],
        attributes_range_lengths: dict[str, float],
        attributes_weights: dict[str, float]
        ) -> float:
    event_error = 0

    for attribute_name, attribute_type in event_attribute_type_map.items():
        attribute_error = 0

        original_value = original_event.attributes.get(attribute_name)
        generated_value = generated_event.attributes.get(attribute_name)

        if attribute_type == XES_STRING:
            if original_value != generated_value:
                attribute_error = 1

        if attribute_type == XES_INT:
            delta = original_value - generated_value
            scaled_delta = delta / attributes_range_lengths[attribute_name]
            attribute_error = scaled_delta ** 2

        if attribute_type == XES_DATE:
            delta = original_value.second - generated_value.second
            scaled_delta = delta / attributes_range_lengths[attribute_name]
            attribute_error = scaled_delta ** 2

        weighted_attribute_error = attribute_error * attributes_weights[attribute_name]
        event_error += weighted_attribute_error

    return event_error

def _create_attributes_weights(
        log: XesLog,
        string_weight=1.0,
        int_weight=1.0,
        date_weight=1.0
        ) -> dict[str, float]:
    attributes_weights: dict[str, float] = {}

    for attribute_name, attribute_type in log.event_attribute_type_map.items():
        weight = 1.0

        if attribute_type == XES_STRING:
            weight = string_weight
        elif attribute_type == XES_INT:
            weight = int_weight
        elif attribute_type == XES_DATE:
            weight = date_weight

        attributes_weights[attribute_name] = weight

    return maxes.utils.normalize(attributes_weights)
