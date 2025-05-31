import networkx as nx
import typing
import maxes.utils
import numpy as np

from maxes.models.models import WeightedSampler
from maxes.utils import powerset


class RandomWeightedTraverser:
    def __init__(
        self,
        rng: np.random.Generator,
        min_steps: int,
        max_steps: int,
        recursion_limit=40000,
        weight_feature_name="weight",
        first_node_weight_feature_name="first",
        last_node_weight_feature_name="last",
    ):
        self.rng = rng
        self.min_steps = min_steps
        self.max_steps = max_steps
        self.recursion_limit = recursion_limit
        self.weight_feature_name = weight_feature_name
        self.first_node_weight_feature_name = first_node_weight_feature_name
        self.last_node_weight_feature_name = last_node_weight_feature_name

    def fit(self, graph: nx.DiGraph):
        self.graph_ = graph

        first_node_weights = {
            node: data[self.first_node_weight_feature_name]
            for node, data in graph.nodes.items()
            if data.get(self.first_node_weight_feature_name)
        }
        self.first_node_sampler_ = WeightedSampler(self.rng).fit(first_node_weights)

        last_node_weights = {
            node: data[self.last_node_weight_feature_name]
            for node, data in graph.nodes.items()
            if data.get(self.last_node_weight_feature_name)
        }
        self.last_node_sampler_ = WeightedSampler(self.rng).fit(last_node_weights)

        # TODO: Validate if it is possible to construct a sequence of min_steps, max_steps
        # Or better: instead of sampling first and last nodes individually, sample pairs
        # and filter out impossible pairs

        self.neighbor_samplers_ = {}
        for start_node in graph.nodes:
            self.neighbor_samplers_[start_node] = {}

            neighbor_nodes = graph[start_node]

            for s in powerset(neighbor_nodes):
                if len(s) == 0:
                    continue

                s = frozenset(s)

                self.neighbor_samplers_[start_node][s] = {}

                weights = {}
                for neighbor_node in s:
                    weight = graph[start_node][neighbor_node][self.weight_feature_name]
                    weights[neighbor_node] = weight

                sampler = WeightedSampler(self.rng).fit(weights)
                self.neighbor_samplers_[start_node][s] = sampler

        return self

    def sample(self, n_samples=1):
        if n_samples != 1:
            raise NotImplementedError("n_samples != 1 is not supported")

        first_node = self.first_node_sampler_.sample()[0]
        last_node = self.last_node_sampler_.sample()[0]

        sequence = random_weighted_traverse(
            graph=self.graph_,
            first_node_name=first_node,
            last_node_name=last_node,
            min_steps=self.min_steps,
            max_steps=self.max_steps,
            neighbor_samplers=self.neighbor_samplers_,
            recursion_limit=self.recursion_limit,
        )
        return [sequence]


def random_weighted_traverse(
    graph: nx.DiGraph,
    max_steps: int,
    first_node_name,
    last_node_name,
    neighbor_samplers: dict[any, dict[set[any], WeightedSampler]],
    min_steps: int = 0,
    recursion_limit: int = 40_000,
    update_step: typing.Callable[[list[str]], None] | None = None,
) -> list:

    current_node_name = first_node_name
    function_stack: list[list[str]] = [[current_node_name], []]

    i = 0
    while True:
        i += 1
        if i > recursion_limit:
            raise maxes.utils.CustomStackOverflowException("Hit recursion limit")

        current_depth = len(function_stack)

        if callable(update_step):
            sequence = []

            for visited in function_stack:
                if len(visited) > 0:
                    sequence.append(visited[-1])

            update_step(sequence)

        if current_depth == 0:
            # no path that satisfies conditions of min_steps, max_steps
            return []

        if current_depth == 1:
            # no path that satisfies conditions
            return []

        if current_depth > max_steps:
            function_stack.pop()
            continue

        current_node_name = function_stack[-2][-1]
        neighbor_names = graph[current_node_name].keys()

        if len(neighbor_names) == 0:
            # node without neighbors
            function_stack.pop()
            continue

        current_context = function_stack[-1]

        unvisited_neighbor_names = frozenset(
            n for n in neighbor_names if n not in current_context
        )

        if len(unvisited_neighbor_names) == 0:
            # all neighbor nodes are already visited
            function_stack.pop()
            continue

        sampler = neighbor_samplers[current_node_name][unvisited_neighbor_names]
        next_node_name = sampler.sample()[0]

        next_node_data = graph.nodes[next_node_name]

        current_context.append(next_node_name)

        if next_node_data.get("last"):
            if current_depth < min_steps:
                function_stack.pop()
                continue
            if current_depth >= min_steps and next_node_name == last_node_name:
                # success
                break

        function_stack.append([])

    return [visited[-1] for visited in function_stack]
