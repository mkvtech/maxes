import numpy as np
import pandas as pd


class BaseGenerator:
    def fit(self, X):
        return self

    def sample(self, n_samples=1) -> list:
        pass


class WeightedSampler:
    def __init__(self, rng: np.random.Generator = np.random):
        self.rng = rng

    def fit(self, weights: dict[str, float] | pd.Series):
        if len(weights) == 0:
            raise ValueError("Empty input")

        if isinstance(weights, pd.Series):
            self.return_type_ = "series"
            weights = dict(weights.value_counts())
        else:
            self.return_type_ = "list"

        weights_amounts = np.array(list(weights.values()))
        weights_amounts = weights_amounts / weights_amounts.sum()
        self.weights_ = weights_amounts
        self.keys_ = list(weights.keys())
        self.len_ = len(self.keys_)

        return self

    def sample(self, n_samples=1) -> list[str]:
        if self.len_ == 1:
            key = self.keys_[0]
            samples = [key for i in range(n_samples)]
            return self._construct_return_value(samples)

        indices = self.rng.choice(
            self.len_, size=n_samples, replace=True, p=self.weights_
        )
        samples = [self.keys_[i] for i in indices]
        return self._construct_return_value(samples)

    def _construct_return_value(self, raw_value: list):
        if self.return_type_ == "list":
            return raw_value

        return pd.Series(raw_value)
