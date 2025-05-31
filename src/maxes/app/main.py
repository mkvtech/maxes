import sys
import logging
import threading
from time import sleep

from PySide6.QtCore import QSize, Qt, Signal, Slot, QThreadPool
from PySide6.QtGui import QAction

from PySide6.QtWidgets import *

from maxes.logging import NestedLogger

from maxes.app.background_tasks import (
    ApplicationProcess,
    prepare_nlogger,
)
from maxes.app.application_context import ApplicationContext
from maxes.app.widgets.sequence_graph_widget import SequenceGraphWidget
from maxes.app.widgets.xes_table_widget import XesTableWidget
from maxes.app.widgets.generate_xes_tab import GenerateXesTab
from maxes.app.widgets.attributes_tab import AttributesTab

from maxes.xes_loader2 import XesLoader
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3 as XesGenerator

import argparse


def _load_file(path: str, progress_callback, log_callback):
    nlogger = prepare_nlogger(log_callback=log_callback)

    steps = 2

    nlogger.logger.info(f"Thread ID: {threading.get_ident()}")

    with nlogger.action_logging("Loading XES"):
        xes_loader = XesLoader(nlogger=nlogger)
        xes_log = xes_loader.load(path)

    progress_callback.emit(1 / steps)

    with nlogger.action_logging("Analyzing XES"):
        xes_generator = XesGenerator(nlogger=nlogger)
        xes_generator.fit(xes_log)

    xes_generator.nlogger = NestedLogger.default()

    progress_callback.emit(1)

    return {
        "xes_log": xes_log,
        "xes_loader": xes_loader,
        "xes_generator": xes_generator,
    }


class InputXesWidget(QWidget):
    def __init__(self, ctx: ApplicationContext):
        super().__init__()

        self.ctx = ctx

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # Upper part
        upper_layout = QVBoxLayout()
        layout.addLayout(upper_layout)

        line_layout = QHBoxLayout()
        upper_layout.addLayout(line_layout)

        self._line_edit_file_path = QLineEdit()
        self._line_edit_file_path.setStatusTip("Path to an XES file.")
        # Fast debug
        # self._line_edit_file_path.setText(
        #     "/vt/md/maxes/maxes/data/other/simple.xes"
        # )
        line_layout.addWidget(self._line_edit_file_path)

        button_browse = QPushButton("Browse")
        button_browse.released.connect(self._open_file_dialog)
        line_layout.addWidget(button_browse)

        checkbox_compute_sequence_graph = QCheckBox("Compute sequence graph")
        checkbox_compute_sequence_graph.setStatusTip(
            "Whether to compute sequence graph after loading the XES file."
        )
        upper_layout.addWidget(checkbox_compute_sequence_graph)

        layout_submit_row = QHBoxLayout()
        layout_submit_row.setAlignment(Qt.AlignmentFlag.AlignRight)
        upper_layout.addLayout(layout_submit_row)

        button_submit = QPushButton("Read")
        button_submit.released.connect(self._on_submit)
        layout_submit_row.addWidget(button_submit)

        # Lower part
        self.xes_table_widget = XesTableWidget()
        layout.addWidget(self.xes_table_widget)

        # divider

        # preview
        # select trace to preview
        # n of events
        # n of attributes
        # xes table

    def _open_file_dialog(self):
        self.dialog = QFileDialog(self)
        self.dialog.finished.connect(self._on_file_dialog_finished)
        self.dialog.open()

    def _on_file_dialog_finished(self):
        selected_path = self.dialog.selectedFiles()[0]
        self._line_edit_file_path.setText(selected_path)

    def _on_submit(self):
        file_path = self._line_edit_file_path.text()
        self.start_loading_file(file_path)

    def start_loading_file(self, file_path: str):
        self._line_edit_file_path.setText = file_path

        print(f"{threading.get_ident()=}")
        self.process = ApplicationProcess(
            parent=self,
            fn=_load_file,
            fn_kwargs={"path": file_path},
            title="Loading XES file",
            thread_pool=self.ctx.thread_pool,
        )
        self.process.prepare()
        self.process.worker.signals.result.connect(self._on_load_complete)

        self.process.exec()

    def _on_load_complete(self, result):
        self.ctx.xes_loader = result["xes_loader"]
        self.ctx.xes_log = result["xes_log"]
        self.ctx.xes_loader = result["xes_loader"]
        self.ctx.xes_generator = result["xes_generator"]

        self.xes_table_widget.set_df(self.ctx.xes_log.df)
        self.xes_table_widget.table_view.resizeColumnsToContents()

        self.ctx.events.xes_log_loaded.emit()


class PreviewXesWidget(QWidget):
    def __init__(self):
        super().__init__()


class MainWindow(QMainWindow):
    def __init__(self, input_file_path: str | None = None):
        super().__init__()

        self.init_options = {"input_file_path": input_file_path}

        self.setWindowTitle("XES Generator")
        self.resize(1000, 600)

        self.ctx = ApplicationContext()
        self.ctx.thread_pool = QThreadPool()

        print(f"{self.ctx.thread_pool.maxThreadCount()=}")
        print(f"{threading.get_ident()=}")

        # Subscribe to events
        self.ctx.events.xes_log_loaded.connect(self._on_xes_log_loaded)
        self.ctx.events.startup.connect(self._on_startup)

        # Other
        self.setStatusBar(QStatusBar(self))

        # Actions
        action_settings = QAction("Settings", self)
        action_exit = QAction("Exit", self)

        action_new_project = QAction("New project", self)
        action_save = QAction("Save", self)
        action_save_as = QAction("Save as...", self)

        action_about = QAction("About", self)

        # Main menu
        menu = self.menuBar()

        app_menu = menu.addMenu("XesGen")
        app_menu.addAction(action_settings)
        app_menu.addAction(action_exit)

        file_menu = menu.addMenu("File")
        file_menu.addAction(action_new_project)
        file_menu.addAction(action_save)
        file_menu.addAction(action_save_as)

        help_menu = menu.addMenu("Help")
        help_menu.addAction(action_about)

        # Main content
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.input_xes_tab_widget = InputXesWidget(ctx=self.ctx)
        self.tabs.addTab(self.input_xes_tab_widget, "Input")

        self.tabs.addTab(SequenceGraphWidget(ctx=self.ctx), "Sequence graph")
        self.tabs.addTab(AttributesTab(ctx=self.ctx), "Attributes")
        self.tabs.addTab(GenerateXesTab(ctx=self.ctx), "Generate")

        self.tabs.setTabEnabled(1, False)

        # self.read

        self.setCentralWidget(self.tabs)

    def _on_xes_log_loaded(self):
        self.tabs.setTabEnabled(1, True)

    def showEvent(self, event):
        print("show")
        # return super().showEvent(event)

    @Slot()
    def _on_startup(self):
        print("STARTUP")

        print(self.init_options)

        if self.init_options.get("input_file_path") is not None:
            file_path = self.init_options["input_file_path"]
            self.input_xes_tab_widget.start_loading_file(file_path)


arg_parser = argparse.ArgumentParser(
    prog="XesGen",
    description="XES File Generator",
)

arg_parser.add_argument("-i", "--input")

args = arg_parser.parse_args()


app = QApplication(sys.argv)

window = MainWindow(input_file_path=args.input)
window.setWindowState(Qt.WindowState.WindowMaximized)
window.show()

window.ctx.events.startup.emit()
print("EXEC")
app.exec()

print("after exec")
