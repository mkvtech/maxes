import unittest


from maxes.xes_loader2 import XesLoader


class TestXesLoader2(unittest.TestCase):

    def test_load(self):

        result = XesLoader().load(
            file_path="data/Activities of daily living of several individuals_1_all/data/edited_hh102_labour.xes/edited_hh102_labour.xes"
        )

        self.assertEqual(len(result.traces), 18)
        self.assertEqual(len(result.traces[0].events), 82)
