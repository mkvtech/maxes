import unittest

from maxes.generators.xes_generator.xes_generator1 import XesGenerator1
from maxes.xes_loader2 import XesLoader

class TestXesGenerator1(unittest.TestCase):
    def test_generate_sequence(self):
        xes_file_path = "data/Activities of daily living of several individuals_1_all/data/activitylog_uci_detailed_labour.xes/activitylog_uci_detailed_labour.xes"
        log = XesLoader().load(xes_file_path)

        xes_generator = XesGenerator1()
        xes_generator.fit(log)

        generated_xes_log = xes_generator.sample(n_samples=1)[0]

        generated_traces_count = len(generated_xes_log.traces)
        self.assertEqual(generated_traces_count, 25)
