from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


from PySide6.QtCore import *
from PySide6.QtWidgets import *

from maxes.app.application_context import ApplicationContext
from maxes.app.background_tasks import (
    ApplicationProcess,
    prepare_nlogger,
)
from maxes.app.widgets.sklearn_model_options import (
    KNeighborsClassifierOptionsWidget,
    CategoricalNBOptionsWidget,
    DecisionTreeClassifierOptionsWidget,
)

from maxes.logging import NestedLogger
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3 as XesGenerator
from maxes.xes_log import XesLog, CONCEPT_NAME, LIFECYCLE_TRANSITION, TIME_TIMESTAMP

from maxes.utils import dig

DEFAULT_MODEL = "CategoricalNB"


model_options = {
    "CategoricalNB": CategoricalNB,
    "KNeighborsClassifier": KNeighborsClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "RandomForestClassifier": RandomForestClassifier,
}

model_to_options_widget = {
    "CategoricalNB": CategoricalNBOptionsWidget,
    "KNeighborsClassifier": KNeighborsClassifierOptionsWidget,
    "DecisionTreeClassifier": DecisionTreeClassifierOptionsWidget,
    "RandomForestClassifier": DecisionTreeClassifierOptionsWidget,
}


class AttributesTab(QWidget):
    def __init__(self, ctx: ApplicationContext):
        super().__init__()

        self.ctx = ctx
        self.ctx.events.xes_log_loaded.connect(self._on__ctx__xes_log_loaded)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # Attribute select
        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)

        label = QLabel("Attribute")
        layout_1.addWidget(label)

        self.combobox__attribute = QComboBox()

        self.combobox__attribute.currentTextChanged.connect(
            self._on__combobox__attribute__current_text_changed
        )
        layout_1.addWidget(self.combobox__attribute)

        # model select
        layout_2 = QHBoxLayout()
        layout.addLayout(layout_2)

        label = QLabel("Model")
        layout_2.addWidget(label)

        self.combobox__model = QComboBox()
        for model_name in model_options.keys():
            self.combobox__model.addItem(model_name)
        self.combobox__model.setCurrentText(DEFAULT_MODEL)
        self.combobox__model.currentTextChanged.connect(
            self._on__combobox__model__current_text_changed
        )
        layout_2.addWidget(self.combobox__model)

        # model-specific params
        self.model_options_container = QWidget()
        self.model_options_container.setLayout(QVBoxLayout())
        layout.addWidget(self.model_options_container)

        options_widget_class = model_to_options_widget[DEFAULT_MODEL]
        self.model_options_widget = options_widget_class()
        self.model_options_container.layout().addWidget(self.model_options_widget)

        # train button
        self.button__train_model = QPushButton("Train model")
        self.button__train_model.released.connect(
            self._on__button__train_model__released
        )
        layout.addWidget(self.button__train_model)

        # test accuracy button

    def _on__ctx__xes_log_loaded(self):
        attributes = [
            attribute
            for attribute in self.ctx.xes_log.df.columns
            if attribute
            not in [
                CONCEPT_NAME,
                LIFECYCLE_TRANSITION,
                TIME_TIMESTAMP,
            ]
        ]

        self.combobox__attribute.clear()
        for attribute in attributes:
            self.combobox__attribute.addItem(attribute)

    def _on__combobox__attribute__current_text_changed(self, text):
        print("_on__combobox__attribute__current_text_changed")

        xes_generator = self.ctx.xes_generator
        attributes_models = xes_generator.attributes_models

        if text not in attributes_models:
            attributes_models[text] = {}

        attribute_params = attributes_models[text]

        model_name = attribute_params.get("model_name", "CategoricalNB")
        self.combobox__model.setCurrentText(model_name)

    def _on__combobox__model__current_text_changed(self, text):
        print("_on__combobox__model__current_text_changed")

        selected_attribute_text = self.combobox__attribute.currentText()

        self.model_options_container.layout().removeWidget(self.model_options_widget)
        self.model_options_widget.deleteLater()

        options_widget_class = model_to_options_widget[text]

        xes_generator = self.ctx.xes_generator
        attributes_models = xes_generator.attributes_models

        model_kwargs = (
            dig(attributes_models, selected_attribute_text, "model_kwargs") or {}
        )

        self.model_options_widget = options_widget_class(model_kwargs)
        self.model_options_container.layout().addWidget(self.model_options_widget)

    def _on__button__train_model__released(self):
        selected_attribute_text = self.combobox__attribute.currentText()
        selected_model_text = self.combobox__model.currentText()

        xes_generator = self.ctx.xes_generator
        attributes_models = xes_generator.attributes_models

        attributes_models[selected_attribute_text] = {}
        attributes_models[selected_attribute_text]["model_name"] = selected_model_text
        attributes_models[selected_attribute_text][
            "model_kwargs"
        ] = self.model_options_widget.get_params()

        xes_generator.fit_event_level_attribute_model(selected_attribute_text)
