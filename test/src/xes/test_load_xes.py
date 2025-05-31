import numpy as np
import pandas as pd
import unittest
import maxes.load_xes

class TestXes(unittest.TestCase):
    def test_loading(self):
        result = maxes.load_xes.load_raw_xes(
            filepath="data/Activities of daily living of several individuals_1_all/data/edited_hh102_labour.xes/edited_hh102_labour.xes"
        )

        self.assertEqual(len(result["traces"]), 18)
        self.assertEqual(len(result["traces"][0]["events"]), 82)
