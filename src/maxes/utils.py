from contextlib import contextmanager
import logging
import urllib.request
import xml.etree.ElementTree as ET
from itertools import tee, chain, filterfalse, combinations
import pandas as pd
import numpy as np
import timeit


class CustomStackOverflowException(Exception):
    """
    Custom Stack Overflow Exception for when u need to stop algorithm that is exceeding some artificial limit. For example, u can raise this exception when implementing a DFS and u dont want to go deeper than N nodes.
    """

    pass


def noop():
    """
    does nothing

    Parameters
    ----------

    no parameters

    ⏎ Returns
    ---------

    nothing

    Examples
    --------

    ```python
    noop()
    ```

    Raises
    ------

    it doesn't

    Notes
    -----

    no notes
    """

    pass


def choice[T](weights: dict[T, float], rng: np.random.Generator = np.random) -> T:
    return choices(weights, 1, rng=rng)[0]


def choices[T](
    weights: dict[T, float], size: int = 1, rng: np.random.Generator = np.random
) -> T:
    """
    WARNING: Use WeightedSampler, with pre-calculated weights and pre-initialized rng

    given options and their weights, returns `size` random choices

    # 💿 Parameters

    ## `weights`

    ```python
    { "common": 100, "rare": 10", "epic": 1, "legendary": 0.1 }
    ```

    # ⏎ Returns

    random element, but based on weight

    """

    np_weights = np.array([weight for weight in weights.values()])
    np_weights = np_weights / np_weights.sum()

    picked_indexes = rng.choice(
        np.arange(len(weights)), size=size, replace=True, p=np_weights
    )
    values = list(weights.keys())

    return [values[i] for i in picked_indexes]


def my_draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=10,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    rotate=True,
    clip_on=True,
    rad=0,
):
    """Draw edge labels.

    Source: https://stackoverflow.com/a/70245742

    Parameters
    ----------
    G : graph
        A networkx graph

    pos : dictionary
        A dictionary with nodes as keys and positions as values.
        Positions should be sequences of length 2.

    edge_labels : dictionary (default={})
        Edge labels in a dictionary of labels keyed by edge two-tuple.
        Only labels for the keys in the dictionary are drawn.

    label_pos : float (default=0.5)
        Position of edge label along edge (0=head, 0.5=center, 1=tail)

    font_size : int (default=10)
        Font size for text labels

    font_color : string (default='k' black)
        Font color string

    font_weight : string (default='normal')
        Font weight

    font_family : string (default='sans-serif')
        Font family

    alpha : float or None (default=None)
        The text transparency

    bbox : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for edge labels.
        Default is {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}.

    horizontalalignment : string (default='center')
        Horizontal alignment {'center', 'right', 'left'}

    verticalalignment : string (default='center')
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

    ax : Matplotlib Axes object, optional
        Draw the graph in the specified Matplotlib axes.

    rotate : bool (deafult=True)
        Rotate edge labels to lie parallel to edges

    clip_on : bool (default=True)
        Turn on clipping of edge labels at axis boundaries

    Returns
    -------
    dict
        `dict` of labels keyed by edge

    Examples
    --------
    >>> G = nx.dodecahedral_graph()
    >>> edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw
    draw_networkx
    draw_networkx_nodes
    draw_networkx_edges
    draw_networkx_labels
    """
    import matplotlib.pyplot as plt
    import numpy as np

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5 * pos_1 + 0.5 * pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0, 1), (-1, 0)])
        ctrl_1 = linear_mid + rad * rotation_matrix @ d_pos
        ctrl_mid_1 = 0.5 * pos_1 + 0.5 * ctrl_1
        ctrl_mid_2 = 0.5 * pos_2 + 0.5 * ctrl_1
        bezier_mid = 0.5 * ctrl_mid_1 + 0.5 * ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items


def sizeof_fmt(num, suffix="B"):
    """
    Prints file size in human-readable form. Stolen from: https://stackoverflow.com/a/1094933.

    Supports:
        - all currently known binary prefixes
        - negative and positive numbers
        - numbers larger than 1000 Yobibytes
        - arbitrary units (maybe you like to count in Gibibits!)
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def xml_tag_without_namespace(tag: str | ET.Element):
    """
    Returns XML tag without XML namespace.

    Namespace notation in XML: `<xes:log>`
    Namespace notation in Python's ElementTree package: `'{http://www.xes-standard.org}log'`
    Returns: `log`
    """

    if isinstance(tag, ET.Element):
        tag = tag.tag

    return tag.rpartition("}")[2]


def xml_remove_namespaces(xml_tree: ET.ElementTree):
    """
    ! Modifies given argument !

    Removes all namespaces from all tags in XML tree.
    """
    for el in xml_tree.iter():
        _, _, el.tag = el.tag.rpartition("}")

    return xml_tree


@contextmanager
def action_logging(message: str, enable: bool = True):
    if enable:
        logging.info("start;    " + message)
    yield
    if enable:
        logging.info("complete; " + message)


@contextmanager
def measured_time():
    start = timeit.default_timer()
    elapser = lambda: timeit.default_timer() - start
    yield lambda: elapser()
    end = timeit.default_timer()
    elapser = lambda: end - start


def with_time(func, *args, **kwargs):
    """
    Note: consider `with measured_time() as timer:` instead, for better IDE support, as this will hide argument types
    """
    start_time = timeit.default_timer()
    return_value = func(*args, **kwargs)
    end_time = timeit.default_timer()
    return return_value, end_time - start_time


def normalize(d: dict) -> dict:
    """Normalizes given dictionary (vector), so that sum of all values equals to 1

    Args:
        d (dict): Dictionary (vector) to normalize

    Returns:
        dict: Normalized dictionary (vector)
    """

    s = float(sum(d.values()))
    return {key: float(value) / s for key, value in d.items()}


import tqdm


class DownloadProgressBar(tqdm.tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_with_progress_bar(url, output_path):
    with DownloadProgressBar(
        unit="B", unit_scale=True, miniters=1, desc=url.split("/")[-1]
    ) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


# Source: https://docs.python.org/3/library/itertools.html#itertools.filterfalse
def partition(iterable, pred):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


# Source: https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    "Subsequences of the iterable from shortest to longest."
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def reorder_xes_columns(df: pd.DataFrame):
    special_columns = [
        "case:concept:name",
        "concept:name",
        "lifecycle:transition",
        "time:timestamp",
    ]

    df_special_columns = [column for column in special_columns if column in df.columns]
    df_other_columns = [
        column for column in df.columns if column not in special_columns
    ]
    new_columns = df_special_columns + df_other_columns

    return df[new_columns]


def remap(value: float, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((value - old_min) * new_range) / old_range) + new_min


def dset(d: dict, *args):
    if len(args) <= 1:
        raise ValueError("Not enough args")

    for key in args[:-2]:
        d = d.setdefault(key, {})

    d[args[-2]] = args[-1]


def dig(d: dict, *args):
    if len(args) <= 1:
        raise ValueError("Not enough args")

    for key in args:
        d = d.get(key)
        if d is None:
            return

    return d
