import sys
import networkx as nx
from PySide6.QtWidgets import *

from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvasQT
import matplotlib.backends.backend_qtagg

# from matplotlib.backends.backend_qt import NavigationToolbar2QT, FigureCanvasQT
from matplotlib.figure import Figure

graph = nx.DiGraph()
graph.add_edge("a", "b", frequency=10)
graph.add_edge("b", "c", frequency=10)
graph.add_edge("c", "a", frequency=10)
graph.add_edge("c", "c", frequency=10)

graph.nodes["a"]["first"] = 10
graph.nodes["c"]["last"] = 10

# pos = nx.kamada_kawai_layout(graph)
pos = nx.circular_layout(graph)


class MplCanvas(FigureCanvasQT):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.axes = fig.add_subplot(111)
        self.setParent(parent)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.figure.tight_layout(pad=0)
        sc.axes.margins(0)

        x = [p[0] for p in pos.values()]
        y = [p[1] for p in pos.values()]

        # sc.axes.set_xlim(min(x), max(x))
        # sc.axes.set_ylim(min(y), max(y))
        # sc.axes.axis("off")
        # sc.axes.margins(0)

        sc.figure.subplots_adjust(0, 0, 1, 1, 0, 0)

        # sc.figure.
        nx.draw(graph, pos, ax=sc.axes)

        toolbar = NavigationToolbar2QT(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
