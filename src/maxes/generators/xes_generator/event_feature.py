import typing
import pandas as pd
from __future__ import annotations

VALID_EVENT_FEATURE_TYPES = [
    "attribute", # Original attribute value
    "le", # Label encoding
    "delta", # Value difference from previous event
    "meta",
]

class EventFeature():
    def __init__(
            self,
            type: typing.Literal["attribute", "le", "delta", "meta"],
            name: str,
            statistical_type: typing.Literal["numerical", "categorical"]
        ):
        if type not in VALID_EVENT_FEATURE_TYPES:
            raise ValueError(f"Invalid event feature type: {type}")

        self.type = type
        self.name = name
        self.statistical_type = statistical_type

    @property
    def id(self):
        return f"{self.type}__{self.name}"

class EventFeature2():

    def __init__(
            self,
            attributes: list[str],
            compute_action_df: str | typing.Callable[[EventFeature2, pd.DataFrame], list[float]] | None,
            compute_action_single: str | typing.Callable[[EventFeature2, list], float] | None
        ):
        """_summary_

        Args:
            attributes (list[str]): Attributes (at least one) that this feature is computed from
            compute_action_df (str | typing.Callable[[EventFeature2, pd.DataFrame], float] | None): Instruction on how to compute multiple instances this feature in bulk from Pandas DataFrame
            compute_action_single (str | typing.Callable[[EventFeature2, list], float] | None): Instruction on how to compute single instance of this feature from list of parameters
        """
        self.attributes = attributes
        self.compute_action_df = compute_action_df
        self.compute_action_single = compute_action_single

    def compute_multiple(self, df: pd.DataFrame):
        return self.compute_action_df(self, df)

    def compute_single(self, input: list) -> float:
        return self.compute_action_single(self, input)

    @property
    def id(self):
        return f"{self.type}__{self.name}"
