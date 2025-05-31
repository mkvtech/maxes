import networkx as nx
import numpy as np

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvasQT
from matplotlib.figure import Figure

from maxes.utils import dset
from maxes.draw_xes_sequence_graph import draw_xes_sequence_graph

from maxes.app.application_context import ApplicationContext

layout_option_to_function_map = {
    "Circular": nx.circular_layout,
    "Kamada Kawai": nx.kamada_kawai_layout,
}


class SequenceGraphWidget(QWidget):
    def __init__(self, ctx: ApplicationContext):
        super().__init__()

        self.ctx = ctx

        layout = QHBoxLayout()
        self.setLayout(layout)

        l_layout = QVBoxLayout()
        layout.addLayout(l_layout)

        lt_layout = QHBoxLayout()
        l_layout.addLayout(lt_layout)

        figure = Figure()
        self.figure_canvas__sequence_graph = FigureCanvasQT(figure)
        l_layout.addWidget(self.figure_canvas__sequence_graph)

        toolbar = NavigationToolbar2QT(self.figure_canvas__sequence_graph)
        lt_layout.addWidget(toolbar)

        label = QLabel("Layout:")
        lt_layout.addWidget(label)

        self.combobox__graph_layout = QComboBox()
        self.combobox__graph_layout.addItems(list(layout_option_to_function_map.keys()))
        self.combobox__graph_layout.currentTextChanged.connect(
            self._on__combobox__graph_layout__current_text_changed
        )
        lt_layout.addWidget(self.combobox__graph_layout)

        r_layout = QVBoxLayout()
        r_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(r_layout)

        self.combobox__event_transition = QComboBox()
        self.combobox__event_transition.currentTextChanged.connect(
            self._on__combobox__event_transition__current_text_changed
        )
        r_layout.addWidget(self.combobox__event_transition)

        self.label__from_event = QLabel()
        self.label__from_event.setAlignment(Qt.AlignmentFlag.AlignTop)
        r_layout.addWidget(self.label__from_event)

        self.label__to_event = QLabel()
        self.label__to_event.setAlignment(Qt.AlignmentFlag.AlignTop)
        r_layout.addWidget(self.label__to_event)

        self.checkbox__highlight_transition = QCheckBox("Highlight")
        self.checkbox__highlight_transition.stateChanged.connect(
            self._on__checkbox__highlight_transition__state_changed
        )
        r_layout.addWidget(self.checkbox__highlight_transition)

        button__focus_on_transition = QPushButton("Focus on transition")
        button__focus_on_transition.released.connect(
            self._on__button__focus_on_transition__released
        )
        r_layout.addWidget(button__focus_on_transition)

        # Generation
        label = QLabel("<font size='+2'>Duration generation</font>")
        r_layout.addWidget(label)

        label = QLabel("Probability function")
        r_layout.addWidget(label)

        self.figure_canvas__transition_plot = FigureCanvasQT(Figure())

        toolbar = NavigationToolbar2QT(self.figure_canvas__transition_plot)
        r_layout.addWidget(toolbar)

        r_layout.addWidget(self.figure_canvas__transition_plot)

        label = QLabel("Bandwidth")
        r_layout.addWidget(label)

        r1_layout = QHBoxLayout()
        r_layout.addLayout(r1_layout)

        self.spin_box__kde_bandwidth = QDoubleSpinBox()
        self.spin_box__kde_bandwidth.setMaximum(2147483647.0)
        r1_layout.addWidget(self.spin_box__kde_bandwidth)

        button__kde_bandwidth_auto = QPushButton("Auto")
        button__kde_bandwidth_auto.released.connect(
            self._on__button__kde_bandwidth_auto__released
        )
        r1_layout.addWidget(button__kde_bandwidth_auto)

        # TODO: Kernel

        button__retrain_transition_model = QPushButton("Re-train model")
        button__retrain_transition_model.released.connect(
            self._on__button__retrain_transition_model__released
        )
        r_layout.addWidget(button__retrain_transition_model)

    def _plot_sequence_graph(self):
        if self.ctx.xes_generator is None:
            return

        selected_layout = self.combobox__graph_layout.currentText()
        pos_fn = layout_option_to_function_map[selected_layout]

        graph = self.ctx.xes_generator.sequence_graph_
        pos = pos_fn(graph)

        figure = self.figure_canvas__sequence_graph.figure
        figure.clear()

        ax = figure.subplots(1, 1)

        figure.subplots_adjust(0, 0, 1, 1, 0, 0)

        draw_xes_sequence_graph(graph, pos, ax, node_size=100)

        self.figure_canvas__sequence_graph.draw()

    def showEvent(self, event):
        self._plot_sequence_graph()
        self._update__combobox__event_transition__options()
        return super().showEvent(event)

    def _on__combobox__graph_layout__current_text_changed(self, text):
        self._plot_sequence_graph()

    def _update__combobox__event_transition__options(self):
        self.combobox__event_transition.clear()
        self.combobox__event_transition.setMinimumWidth(200)

        graph = self.ctx.xes_generator.sequence_graph_

        self._combobox__event_transition__options = {}

        for edge in graph.edges:
            self._combobox__event_transition__options[str(edge)] = edge
            self.combobox__event_transition.addItem(str(edge))

    def _on__combobox__event_transition__current_text_changed(self, text):
        if text is None or text == "":
            return

        edge = self._combobox__event_transition__options[text]
        self._update_event_transition_part(edge)

    def _on__checkbox__highlight_transition__state_changed(self):
        print("TODO")

    def _on__button__focus_on_transition__released(self):
        print("TODO")

    def _update_event_transition_part(self, edge):

        from_text = f"From: {str(edge[0])}"
        self.label__from_event.setText(from_text)

        to_text = f"To: {str(edge[0])}"
        self.label__to_event.setText(to_text)

        self._plot_transition_kde()

        kde = self.get_current_selected_transition_kde_model()

        self.spin_box__kde_bandwidth.setValue(kde.bandwidth_)

    def _plot_transition_kde(self):
        # Get selected model
        combobox_text = self.combobox__event_transition.currentText()
        edge = self._combobox__event_transition__options[combobox_text]
        graph = self.get_graph()
        edge_data = graph.edges[edge]
        kde = self.get_current_selected_transition_kde_model()

        # Interval
        transition_durations_seconds = [
            duration.seconds for duration in edge_data["transition_durations"]
        ]
        low = min(transition_durations_seconds)
        high = max(transition_durations_seconds)

        # Data
        resolution = 500
        x = np.linspace(low, high, resolution)
        y = np.exp(kde.score_samples(x[:, None]))

        # Plot
        figure = self.figure_canvas__transition_plot.figure
        figure.clear()

        ax = figure.subplots(1, 1)
        ax.fill_between(x, y)

        self.figure_canvas__transition_plot.draw()

    def get_graph(self):
        return self.ctx.xes_generator.sequence_graph_

    def get_current_selected_transition(self):
        combobox_text = self.combobox__event_transition.currentText()
        edge = self._combobox__event_transition__options[combobox_text]
        return edge

    def get_current_selected_transition_kde_model(self):
        edge = self.get_current_selected_transition()

        graph = self.get_graph()
        edge_data = graph.edges[edge]
        transition_generator = edge_data["duration_generator"]

        return transition_generator.kde_

    def _on__button__kde_bandwidth_auto__released(self):
        self.spin_box__kde_bandwidth.setValue(1)

    def _on__button__retrain_transition_model__released(self):
        edge = self.get_current_selected_transition()

        bandwidth = self.spin_box__kde_bandwidth.value()

        xes_generator = self.ctx.xes_generator
        dset(xes_generator.transition_models_kwargs, edge, "bandwidth", bandwidth)
        xes_generator.fit_transition_model(edge)

        self._plot_transition_kde()
