import sys

import pandas as pd

from PySide6.QtWidgets import *

from maxes.app.widgets.xes_table_widget import XesTableWidget

data = [
    ["1", "a", "start"],
    ["1", "a", "complete"],
    ["1", "b", "start"],
    ["1", "b", "complete"],
    ["2", "a", "start"],
    ["2", "a", "complete"],
    ["2", "c", "start"],
    ["2", "c", "complete"],
    ["3", "a", "start"],
    ["3", "a", "complete"],
]
df = pd.DataFrame(
    data, columns=["case:concept:name", "concept:name", "lifecycle:transition"]
)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()

        self.xes_table = XesTableWidget(df)
        # self.xes_table = XesTableWidget(pd.DataFrame())
        layout.addWidget(self.xes_table)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
w.resize(1000, 600)
app.exec()
