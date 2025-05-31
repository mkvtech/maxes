# import ete3 as ete
import functools
import networkx as nx
import pandas as pd
import typing

from maxes.xes_loader2 import XesLog


from maxes.constants import CONCEPT_NAME, LIFECYCLE_TRANSITION


DEFAULT_SEQUENCE_KEYS = [CONCEPT_NAME, LIFECYCLE_TRANSITION]


def get_sequence_keys(columns: list[str]):
    if CONCEPT_NAME not in columns:
        raise ValueError("concept:name column is required")

    result = [CONCEPT_NAME]

    if LIFECYCLE_TRANSITION in columns:
        result.append(LIFECYCLE_TRANSITION)

    return result


def analyze_xes_log_sequence(xes: XesLog, sequence_keys: list[str] | None = None):
    if sequence_keys is None:
        sequence_keys = get_sequence_keys(xes.df.columns)

    sequences = [
        analyze_xes_trace_sequence(trace.df, sequence_keys=sequence_keys)
        for trace in xes.traces
    ]
    sequence = merge_graphs(
        sequences, resolve_node_conflict="add", resolve_edge_conflict="add"
    )
    return sequence


def analyze_xes_trace_sequence(df: pd.DataFrame, sequence_keys=DEFAULT_SEQUENCE_KEYS):
    def initialize_edge():
        return {"frequency": 0, "transition_durations": []}

    def collect_edge(edge, current_event: pd.Series, next_event: pd.Series):
        edge["frequency"] += 1

        transition_duration = abs(
            next_event["time:timestamp"] - current_event["time:timestamp"]
        )
        edge["transition_durations"].append(transition_duration)

    return analyze_sequence(
        df,
        sequence_keys=sequence_keys,
        initialize_edge=initialize_edge,
        collect_edge=collect_edge,
    )


def analyze_sequence(
    df: pd.DataFrame,
    sequence_keys: (
        str | list[str] | typing.Callable[[pd.Series], str]
    ) = DEFAULT_SEQUENCE_KEYS,
    next_event_filter: (
        None | str | list[str] | typing.Callable[[pd.DataFrame, pd.Series], pd.Series]
    ) = None,
    initialize_edge: typing.Callable[[], dict] = lambda: {"frequency": 0},
    collect_edge: None | typing.Callable[[any, pd.Series, pd.Series], None] = None,
) -> nx.DiGraph:
    """
    returns sequence graph of specified columns in dataframe.

    Parameters
    ----------

    df : pd.DataFrame
        pandas dataframe that will be analyzed
    sequence_keys : str | list[str]
        dataframe columns that make up a node in graph
    next_event_filter : None | str | list[str]
        if None: will just take next event in sequence,
        if str or list[str]: will take next event that has the same values on given column(s),
        if Callable: i will give u a dataframe with all events after current event and current event and u do ur own filtering

    📝 Notes
    --------

    u might want to filter the dataframe before calling this method, like this:

    ```python
    analyze_sequence(df[df["lifecycle:transition" == "start"]])
    ```
    """

    # Initialize sequence_keys
    generate_key = None
    if isinstance(sequence_keys, str):

        def generate_key(series):
            return series.loc[sequence_keys]

    elif isinstance(sequence_keys, list):

        def generate_key(series):
            return tuple(series.loc[key] for key in sequence_keys)

    else:
        generate_key = sequence_keys

    # Initialize next_event_filter
    find_next_events = None
    if callable(next_event_filter):
        find_next_events = next_event_filter
    elif isinstance(next_event_filter, str):

        def find_next_events(df, series):
            return df[df[next_event_filter] == series[next_event_filter]]

    elif isinstance(next_event_filter, list):

        def find_next_events(df, series):
            return df[
                functools.reduce(
                    lambda a, b: a & b,
                    [(df[key] == series[key]) for key in next_event_filter],
                )
            ]

    else:

        def find_next_events(df, series):
            return df

    # Initialize collect_edge
    if collect_edge is None:

        def collect_edge(edge, current_event: pd.Series, next_event: pd.Series):
            edge["frequency"] += 1

    # Generate graph
    graph = nx.DiGraph()

    if len(df) == 1:
        key = generate_key(df.iloc[0])
        graph.add_node(key)
        graph.nodes[key]["frequency"] = 1
    else:
        for index, series in df.iterrows():
            current_key = generate_key(series)
            events_after_current = df.loc[index + 1 :]
            events_after_current = find_next_events(events_after_current, series)

            if current_key not in graph.nodes:
                graph.add_node(current_key, frequency=0)
            elif "frequency" not in graph.nodes[current_key]:
                graph.nodes[current_key]["frequency"] = 0

            graph.nodes[current_key]["frequency"] += 1

            if len(events_after_current) == 0:
                continue

            next_event = events_after_current.iloc[0]
            next_event_key = generate_key(next_event)

            edge = (current_key, next_event_key)

            if edge not in graph.edges:
                graph.add_edge(*edge, **initialize_edge())

            edge_view = graph.edges[edge]
            collect_edge(edge_view, series, next_event)

    first_event_key = generate_key(df.iloc[0])
    graph.nodes[first_event_key]["first"] = 1

    last_event_key = generate_key(df.iloc[-1])
    graph.nodes[last_event_key]["last"] = 1

    return graph


def resolve_dict_conflict__add(existing_data: dict, incoming_data: dict):
    for key, value in incoming_data.items():
        if key in existing_data:
            existing_data[key] += value
        else:
            existing_data[key] = value


def resolve_dict_conflict__overwrite(existing_data: dict, incoming_data: dict):
    existing_data.update(incoming_data)


def merge_graphs(
    graphs: nx.DiGraph,
    resolve_node_conflict: (
        typing.Literal["add"]
        | typing.Literal["overwrite"]
        | typing.Callable[[dict, dict], None]
    ) = "add",
    resolve_edge_conflict: (
        typing.Literal["add"]
        | typing.Literal["overwrite"]
        | typing.Callable[[dict, dict], None]
    ) = "add",
):
    result = nx.DiGraph()

    if resolve_node_conflict == "add":
        resolve_node_conflict = resolve_dict_conflict__add
    elif resolve_node_conflict == "overwrite":
        resolve_node_conflict = resolve_dict_conflict__overwrite

    if resolve_edge_conflict == "add":
        resolve_edge_conflict = resolve_dict_conflict__add
    elif resolve_edge_conflict == "overwrite":
        resolve_edge_conflict = resolve_dict_conflict__overwrite

    for other in graphs:
        for node, data in other.nodes.items():
            if node in result.nodes:
                resolve_node_conflict(result.nodes[node], other.nodes[node])
            else:
                result.add_node(node, **data)

        for edge, data in other.edges.items():
            if edge in result.edges:
                resolve_edge_conflict(result.edges[edge], other.edges[edge])
            else:
                result.add_edge(*edge, **data)

    return result
