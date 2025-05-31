import numpy as np
import pandas as pd
import unittest

from maxes.analyze_sequence import analyze_sequence

class TestAnalyzeSequence(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def assertGraph(self, graph, expected):
        edges = {edge: graph.edges[edge] for edge in graph.edges}
        self.assertDictEqual(edges, expected)

    def test_df1_analyze_sequence(self):
        df = TestAnalyzeSequence._events_df1()
        seq = analyze_sequence(df)

        self.assertGraph(seq, {
            (("A", "start"),    ("A", "complete")): {"frequency": 1},
            (("A", "complete"), ("B", "start")):    {"frequency": 1},
            (("B", "start"),    ("B", "complete")): {"frequency": 1},
            (("B", "complete"), ("C", "start")):    {"frequency": 1},
            (("C", "start"),    ("C", "complete")): {"frequency": 1},
        })
        self.assertTrue(seq.nodes[("A", "start")]["first"])
        self.assertTrue(seq.nodes[("C", "complete")]["last"])

    def test_df1_with_single_sequence_key(self):
        df = TestAnalyzeSequence._events_df1()
        seq = analyze_sequence(df, sequence_keys=["concept:name"])

        self.assertGraph(seq, {
            (("A",), ("A",)): {"frequency": 1},
            (("A",), ("B",)): {"frequency": 1},
            (("B",), ("B",)): {"frequency": 1},
            (("B",), ("C",)): {"frequency": 1},
            (("C",), ("C",)): {"frequency": 1},
        })
        self.assertTrue(seq.nodes[("A",)]["first"])
        self.assertTrue(seq.nodes[("C",)]["last"])

    def test_df1_with_only_start_events(self):
        df = TestAnalyzeSequence._events_df1()
        df = df[df["lifecycle:transition"] == "start"]

        seq = analyze_sequence(df, sequence_keys=["concept:name"])

        self.assertGraph(seq, {
            (("A",), ("B",)): {"frequency": 1},
            (("B",), ("C",)): {"frequency": 1},
        })
        self.assertTrue(seq.nodes[("A",)]["first"])
        self.assertTrue(seq.nodes[("C",)]["last"])

    def test_df2_with_only_start_events(self):
        df = TestAnalyzeSequence._events_df2()
        df = df[df["lifecycle:transition"] == "start"]

        seq = analyze_sequence(df, sequence_keys=["concept:name"])

        self.assertGraph(seq, {
            (("A",), ("B",)): {"frequency": 1},
            (("B",), ("C",)): {"frequency": 2},
            (("B",), ("D",)): {"frequency": 1},
            (("B",), ("H",)): {"frequency": 5},
            (("C",), ("B",)): {"frequency": 3},
            (("C",), ("E",)): {"frequency": 1},
            (("C",), ("J",)): {"frequency": 1},
            (("D",), ("C",)): {"frequency": 1},
            (("E",), ("F",)): {"frequency": 1},
            (("F",), ("G",)): {"frequency": 1},
            (("G",), ("B",)): {"frequency": 1},
            (("H",), ("B",)): {"frequency": 2},
            (("H",), ("I",)): {"frequency": 2},
            (("H",), ("J",)): {"frequency": 1},
            (("I",), ("B",)): {"frequency": 1},
            (("I",), ("C",)): {"frequency": 1},
            (("I",), ("L",)): {"frequency": 1},
            (("J",), ("I",)): {"frequency": 1},
            (("J",), ("K",)): {"frequency": 1},
            (("K",), ("C",)): {"frequency": 1},
        })
        self.assertTrue(seq.nodes[("A",)]["first"])
        self.assertTrue(seq.nodes[("L",)]["last"])

    def test_df3_last_event(self):
        df = TestAnalyzeSequence._events_df3()
        seq = analyze_sequence(df)

        self.assertGraph(seq, {
            (("A", "start"),    ("A", "complete")): {"frequency": 2},
            (("A", "complete"), ("B", "start")):    {"frequency": 2},
            (("B", "start"),    ("B", "complete")): {"frequency": 3},
            (("B", "complete"), ("A", "start")):    {"frequency": 1},
            (("B", "complete"), ("C", "start")):    {"frequency": 2},
            (("C", "start"),    ("C", "complete")): {"frequency": 2},
            (("C", "complete"), ("B", "start")):    {"frequency": 1},
        })
        self.assertTrue(seq.nodes[("A", "start")]["first"])
        self.assertTrue(seq.nodes[("C", "complete")]["last"])


    def _events_df1():
        return pd.DataFrame(
            [["A", "start"],
             ["A", "complete"],
             ["B", "start"],
             ["B", "complete"],
             ["C", "start"],
             ["C", "complete"]],
            columns=["concept:name", "lifecycle:transition"]
        )

    def _events_df2():
        return pd.DataFrame(
            [
                ["A", "start"],    ["A", "complete"], ["B", "start"],    ["B", "complete"], ["C", "start"],
                ["B", "start"],    ["C", "complete"], ["B", "complete"], ["D", "start"],    ["D", "complete"],
                ["C", "start"],    ["C", "complete"], ["E", "start"],    ["E", "complete"], ["F", "start"],
                ["F", "complete"], ["G", "start"],    ["G", "complete"], ["B", "start"],    ["B", "complete"],
                ["H", "start"],    ["H", "complete"], ["B", "start"],    ["B", "complete"], ["H", "start"],
                ["H", "complete"], ["I", "start"],    ["I", "complete"], ["B", "start"],    ["B", "complete"],
                ["H", "start"],    ["H", "complete"], ["J", "start"],    ["J", "complete"], ["I", "start"],
                ["I", "complete"], ["C", "start"],    ["B", "start"],    ["B", "complete"], ["C", "start"],
                ["C", "complete"], ["C", "complete"], ["J", "start"],    ["J", "complete"], ["K", "start"],
                ["K", "complete"], ["C", "start"],    ["C", "complete"], ["B", "start"],    ["B", "complete"],
                ["H", "start"],    ["H", "complete"], ["B", "start"],    ["B", "complete"], ["H", "start"],
                ["H", "complete"], ["I", "start"],    ["I", "complete"], ["L", "start"],    ["L", "complete"],
            ],
            columns=["concept:name", "lifecycle:transition"]
        )

    def _events_df3():
        return pd.DataFrame(
            [["A", "start"],
             ["A", "complete"],
             ["B", "start"],
             ["B", "complete"],
             ["C", "start"],
             ["C", "complete"],
             ["B", "start"],
             ["B", "complete"],
             ["A", "start"],
             ["A", "complete"],
             ["B", "start"],
             ["B", "complete"],
             ["C", "start"],
             ["C", "complete"]],
            columns=["concept:name", "lifecycle:transition"]
        )
