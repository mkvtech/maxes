import xml.etree.ElementTree as ET

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from maxes.app.application_context import ApplicationContext
from maxes.app.widgets.xes_table_widget import XesTableWidget

from maxes.app.background_tasks import (
    ApplicationProcess,
    prepare_nlogger,
)

from maxes.logging import NestedLogger
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3 as XesGenerator
from maxes.xes_log import XesLog
from maxes.serialization.serialize import Serializer


class GenerateXesTab(QWidget):
    def __init__(self, ctx: ApplicationContext):
        super().__init__()

        self.ctx = ctx

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # Options
        label = QLabel("Options")
        layout.addWidget(label)

        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)

        label = QLabel("Traces: ")
        layout_1.addWidget(label)

        self.spin_box__n_of_traces = QSpinBox()
        self.spin_box__n_of_traces.setMaximum(2147483647)
        self.spin_box__n_of_traces.setValue(1)
        layout_1.addWidget(self.spin_box__n_of_traces)

        layout_2 = QHBoxLayout()
        layout.addLayout(layout_2)

        label = QLabel("Save path:")
        layout_2.addWidget(label)

        self.line_edit__save_path = QLineEdit()
        layout_2.addWidget(self.line_edit__save_path)

        self.button__browse_save_path = QPushButton("Browse...")
        self.button__browse_save_path.released.connect(
            self._on__button__browse_save_path__released
        )
        layout_2.addWidget(self.button__browse_save_path)

        layout_3 = QHBoxLayout()
        layout.addLayout(layout_3)

        self.button__clear = QPushButton("Clear")
        self.button__clear.setEnabled(False)
        self.button__clear.released.connect(self._on__button__clear__released)
        layout_3.addWidget(self.button__clear)

        self.button__generate = QPushButton("Generate")
        self.button__generate.released.connect(self._on__button__generate__released)
        layout_3.addWidget(self.button__generate)

        self.button__save = QPushButton("Save")
        self.button__save.setEnabled(False)
        self.button__save.released.connect(self._on__button__save__released)
        layout_3.addWidget(self.button__save)

        # checkbox save when generation done
        # self.checkbox__save_when_generated = QCheckBox("Save when generation is done")

        # File input
        # Browse button
        # Save button

        # preview
        self.xes_table_widget = XesTableWidget()
        layout.addWidget(self.xes_table_widget)

    def _on__button__generate__released(self):
        xes_generator = self.ctx.xes_generator
        n_of_traces = max(0, self.spin_box__n_of_traces.value())
        xes_generator.generate_traces_count = n_of_traces

        self.process = ApplicationProcess(
            parent=self,
            fn=_generate_xes,
            fn_kwargs={"xes_generator": xes_generator},
            title="Genearting XES log",
            thread_pool=self.ctx.thread_pool,
        )
        self.process.prepare()
        self.process.worker.signals.result.connect(self._on_generate_complete)

        self.process.exec()

    def _on_generate_complete(self, result):
        self.ctx.generated_xes_log = result["generated_log"]
        self.xes_table_widget.set_df(self.ctx.generated_xes_log.df)
        self.xes_table_widget.table_view.resizeColumnsToContents()
        self.button__clear.setEnabled(True)
        self.button__save.setEnabled(True)

    def _on__button__browse_save_path__released(self):
        self.dialog = QFileDialog(self)
        self.dialog.finished.connect(self._on_file_dialog_finished)
        self.dialog.open()

    def _on_file_dialog_finished(self):
        selected_path = self.dialog.selectedFiles()[0]
        self.line_edit__save_path.setText(selected_path)

    def _on__button__clear__released(self):
        self.ctx.generated_xes_log = None
        self.xes_table_widget.set_df(None)
        self.button__clear.setEnabled(False)
        self.button__save.setEnabled(False)

    def _on__button__save__released(self):
        path = self.line_edit__save_path.text()
        generated_xes_log = self.ctx.generated_xes_log

        self.process = ApplicationProcess(
            parent=self,
            fn=_save_path,
            fn_kwargs={"xes_log": generated_xes_log, "path": path},
            title="Saving generated XES log",
            thread_pool=self.ctx.thread_pool,
        )
        self.process.prepare()
        self.process.exec()


def _generate_xes(xes_generator: XesGenerator, progress_callback, log_callback):
    nlogger = prepare_nlogger(log_callback=log_callback)

    xes_generator.nlogger = nlogger

    with nlogger.action_logging("Generating XES"):
        generated_log = xes_generator.generate()

    xes_generator.nlogger = NestedLogger.default()

    progress_callback.emit(1)

    return {
        "generated_log": generated_log,
    }


def _save_path(xes_log: XesLog, path: str, progress_callback, log_callback):
    nlogger = prepare_nlogger(log_callback=log_callback)

    with nlogger.action_logging("Serializing"):
        xes_serializer = Serializer()
        xes_log_ET = xes_serializer.serialize(xes_log)

    with nlogger.action_logging("Formatting XML"):
        ET.indent(xes_log_ET)
        ET.register_namespace("", "http://www.xes-standard.org")

    with nlogger.action_logging("Writing XML to file"):
        with open(path, "w") as file:
            xes_log_ET.write(file, encoding="unicode")

    progress_callback.emit(1)
