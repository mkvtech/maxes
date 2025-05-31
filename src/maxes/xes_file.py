import pandas as pd

import maxes.xes_loader
from maxes.types import XesTraceRaw, XesFileRaw


class XesFile:
    def read(filepath):
        return XesFile(maxes.load_xes.load_raw_xes(filepath))

    def __init__(self, data: XesFileRaw):
        self.traces = [XesTrace(trace_raw) for trace_raw in data["traces"]]
        self.df = pd.concat([trace.df for trace in self.traces])


class XesTrace:
    def __init__(self, data: XesTraceRaw):
        self.data = data

        self.events_raw = data["events"]
        self.df = pd.DataFrame(data["events"])
        self.events = self.df

        self.attributes = data["attributes"]


class XesAttribute:
    def __init__(self, type: str, key: str, value: str):
        self.type = type
        self.key = key
        self.raw_value = value
        self.value = value
