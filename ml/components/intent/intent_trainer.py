import sys

import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from ml.utils.exception import MyException
from ml.utils.logger import logging


class IntentTrainer:

    def train(self, X_train, y_train):

        try:

            logging.info(
                "Starting TF-IDF + Logistic Regression training"
            )

            model = Pipeline([
                (
                    "tfidf",
                    TfidfVectorizer(
                        ngram_range=(1, 2),
                        sublinear_tf=True,
                        max_features=50000
                    )
                ),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=1000
                    )
                )
            ])

            model.fit(
                X_train,
                y_train
            )

            logging.info(
                "Intent model training completed"
            )

            mlflow.log_param(
                "model",
                "LogisticRegression"
            )

            mlflow.log_param(
                "vectorizer",
                "TF-IDF"
            )

            mlflow.log_param(
                "ngram_range",
                "(1,2)"
            )

            mlflow.log_param(
                "sublinear_tf",
                True
            )

            mlflow.log_param(
                "max_features",
                50000
            )

            mlflow.log_param(
                "max_iter",
                1000
            )

            mlflow.sklearn.log_model(
                model,
                "intent_detection_model"
            )

            logging.info(
                "Intent model logged to MLflow"
            )

            return model

        except Exception as e:

            logging.exception(
                "Error occurred during intent model training"
            )

            raise MyException(e, sys) from e