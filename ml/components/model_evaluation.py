import sys
import json
from pathlib import Path

import mlflow
import mlflow.xgboost
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)

from ml.constants.fraud_constants import (
    MIN_RECALL,
    MIN_PRECISION,
    MIN_F1_SCORE,
    MIN_ROC_AUC,
    MIN_PR_AUC,
    MODEL_EVALUATION_DIR,
    METRICS_PATH,
    CONFUSION_MATRIX_FILE_NAME,
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_MODEL_NAME,
)

from ml.utils.logger import logging
from ml.utils.exception import MyException


class ModelEvaluation:

    def __init__(self):
        pass

    def evaluate(
        self,
        model,
        X_test,
        y_test,
        threshold=0.50,
    ):

        try:

            logging.info(
                "Starting model evaluation"
            )

            probabilities = model.predict_proba(
                X_test
            )[:, 1]

            best_thresh_info = self.find_best_threshold(
                y_test,
                probabilities
            )

            if best_thresh_info.get("threshold") is not None:
                threshold = best_thresh_info["threshold"]

            predictions = (
                probabilities >= threshold
            ).astype(int)

            metrics = self._calculate_metrics(
                y_test,
                predictions,
                probabilities,
                threshold,
            )

            logging.info(
                f"Model metrics: {metrics}"
            )

            self._save_metrics(
                metrics
            )

            self._save_confusion_matrix(
                y_test,
                predictions
            )

            self._validate_model_quality(
                metrics
            )

            self._log_to_mlflow(
                model,
                metrics
            )

            logging.info(
                "Model evaluation completed successfully"
            )

            return metrics

        except Exception as e:

            logging.exception(
                "Model evaluation failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    def find_best_threshold(
        self,
        y_true,
        probabilities,
        minimum_recall=MIN_RECALL,
    ):

        logging.info(
            "Searching for optimal fraud threshold"
        )

        thresholds = np.arange(
            0.05,
            0.96,
            0.01
        )

        best_threshold = None
        best_f1 = -1
        best_precision = 0.0
        best_recall = 0.0

        threshold_results = []

        for threshold in thresholds:

            predictions = (
                probabilities >= threshold
            ).astype(int)

            recall = recall_score(
                y_true,
                predictions,
                zero_division=0
            )

            precision = precision_score(
                y_true,
                predictions,
                zero_division=0
            )

            f1 = f1_score(
                y_true,
                predictions,
                zero_division=0
            )

            threshold_results.append(
                {
                    "threshold": float(threshold),
                    "precision": float(precision),
                    "recall": float(recall),
                    "f1": float(f1),
                }
            )

            if (
                recall >= minimum_recall
                and f1 > best_f1
            ):
                best_threshold = float(
                    threshold
                )

                best_f1 = float(f1)

                best_precision = float(
                    precision
                )

                best_recall = float(
                    recall
                )

        if best_threshold is None:

            logging.warning(
                "No threshold satisfied the minimum recall requirement"
            )

            return {
                "threshold": None,
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "all_results": threshold_results,
            }

        result = {
            "threshold": best_threshold,
            "precision": best_precision,
            "recall": best_recall,
            "f1": best_f1,
            "all_results": threshold_results,
        }

        logging.info(
            f"Best threshold: {best_threshold:.2f}"
        )

        logging.info(
            f"Threshold recall: {best_recall:.4f}"
        )

        logging.info(
            f"Threshold precision: {best_precision:.4f}"
        )

        logging.info(
            f"Threshold F1: {best_f1:.4f}"
        )

        return result

    def _calculate_metrics(
        self,
        y_true,
        predictions,
        probabilities,
        threshold,
    ):

        return {
            "accuracy": accuracy_score(
                y_true,
                predictions
            ),

            "precision": precision_score(
                y_true,
                predictions,
                zero_division=0
            ),

            "recall": recall_score(
                y_true,
                predictions,
                zero_division=0
            ),

            "f1": f1_score(
                y_true,
                predictions,
                zero_division=0
            ),

            "roc_auc": roc_auc_score(
                y_true,
                probabilities
            ),

            "pr_auc": average_precision_score(
                y_true,
                probabilities
            ),

            "threshold": float(threshold),
        }

    def _validate_model_quality(
        self,
        metrics
    ):

        logging.info(
            "Running model quality gates"
        )

        failures = []

        if metrics["recall"] < MIN_RECALL:

            failures.append(
                f"Recall {metrics['recall']:.4f} "
                f"< minimum {MIN_RECALL}"
            )

        if metrics["precision"] < MIN_PRECISION:

            failures.append(
                f"Precision {metrics['precision']:.4f} "
                f"< minimum {MIN_PRECISION}"
            )

        if metrics["f1"] < MIN_F1_SCORE:

            failures.append(
                f"F1 {metrics['f1']:.4f} "
                f"< minimum {MIN_F1_SCORE}"
            )

        if metrics["roc_auc"] < MIN_ROC_AUC:

            failures.append(
                f"ROC-AUC {metrics['roc_auc']:.4f} "
                f"< minimum {MIN_ROC_AUC}"
            )

        if metrics["pr_auc"] < MIN_PR_AUC:

            failures.append(
                f"PR-AUC {metrics['pr_auc']:.4f} "
                f"< minimum {MIN_PR_AUC}"
            )

        if failures:

            logging.error(
                "Model quality gate FAILED"
            )

            for failure in failures:
                logging.error(
                    failure
                )

            raise ValueError(
                "Model rejected by quality gate:\n"
                + "\n".join(failures)
            )

        logging.info(
            "Model quality gate PASSED"
        )

    def _save_metrics(
        self,
        metrics
    ):

        Path(
            MODEL_EVALUATION_DIR
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            METRICS_PATH,
            "w"
        ) as file:

            json.dump(
                metrics,
                file,
                indent=4
            )

        logging.info(
            f"Metrics saved to {METRICS_PATH}"
        )

    def _save_confusion_matrix(
        self,
        y_test,
        predictions
    ):

        matrix = confusion_matrix(
            y_test,
            predictions
        )

        confusion_matrix_path = (
            Path(MODEL_EVALUATION_DIR)
            / CONFUSION_MATRIX_FILE_NAME
        )

        with open(
            confusion_matrix_path,
            "w"
        ) as file:

            json.dump(
                matrix.tolist(),
                file,
                indent=4
            )

        logging.info(
            f"Confusion matrix saved to "
            f"{confusion_matrix_path}"
        )

    def _log_to_mlflow(
        self,
        model,
        metrics
    ):

        mlflow.set_experiment(
            MLFLOW_EXPERIMENT_NAME
        )

        with mlflow.start_run():

            for name, value in metrics.items():

                mlflow.log_metric(
                    name,
                    float(value)
                )

            mlflow.set_tag(
                "model_type",
                "xgboost"
            )

            mlflow.set_tag(
                "project",
                "AI-Banking-Agent-Platform"
            )

            mlflow.xgboost.log_model(
                model,
                name="fraud_model",
                registered_model_name=MLFLOW_MODEL_NAME
            )

        logging.info(
            "Model logged to MLflow successfully"
        )