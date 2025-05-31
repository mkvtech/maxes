import unittest

from maxes.analyze_xes import AnalyzeXes

class TestAanlyzeXes(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        return super().setUp()

    def test_simple1(self):
        xes_file_path = "data/Activities of daily living of several individuals_1_all/data/activitylog_uci_detailed_labour.xes/activitylog_uci_detailed_labour.xes"
        result = AnalyzeXes.s_analyze(xes_file_path)

        self.assertCountEqual(
            result.keys(),
            ['File', 'XML', 'Log', 'Traces', 'Events', 'Analysis time']
        )

        # File
        self.assertCountEqual(
            result['File'].keys(),
            ["Path", "Size in bytes", "Size human-readable"]
        )

        # XML
        self.assertCountEqual(
            result["XML"].keys(),
            ["XES 2014", "XES 2023", "XES 2023 (Extended)", "Tags"]
        )

        # Log
        self.assertDictEqual(
            result["Log"],
            {
                "Extensions": {
                    "Count": 3,
                    "Each": [
                        {
                            "Name": "Concept",
                            "Prefix": "concept",
                            "uri": "http://www.xes-standard.org/concept.xesext"
                        },
                        {
                            "Name": "Lifecycle",
                            "Prefix": "lifecycle",
                            "uri": "http://www.xes-standard.org/lifecycle.xesext"
                        },
                        {
                            "Name": "Time",
                            "Prefix": "time",
                            "uri": "http://www.xes-standard.org/time.xesext"
                        }
                    ]
                }
            }
        )

        # Traces
        self.assertDictEqual(
            result["Traces"],
            { "Count": 25 }
        )

        # Events
        self.assertCountEqual(
            result["Events"].keys(),
            ["Count in log", "Count per trace", "Attributes"]
        )
        self.assertEqual(result["Events"]["Count in log"], 1392)
        self.assertEqual(result["Events"]["Count per trace"]["count"], 25)
        self.assertEqual(result["Events"]["Count per trace"]["min"], 34)
        self.assertEqual(result["Events"]["Count per trace"]["25%"], 46)
        self.assertEqual(result["Events"]["Count per trace"]["50%"], 58)
        self.assertEqual(result["Events"]["Count per trace"]["75%"], 62)
        self.assertEqual(result["Events"]["Count per trace"]["max"], 92)

        # Events / Attributes
        self.assertCountEqual(
            result["Events"]["Attributes"].keys(),
            ["Unique count", "Each"]
        )
        self.assertEqual(result["Events"]["Attributes"]["Unique count"], 11)
