import numpy as np
import pandas as pd
import unittest
import xes


class TestXes(unittest.TestCase):

    def test_debugger(self):
        a = 1
        b = 2
        self.assertEqual(a + b, 3)

    def test_find_closest_event_by_time(self):
        df = pd.DataFrame(
            columns=["concept:name", "time:timestamp", "lifecycle:transition"],
            data=[
                ["sleep", "2024-01-01T00:00:30.000", "start"],
                ["sleep", "2024-01-01T00:10:00.000", "complete"],
                ["eat", "2024-01-01T00:10:20.000", "start"],
                ["eat", "2024-01-01T00:10:30.000", "complete"],
                ["sleep", "2024-01-01T00:23:00.000", "start"],
                ["sleep", "2024-01-02T00:07:30.000", "complete"],
            ]
        )

        df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])

        sample_sleep_event = pd.Series({
            "concept:name": "sleep",
            "time:timestamp": np.datetime64("2024-01-01T00:08:30.000"),
            "lifecycle:transition": "start"
        })

        closest_event = xes.find_closest_event_by_time(
            df,
            sample_sleep_event,
            filter_columns=["concept:name", "lifecycle:transition"],
            distance_column="time:timestamp"
        )
        pd.testing.assert_series_equal(closest_event, df.iloc[0])

    def test_event_stream_distance1(self):
        df1 = pd.DataFrame(
            columns=["a", "b", "c", "d", "e"],
            data=[
                ["sleep", "2024-10-17T23:13:42", 0.1, 4, 0.079],
                ["sleep", "2024-09-21T11:55:35", 0.1, 5, 0.528],
                ["eat", "2024-04-02T04:23:16", 0.1, 0, 0.288],
                ["sleep", "2024-09-25T16:25:53", 0.1, 9, 0.158],
                ["sleep", "2024-06-15T16:28:39", 0.1, 0, 0.848],
                ["eat", "2024-11-16T08:08:29", 0.1, 8, 0.328],
                ["sleep", "2024-02-03T06:51:46", 0.1, 2, 0.974],
                ["sleep", "2024-01-03T09:52:04", 0.1, 6, 0.445],
                ["sleep", "2024-05-16T17:48:30", 0.1, 8, 0.778],
                ["sleep", "2024-08-21T04:51:05", 0.1, 1, 0.875],
                ["sleep", "2024-08-02T08:34:29", 0.1, 1, 0.620],
                ["eat", "2024-01-03T14:34:51", 0.1, 1, 0.016],
                ["sleep", "2024-06-02T01:15:05", 0.1, 7, 0.893],
            ]
        )
        df1["b"] = pd.to_datetime(df1["b"])

        df2 = pd.DataFrame(
            columns=["a", "b", "c", "d", "e"],
            data=[
                ["sleep", "2024-04-30T13:54:49", 0.1, 5, 0.781],
                ["sleep", "2024-06-28T04:18:35", 0.1, 6, 0.453],
                ["eat", "2024-07-30T00:38:06", 0.1, 2, 0.198],
                ["sleep", "2024-08-21T10:22:45", 0.1, 10, 0.970],
                ["sleep", "2024-10-16T13:08:55", 0.1, 1, 0.152],
                ["sleep", "2024-12-16T14:37:50", 0.1, 8, 0.326],
                ["eat", "2024-11-19T01:57:57", 0.1, 3, 0.594],
            ]
        )
        df2["b"] = pd.to_datetime(df2["b"])

        found_events_ratio, avg_deltas = xes.event_stream_distance1(
            df1, df2,
            closest_event_filter_columns=["a"],
            closest_event_search_column="b",
            distance_columns=["b", "c", "d", "e"]
        )

        self.assertEqual(found_events_ratio, 1.0)

        expected_avg_deltas = pd.Series({
            "b": pd.to_timedelta("28 days 20:34:51.857142857"),
            "c": 0.0,
            "d": 5.142857,
            "e": 0.172714,
        })

        pd.testing.assert_series_equal(avg_deltas, expected_avg_deltas)
