from PySide6.QtCore import *
from PySide6.QtWidgets import *


def add_label(label_text: str, widget: QWidget):
    layout = QHBoxLayout()

    label = QLabel(label_text)
    layout.addWidget(label)

    layout.addWidget(widget)

    return layout, label


class KNeighborsClassifierOptionsWidget(QWidget):
    """
    params: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    """

    def __init__(self, initial_data: dict = {}):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # n_neighbors
        self.spin_box__n_neighbors = QSpinBox()
        self.spin_box__n_neighbors.setMaximum(2147483647)
        sub_layout, label = add_label("n_neighbors", self.spin_box__n_neighbors)
        layout.addLayout(sub_layout)

        # weights
        self.combobox__weights = QComboBox()
        self.combobox__weights.addItem("uniform")
        self.combobox__weights.addItem("distance")
        sub_layout, label = add_label("weights", self.combobox__weights)
        layout.addLayout(sub_layout)

        self.set_params(initial_data)

    def get_params(self):
        return {
            "n_neighbors": self.spin_box__n_neighbors.value(),
            "weights": self.combobox__weights.currentText(),
        }

    def set_params(self, params: dict):
        self.spin_box__n_neighbors.setValue(params.get("n_neighbors", 5))
        self.combobox__weights.setCurrentText(params.get("weights", "uniform"))


class CategoricalNBOptionsWidget(QWidget):
    """
    params: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.CategoricalNB.html
    """

    def __init__(self, initial_data: dict = {}):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # alpha
        self.spin_box__alpha = QSpinBox()
        self.spin_box__alpha.setMaximum(2147483647)
        sub_layout, label = add_label("alpha", self.spin_box__alpha)
        layout.addLayout(sub_layout)

        self.set_params(initial_data)

    def get_params(self):
        return {
            "alpha": self.spin_box__alpha.value(),
        }

    def set_params(self, params: dict):
        self.spin_box__alpha.setValue(params.get("alpha", 1))


class DecisionTreeClassifierOptionsWidget(QWidget):
    """
    params: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
    """

    def __init__(self, initial_data: dict = {}):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # random_state
        self.spin_box__random_state = QSpinBox()
        self.spin_box__random_state.setMaximum(2147483647)
        sub_layout, label = add_label("random_state", self.spin_box__random_state)
        layout.addLayout(sub_layout)

        self.set_params(initial_data)

    def get_params(self):
        return {
            "random_state": self.spin_box__random_state.value(),
        }

    def set_params(self, params: dict):
        self.spin_box__random_state.setValue(params.get("random_state", 1))
