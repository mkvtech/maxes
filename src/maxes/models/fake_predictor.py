import numpy as np


class FakePredictor:
    def __init__(self, value):
        self.value = value

    def fit(self, X, y):
        return self

    def predict(self, X):
        return np.repeat(True, X.shape[0])
