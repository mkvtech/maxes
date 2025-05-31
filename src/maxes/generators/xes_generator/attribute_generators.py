import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# MLPClassifier, ClassifierNB, RandomForestClassifier


class AttributePredictorBase:
    def __init__(self, random_state=None):
        self.random_state = random_state

    def fit_transformers(self, X: pd.DataFrame, y: pd.Series):
        raise NotImplementedError()

    def fit(self, X: pd.DataFrame, y: pd.Series):
        raise NotImplementedError()

    def predict(self, X: pd.DataFrame):
        raise NotImplementedError()


class AttributeGenerator:
    def __init__(
        self,
        input_columns: list[str],
        output_column: str,
        model: AttributePredictorBase,
    ):
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = model

    def fit_transformers(self, df: pd.DataFrame):
        X, y = self.split_xy(df)
        self.model.fit_transformers(X, y)

    def fit(self, df: pd.DataFrame):
        X, y = self.split_xy(df)
        self.model.fit(X, y)

        return self

    def predict(self, df: pd.DataFrame):
        X = df[self.input_columns]
        y_pred = self.model.predict(X)

        return y_pred

    def split_xy(self, df: pd.DataFrame):
        return df[self.input_columns], df[self.output_column]

    def score(self, df: pd.DataFrame):
        X, y = self.split_xy(df)
        return self.model.score(X, y)


class AttributePredictor_MLPClassifier(AttributePredictorBase):
    def __init__(self, random_state=None):
        super().__init__(random_state=random_state)

        self._is_transformers_fit = False

    def clone_unfitted(self):
        return AttributePredictor_MLPClassifier(random_state=self.random_state)

    def get_params(self, deep):
        return {"random_state": self.random_state}

    def set_params(self, **kwargs):
        self.random_state = kwargs["random_state"]

    def fit_transformers(self, X: pd.DataFrame, y: pd.Series):
        self.input_encoder = OneHotEncoder()
        self.input_encoder.fit(X)

        self.output_encoder = OneHotEncoder()
        y_np = np.array(y).reshape(-1, 1)
        self.output_encoder.fit(y_np)

        self._is_transformers_fit = True

    def fit(self, X: pd.DataFrame, y: pd.Series):
        if not self._is_transformers_fit:
            raise RuntimeError(
                "Input/Output transformers are not trained. Please use .fit_transformers(X, y)"
            )

        X = self.input_encoder.transform(X)

        y_np = np.array(y).reshape(-1, 1)
        y = self.output_encoder.transform(y_np)

        self.model = MLPClassifier(random_state=self.random_state)
        self.model.fit(X, y)

        return self

    def predict(self, X: pd.DataFrame):
        X = self.input_encoder.transform(X)
        y_pred = self.model.predict(X)
        y_pred = self.output_encoder.inverse_transform(y_pred).ravel()

        return y_pred

    def score(self, X: pd.DataFrame, y: pd.Series):
        X = self.input_encoder.transform(X)
        y_np = np.array(y).reshape(-1, 1)
        y = self.output_encoder.transform(y_np)

        return self.model.score(X, y)


class AttributePredictor_ClassifierWrapper(AttributePredictorBase):
    def __init__(self, inner_model_class, inner_model_kwargs={}, random_state=None):
        super().__init__(random_state=random_state)
        self.inner_model_class = inner_model_class
        self.inner_model_kwargs = inner_model_kwargs
        self._is_transformers_fit = False

    def get_params(self, deep):
        return {
            "random_state": self.random_state,
            "inner_model_class": self.inner_model_class,
            "inner_model_kwargs": self.inner_model_kwargs,
        }

    def set_params(self, **kwargs):
        self.random_state = kwargs["random_state"]
        self.inner_model_class = kwargs["inner_model_class"]
        self.inner_model_kwargs = kwargs["inner_model_kwargs"]

    def fit_transformers(self, X: pd.DataFrame, y: pd.Series):
        self.input_encoder = OneHotEncoder()
        self.input_encoder.fit(X)

        self.output_encoder = LabelEncoder()
        y_np = np.array(y)
        self.output_encoder.fit(y_np)

        self._is_transformers_fit = True

    def fit(self, X: pd.DataFrame, y: pd.Series):
        if not self._is_transformers_fit:
            raise RuntimeError(
                "Input/Output transformers are not trained. Please use .fit_transformers(X, y)"
            )

        X = self.input_encoder.transform(X)
        X = np.asarray(X.todense())

        y_np = np.array(y)
        y = self.output_encoder.transform(y_np)

        self.model = self.inner_model_class(**self.inner_model_kwargs)
        self.model.fit(X, y)

        return self

    def predict(self, X: pd.DataFrame):
        X = self.input_encoder.transform(X)
        X = np.asarray(X.todense())

        y_pred = self.model.predict(X)
        y_pred = self.output_encoder.inverse_transform(y_pred).ravel()

        return y_pred

    def score(self, X: pd.DataFrame, y: pd.Series):
        X = self.input_encoder.transform(X)
        X = np.asarray(X.todense())

        y_np = np.array(y)
        y = self.output_encoder.transform(y_np)

        return self.model.score(X, y)
