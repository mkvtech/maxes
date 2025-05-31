import unittest
import numpy as np

from maxes.models.simple_categorical_feature_picker import SimpleCategoricalFeaturePicker

class TestSimpleCategoricalFeaturePicker(unittest.TestCase):
    def test_with_python_list(self):
        model = SimpleCategoricalFeaturePicker()
        X = [
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["green"], ["green"], ["green"], ["green"], ["blue"],
        ]
        model.fit(X)

        samples = model.sample(n_samples=5)

        for sample in samples:
            self.assertIn(sample, ["red", "green", "blue"])

    def test_with_numpy_array(self):
        model = SimpleCategoricalFeaturePicker()
        X = np.array([
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["red"], ["red"], ["red"], ["red"], ["red"],
            ["green"], ["green"], ["green"], ["green"], ["blue"],
        ])
        model.fit(X)

        samples = model.sample(n_samples=5)

        for sample in samples:
            self.assertIn(sample, ["red", "green", "blue"])
