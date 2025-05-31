import typing

import networkx as nx
import matplotlib.pyplot as plt

import maxes.utils

NODE_COLOR = "#BFBFBF"
NODE_COLOR_FIRST = "#BEFFC7"
NODE_COLOR_LAST = "#FC814A"


def draw_xes_sequence_graph_nodes(
    graph: nx.DiGraph,
    pos: dict[any, tuple[float, float]],
    ax,
    node_size_range: tuple[float, float] = None,
    node_size: float | int | dict[any, float] | typing.Literal["weight"] = 300,
):
    # Calculate node sizes
    if isinstance(node_size, float) or isinstance(node_size, int):
        node_size = {node: node_size for node in graph.nodes.keys()}
    elif isinstance(node_size, str):
        result = {}

        node_to_value = {node: data[node_size] for node, data in graph.nodes.items()}
        min_value = min(node_to_value.values())
        max_value = max(node_to_value.values())

        for node, data in graph.nodes.items():
            value = data[node_size]
            new_size = maxes.utils.remap(
                value,
                min_value,
                max_value,
                node_size_range[0],
                node_size_range[1],
            )

            result[node] = new_size

        node_size = result

    for node, data in graph.nodes.items():
        nx_node_shape = None
        nx_node_color = None
        if data.get("first"):
            nx_node_shape = "s"
            nx_node_color = NODE_COLOR_FIRST
        elif data.get("last"):
            nx_node_shape = "s"
            nx_node_color = NODE_COLOR_LAST
        else:
            nx_node_shape = "o"
            nx_node_color = NODE_COLOR

        nx_node_size = node_size[node]

        nx.draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            nodelist=[node],
            node_shape=nx_node_shape,
            node_color=nx_node_color,
            node_size=nx_node_size,
        )


def draw_xes_log_graph__node_labels(
    graph: nx.DiGraph,
    pos: dict[any, tuple[float, float]],
    ax,
):
    def get_node_label(node, data):
        extra = []

        if data.get("first"):
            extra.append(data["first"])
        if data.get("last"):
            extra.append(data["last"])

        extra = ", ".join(str(item) for item in extra)
        extra = f" ({extra})" if len(extra) > 0 else ""
        return f"{node}{extra}"

    node_labels = {
        node: get_node_label(node, data) for node, data in graph.nodes.items()
    }
    nx.draw_networkx_labels(graph, pos, ax=ax, labels=node_labels)


def draw_xes_sequence_graph_edges(
    graph: nx.DiGraph,
    pos: dict[any, tuple[float, float]],
    ax,
    edge_label: str | None = None,
):
    # Arcs
    edgelist_curved = [edge for edge in graph.edges if reversed(edge) in graph.edges]
    arc_rad = 0.1
    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        edgelist=edgelist_curved,
        connectionstyle=f"arc3, rad = {arc_rad}",
        alpha=0.5,
    )

    # Straight
    edgelist_straight = list(set(graph.edges) - set(edgelist_curved))
    nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=edgelist_straight, alpha=0.5)

    # edge labels
    if edge_label is not None:
        edge_labels = nx.get_edge_attributes(graph, edge_label)

        curved_edge_labels = {edge: edge_labels[edge] for edge in edgelist_curved}
        maxes.utils.my_draw_networkx_edge_labels(
            graph, pos, ax=ax, edge_labels=curved_edge_labels, rotate=False, rad=arc_rad
        )

        straight_edge_labels = {edge: edge_labels[edge] for edge in edgelist_straight}
        nx.draw_networkx_edge_labels(
            graph, pos, ax=ax, edge_labels=straight_edge_labels, rotate=False
        )


def draw_xes_sequence_graph(
    graph: nx.DiGraph,
    pos=None,
    ax=None,
    edge_label: str | None = None,
    node_size: float | dict[str, float] | str = "frequency",
    node_size_range=[100.0, 5000.0],
    node_labels=True,
) -> None:

    if ax is None:
        fig, ax = plt.subplots()

    if pos is None:
        pos = nx.shell_layout(graph)

    def get_node_label(node, data):
        extra = []

        if data.get("first"):
            extra.append(data["first"])
        if data.get("last"):
            extra.append(data["last"])

        extra = ", ".join(str(item) for item in extra)
        extra = f" ({extra})" if len(extra) > 0 else ""
        return f"{node}{extra}"

    draw_xes_sequence_graph_nodes(
        graph, pos=pos, ax=ax, node_size=node_size, node_size_range=node_size_range
    )

    # edges
    draw_xes_sequence_graph_edges(graph, pos, ax, edge_label=edge_label)

    # node labels
    if node_labels:
        node_labels = {
            node: get_node_label(node, data) for node, data in graph.nodes.items()
        }
        nx.draw_networkx_labels(graph, pos, ax=ax, labels=node_labels)
