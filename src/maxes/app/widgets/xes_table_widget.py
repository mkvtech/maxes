import pandas as pd

from PySide6.QtCore import *
from PySide6.QtWidgets import *


class DataFrameTableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame = pd.DataFrame()):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return str(self._data.columns[section])

        if orientation == Qt.Orientation.Vertical:
            return str(self._data.index[section])


class XesTableWidget(QWidget):
    def __init__(
        self,
        df: pd.DataFrame | None = None,
        trace_identifier_column: str = "case:concept:name",
    ):
        super().__init__()

        self.table_model = DataFrameTableModel()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)

        self.checkbox__all_traces = QCheckBox("All traces")
        self.checkbox__all_traces.setCheckState(Qt.CheckState.Checked)
        self.checkbox__all_traces.stateChanged.connect(
            self.checkbox__all_traces__state_changed
        )
        layout_1.addWidget(self.checkbox__all_traces)

        label = QLabel("Trace: ")
        layout_1.addWidget(label)

        self.combobox__trace = QComboBox()
        self.combobox__trace.currentTextChanged.connect(
            self.combobox__trace__current_text_changed
        )
        layout_1.addWidget(self.combobox__trace)

        self.combobox__trace__options = {}

        self.trace_identifier_column = trace_identifier_column

        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        layout.addWidget(self.table_view)

        self.set_df(df)

    def set_df(self, df: pd.DataFrame | None):
        if df is None:
            df = pd.DataFrame()

        self.df = df

        if self.trace_identifier_column in df:
            self.combobox__trace__options = {
                str(case_concept_name): case_concept_name
                for case_concept_name in df[self.trace_identifier_column]
            }
        else:
            self.combobox__trace__options = {}

        self.table_model.beginResetModel()
        self.table_model._data = df
        self.table_model.endResetModel()

        self.combobox__trace.clear()
        for case_concept_name_str in self.combobox__trace__options.keys():
            self.combobox__trace.addItem(case_concept_name_str)

    def checkbox__all_traces__state_changed(self, state):
        if self.checkbox__all_traces.checkState() == Qt.CheckState.Checked:
            self.table_model.beginResetModel()
            self.table_model._data = self.df
            self.table_model.endResetModel()
        else:
            self._set_df_to_currently_selected_trace()

    def combobox__trace__current_text_changed(self, text):
        if self.table_model is None:
            return

        if self.checkbox__all_traces.checkState() == Qt.CheckState.Checked:
            return

        self._set_df_to_currently_selected_trace()

    def _set_df_to_currently_selected_trace(self):
        if len(self.combobox__trace__options) == 0:
            return

        self.table_model.beginResetModel()

        case_concept_name_str = self.combobox__trace.currentText()
        case_concept_name = self.combobox__trace__options[case_concept_name_str]
        df_trace = self.df[self.df[self.trace_identifier_column] == case_concept_name]
        self.table_model._data = df_trace

        self.table_model.endResetModel()
