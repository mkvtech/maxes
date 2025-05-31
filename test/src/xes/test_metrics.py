import numpy as np
import unittest

from maxes.metrics.general import incorrect_transitions_ratio, dot_product

class TestMetrics(unittest.TestCase):
    def test_incorrect_transitions_ratio(self):
        original_sequence = {
            ("A", "B"): 3,
            ("A", "C"): 1
        }
        generated_sequence = {
            ("A", "B"): 3,
            ("B", "C"): 1,
        }

        np.testing.assert_allclose(incorrect_transitions_ratio(original_sequence, generated_sequence), 0.25)
        np.testing.assert_allclose(incorrect_transitions_ratio(original_sequence, generated_sequence, use_counts=False), 0.5)

    def test_dot_product2(self):
        original = {
            ("A", "B"): 1,
        }
        generated = {
            ("A", "C"): 1,
        }

        np.testing.assert_allclose(dot_product(original, generated), 0)

    def test_dot_product3(self):
        original = {
            ("A", "B"): 1,
            ("A", "C"): 0
        }
        generated = {
            ("A", "B"): 1,
            ("A", "C"): 0,
        }

        np.testing.assert_allclose(dot_product(original, generated), 1)

    def test_dot_product4(self):
        original = {
            ("A", "B"): 3,
            ("A", "C"): 1
        }
        generated = {
            ("A", "B"): 3,
            ("B", "C"): 1,
        }
        np.testing.assert_allclose(dot_product(original, generated), 0.9)
