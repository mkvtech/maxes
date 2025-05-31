import sys
import traceback
import time
import logging

from maxes.logging import NestedLogger

from PySide6.QtCore import QObject, QRunnable, Signal, Slot, QThreadPool
from PySide6.QtWidgets import *


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(float)
    log = Signal(str)


class Worker(QRunnable):
    def __init__(self, fn, fn_args=[], fn_kwargs={}):
        super().__init__()
        self.fn = fn
        self.fn_args = fn_args
        self.fn_kwargs = fn_kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.fn_kwargs["progress_callback"] = self.signals.progress
            self.fn_kwargs["log_callback"] = self.signals.log
            result = self.fn(*self.fn_args, **self.fn_kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


def example_long_task(seconds: int, nlogger: NestedLogger, progress_callback):
    with nlogger.action_logging("Running task"):
        for i in range(seconds * 10):
            time.sleep(0.1)
            progress = i / (seconds * 10)
            progress_callback.emit(progress)
            nlogger.logger.info(progress)

    nlogger.logger.info("Complete")

    return "Done"


class PassThroughLoggingHandler(logging.Handler):
    def __init__(self, on_emit):
        logging.Handler.__init__(self=self)
        self.on_emit = on_emit

    def emit(self, record):
        msg = self.format(record)
        self.on_emit(msg)


def example_long_task_with_logger(
    seconds: int, progress_callback: Signal, log_callback: Signal
):
    log_callback.emit("initializing")

    def on_emit(msg: str):
        log_callback.emit(msg)

    logging_handler = PassThroughLoggingHandler(on_emit)

    logger = logging.Logger("loadingxesfile")
    logger.addHandler(logging_handler)

    nlogger = NestedLogger(logger)

    with nlogger.action_logging("Running task"):
        for i in range(seconds * 10):
            time.sleep(0.1)
            progress = i / (seconds * 10)
            progress_callback.emit(progress)

    logger.info("Complete")

    return "Done"


def prepare_nlogger(log_callback):
    def on_emit(msg: str):
        print(msg)
        log_callback.emit(msg)

    logging_handler = PassThroughLoggingHandler(on_emit)

    logger = logging.Logger("temp")
    logger.addHandler(logging_handler)

    nlogger = NestedLogger(logger)

    return nlogger


class PassThroughLoggingHandler(logging.Handler):
    def __init__(self, on_emit):
        logging.Handler.__init__(self=self)
        self.on_emit = on_emit

    def emit(self, record):
        msg = self.format(record)
        self.on_emit(msg)


class ApplicationProgressDialog(QDialog):
    def __init__(self, parent=None, show_progress: bool = True, show_log: bool = True):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        if show_progress:
            self.progress_bar = QProgressBar(self)
            layout.addWidget(self.progress_bar)

        if show_log:
            self.text = QPlainTextEdit("")
            self.text.setReadOnly(True)
            layout.addWidget(self.text)

        button_flags = QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(button_flags)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.resize(640, 480)

    def set01(self, value: float):
        value = round(value * self.progress_bar.maximum())
        self.progress_bar.setValue(value)

    def add_text_line(self, text: str):
        self.text.appendPlainText(text)


class ApplicationProcess(QObject):
    def __init__(
        self, parent: QWidget, fn, fn_kwargs, title: str, thread_pool: QThreadPool
    ):
        super().__init__()
        self.parent = parent
        self.title = title
        self.thread_pool = thread_pool
        self.fn = fn
        self.fn_kwargs = fn_kwargs

    def prepare(self):
        self.progress_dialog = ApplicationProgressDialog(self.parent)
        self.progress_dialog.setWindowTitle(self.title)

        self.worker = Worker(self.fn, fn_kwargs=self.fn_kwargs)
        self.worker.signals.progress.connect(self._on_progress)
        self.worker.signals.log.connect(self._on_log)
        self.worker.signals.finished.connect(self._on_complete)

    def exec(self):
        self.progress_dialog.show()
        self.thread_pool.start(self.worker)
        self.progress_dialog.exec()

    def _on_progress(self, progress: float):
        self.progress_dialog.set01(progress)

    def _on_log(self, message: str):
        self.progress_dialog.text.appendPlainText(message)

    def _on_complete(self):
        self.progress_dialog.close()
        self.progress_dialog = None
