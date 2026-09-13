import sys

import mlflow

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from ml.utils.exception import MyException
from ml.utils.logger import logging


class IntentEvaluator:

    def evaluate(self, model, X_test, y_test):

        try:

            logging.info(
                "Starting intent model evaluation"
            )

            predictions = model.predict(
                X_test
            )

            accuracy = accuracy_score(
                y_test,
                predictions
            )

            precision = precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            recall = recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            mlflow.log_metric(
                "accuracy",
                accuracy
            )

            mlflow.log_metric(
                "precision",
                precision
            )

            mlflow.log_metric(
                "recall",
                recall
            )

            mlflow.log_metric(
                "f1_score",
                f1
            )

            logging.info(
                f"Accuracy: {accuracy:.4f}"
            )

            logging.info(
                f"Precision: {precision:.4f}"
            )

            logging.info(
                f"Recall: {recall:.4f}"
            )

            logging.info(
                f"F1 Score: {f1:.4f}"
            )

            print(f"Accuracy  : {accuracy:.4f}")
            print(f"Precision : {precision:.4f}")
            print(f"Recall    : {recall:.4f}")
            print(f"F1 Score  : {f1:.4f}")

            logging.info(
                "Intent model evaluation completed successfully"
            )

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }

        except Exception as e:

            logging.exception(
                "Error occurred during intent model evaluation"
            )

            raise MyException(e, sys) from e