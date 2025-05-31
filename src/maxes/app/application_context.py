import PySide6.QtCore

from maxes.xes_log import XesLog
from maxes.xes_loader2 import XesLoader
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3 as XesGenerator


class ApplicationEvents(PySide6.QtCore.QObject):
    startup = PySide6.QtCore.Signal()
    xes_log_loaded = PySide6.QtCore.Signal()
    sequence_graph_computed = PySide6.QtCore.Signal()
    xes_log_generated = PySide6.QtCore.Signal()


class ApplicationContext:
    xes_log: XesLog
    xes_loader: XesLoader
    xes_generator: XesGenerator
    generated_xes_log: XesLog

    thread_pool: PySide6.QtCore.QThreadPool

    events = ApplicationEvents()
